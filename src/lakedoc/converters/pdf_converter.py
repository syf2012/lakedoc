"""
PDF 转换器

作者：
    gupingan [gupingan6@outlook.com]

特性：
    - 将 Lake 文档转换为 PDF 格式
    - 基于 HTMLConverter 生成中间 HTML，再通过 weasyprint 渲染为 PDF
    - html -> md -> html -> pdf

注意：
    - 需要安装 weasyprint：pip install weasyprint
    - weasyprint 依赖系统级库（如 GTK/Pango），Windows 用户可能需要额外配置
"""

from typing import Optional, Set, List, Dict, Callable, Union
from pathlib import Path

from bs4.element import Tag
from weasyprint import HTML, CSS
from lakedoc.utils import debug as debug_module
from .base import LakeBaseConverter
from .html_converter import HTMLConverter
from .ht2md import (
    HeadingStyle,
    NewlineStyle,
    StrongEmSymbol,
    StripMode,
)


class PdfConverter(LakeBaseConverter):
    """
    PDF 转换器，继承自 LakeBaseConverter

    设计原则：
    1. 使用 HTMLConverter 将原始 HTML 转换为带样式的完整 HTML 文档
    2. 使用 weasyprint 将 HTML 文档渲染为 PDF 字节流
    3. 支持自定义 PDF 样式（通过额外 CSS 样式表）
    """

    name = "pdf"
    suffix = ".pdf"

    def __init__(
        self,
        raw_html: str,
        bs4_builder: str = "html.parser",
        title: Optional[str] = None,
        remove_tags: Optional[Set[str]] = None,
        remove_watermark: bool = False,
        diagram_as_code: bool = False,
        diagram_as_code_cond: Optional[Callable[[str, str, str], bool]] = None,
        autolinks: bool = True,
        bullets: str = "*+-",
        code_language: str = "",
        code_language_callback: Optional[Callable[[Tag], Optional[str]]] = None,
        convert: Optional[List[str]] = None,
        default_title: bool = False,
        escape_asterisks: bool = True,
        escape_underscores: bool = True,
        escape_misc: bool = False,
        heading_style: HeadingStyle = HeadingStyle.ATX,
        keep_inline_images_in: Optional[List[str]] = None,
        newline_style: NewlineStyle = NewlineStyle.SPACES,
        strip: Optional[List[str]] = None,
        strip_document: Optional[StripMode] = StripMode.STRIP,
        strip_pre: Optional[StripMode] = StripMode.STRIP,
        strong_em_symbol: StrongEmSymbol = StrongEmSymbol.ASTERISK,
        sub_symbol: str = "~",
        sup_symbol: str = "^",
        table_infer_header: bool = False,
        wrap: bool = False,
        wrap_width: int = 80,
        md_extensions: Optional[List[str]] = None,
        extension_configs: Optional[Dict[str, Dict]] = None,
        # PDF 专有参数
        pdf_stylesheets: Optional[List[Union[str, CSS]]] = None,
        pdf_base_url: Optional[str] = None,
        pdf_presentational_hints: bool = True,
    ):
        """
        Lake Doc -> PDF Doc

        :param raw_html: 未经过处理的 HTML 内容（最原生的）
        :param bs4_builder: BeautifulSoup 的树构建器，默认为 'html.parser'
        :param title: 指定设置转换后 HTML 内容的标题，默认为 None
        :param remove_tags: 处理 html 时应该删除哪些标签，默认为 {'meta', 'link', 'script', 'style'}
        :param remove_watermark: 是否删除水印标签，默认为 False
        :param diagram_as_code: 是否将 diagram 转换为代码块格式，默认 False
        :param diagram_as_code_cond: 指定需要转换为代码块的回调条件函数，参数是 (src, lang, code)
        :param autolinks: 是否自动将 URL 转换为自动链接格式
        :param bullets: 无序列表的标记字符序列
        :param code_language: 代码块的语言标识符
        :param code_language_callback: 代码块语言回调函数
        :param convert: 要转换的标签列表（与 strip 互斥）
        :param default_title: 是否为没有标题的链接使用 URL 作为默认标题
        :param escape_asterisks: 是否转义星号
        :param escape_underscores: 是否转义下划线
        :param escape_misc: 是否转义其他特殊字符
        :param heading_style: 标题样式（HeadingStyle枚举）：ATX / ATX_CLOSED / UNDERLINED / SETEXT
        :param keep_inline_images_in: 保持内联图片的父标签列表
        :param newline_style: 换行样式（NewLineStyle枚举）：SPACES / BACKSLASH
        :param strip: 要移除的标签列表（与 convert 互斥）
        :param strip_document: 文档空白处理方式（StripMode枚举）：LSTRIP / RSTRIP / STRIP / STRIP_ONE
        :param strip_pre: pre 标签空白处理方式（StripMode枚举）：LSTRIP / RSTRIP / STRIP / STRIP_ONE
        :param strong_em_symbol: 粗体和斜体符号（StrongEmSymbol枚举）：ASTERISK / UNDERSCORE
        :param sub_symbol: 下标符号，默认为 '~'
        :param sup_symbol: 上标符号，默认为 '^'
        :param table_infer_header: 是否推断表格标题行
        :param wrap: 是否自动换行
        :param wrap_width: 换行宽度
        :param md_extensions: Markdown 扩展列表
        :param extension_configs: Markdown 扩展配置
        :param pdf_stylesheets: 额外的 CSS 样式表列表，用于覆盖/补充 PDF 渲染样式。
                                元素可以是 CSS 文件路径字符串或 weasyprint.CSS 对象
        :param pdf_base_url: weasyprint 解析相对 URL（如图片路径）时使用的基准 URL，
                             默认为 None（使用当前工作目录）
        :param pdf_presentational_hints: 是否遵循 HTML 元素的表现性属性（如 align、width 等），
                                         默认 True
        """
        # 初始化 HTMLConverter 作为内部转换器（复用其 HTML 生成能力）
        html_options = {
            "bs4_builder": bs4_builder,
            "title": title,
            "remove_tags": remove_tags,
            "remove_watermark": remove_watermark,
            "diagram_as_code": diagram_as_code,
            "diagram_as_code_cond": diagram_as_code_cond,
            "autolinks": autolinks,
            "bullets": bullets,
            "code_language": code_language,
            "code_language_callback": code_language_callback,
            "convert": convert,
            "default_title": default_title,
            "escape_asterisks": escape_asterisks,
            "escape_underscores": escape_underscores,
            "escape_misc": escape_misc,
            "heading_style": heading_style,
            "keep_inline_images_in": keep_inline_images_in,
            "newline_style": newline_style,
            "strip": strip,
            "strip_document": strip_document,
            "strip_pre": strip_pre,
            "strong_em_symbol": strong_em_symbol,
            "sub_symbol": sub_symbol,
            "sup_symbol": sup_symbol,
            "table_infer_header": table_infer_header,
            "wrap": wrap,
            "wrap_width": wrap_width,
            "md_extensions": md_extensions,
            "extension_configs": extension_configs,
        }

        self._html_converter = HTMLConverter(raw_html, **html_options)

        # PDF 专有属性
        self.pdf_stylesheets = pdf_stylesheets or []
        self.pdf_base_url = pdf_base_url
        self.pdf_presentational_hints = pdf_presentational_hints

    def convert(self) -> bytes:
        """
        执行 HTML -> Markdown -> HTML -> PDF 的转换

        :return: PDF 文件的字节内容
        """
        debug_module.debug_section("PDF 转换开始")
        debug_module.debug(f"额外样式表数量: {len(self.pdf_stylesheets)}", level=1)
        debug_module.debug(f"基准 URL: {self.pdf_base_url}", level=1)

        # 1. 使用 HTMLConverter 生成完整的 HTML 文档
        debug_module.debug_subsection("生成中间 HTML", level=1)
        html_data = self._html_converter.convert()

        # 2. 使用 weasyprint 将 HTML 转换为 PDF
        debug_module.debug_subsection("HTML 到 PDF 转换", level=1)
        pdf_data = self._html_to_pdf(html_data)

        debug_module.debug_section("PDF 转换完成")
        debug_module.debug(f"PDF 输出大小: {len(pdf_data)} 字节", level=1)

        return pdf_data

    def _html_to_pdf(self, html_content: str) -> bytes:
        """
        使用 weasyprint 将 HTML 内容转换为 PDF 字节流

        :param html_content: 完整的 HTML 文档字符串
        :return: PDF 字节内容
        """

        debug_module.debug("正在使用 weasyprint 渲染 PDF...", level=2)

        # 构建 HTML 对象
        html_obj = HTML(string=html_content, base_url=self.pdf_base_url)

        # 处理额外的样式表
        stylesheets = []
        for sheet in self.pdf_stylesheets:
            if isinstance(sheet, str):
                # 字符串视为 CSS 文件路径
                sheet_path = Path(sheet)
                if sheet_path.exists():
                    stylesheets.append(CSS(filename=str(sheet_path)))
                    debug_module.debug(f"加载样式表: {sheet}", level=2)
                else:
                    debug_module.debug(
                        f"样式表文件不存在，已跳过: {sheet}", level=2, color="yellow"
                    )
            else:
                # 假设已经是 weasyprint.CSS 对象
                stylesheets.append(sheet)

        # 渲染为 PDF
        pdf_bytes = html_obj.write_pdf(
            stylesheets=stylesheets,
            presentational_hints=self.pdf_presentational_hints,
        )

        debug_module.debug(f"PDF 渲染完成，大小: {len(pdf_bytes)} 字节", level=2)

        return pdf_bytes