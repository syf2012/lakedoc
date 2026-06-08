"""
测试 HTML 转换器
"""

from lakedoc.converters import HTMLConverter


def test_html_converter_init():
    """测试 HTML 转换器初始化"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content)

    assert converter.raw_html == html_content
    assert converter.title is None


def test_html_converter_with_title():
    """测试带标题的 HTML 转换器"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content, title="自定义标题")

    assert converter.title == "自定义标题"


def test_html_converter_with_diagram_options():
    """测试带 diagram 选项的 HTML 转换器"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(
        html_content,
        diagram_as_code=True,
        diagram_as_code_cond=lambda s, l, c: l in {"mermaid", "plantuml"},
    )

    # 通过内部 md_converter 验证选项
    assert converter._md_converter.diagram_as_code is True
    assert converter._md_converter.diagram_as_code_cond is not None
    assert (
        converter._md_converter.diagram_as_code_cond("http://...", "mermaid", "A -> B")
        is True
    )


def test_html_converter_with_bs4_builder():
    """测试指定 BeautifulSoup 构建器"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content, bs4_builder="html.parser")

    # 通过内部 md_converter 验证选项
    assert converter._md_converter.bs4_builder == "html.parser"


def test_html_converter_with_remove_tags():
    """测试指定删除标签"""
    html_content = '<!doctype lake><p>测试内容</p><script>alert("test")</script>'
    converter = HTMLConverter(html_content, remove_tags={"script"})

    # 通过内部 md_converter 验证选项
    assert "script" in converter._md_converter.remove_tags


def test_html_converter_convert():
    """测试 HTML 转换方法"""
    html_content = "<!doctype lake><h1>测试标题</h1><p>测试段落</p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
    assert "<!DOCTYPE html>" in result
    assert "<html" in result
    assert "</html>" in result


def test_html_converter_with_custom_title():
    """测试带自定义标题的转换"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content, title="我的文档")

    result = converter.convert()
    assert "<title>我的文档</title>" in result


def test_html_converter_default_title():
    """测试默认标题"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<title>Lake Document</title>" in result


def test_html_converter_with_custom_extensions():
    """测试自定义 Markdown 扩展"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content, md_extensions=["markdown.extensions.extra"])

    assert "markdown.extensions.extra" in converter.md_extensions


def test_html_converter_with_extension_configs():
    """测试 Markdown 扩展配置"""
    html_content = "<!doctype lake><p>测试内容</p>"
    extension_configs = {"markdown.extensions.codehilite": {"linenums": True}}
    converter = HTMLConverter(html_content, extension_configs=extension_configs)

    assert converter.extension_configs == extension_configs


def test_html_converter_convert_heading():
    """测试标题转换"""
    html_content = "<!doctype lake><h1>标题1</h1><h2>标题2</h2>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "</h1>" in result
    assert "</h2>" in result
    assert "标题1" in result
    assert "标题2" in result


def test_html_converter_convert_paragraph():
    """测试段落转换"""
    html_content = "<!doctype lake><p>测试段落</p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<p>" in result
    assert "测试段落" in result


def test_html_converter_convert_list():
    """测试列表转换"""
    html_content = "<!doctype lake><ul><li>列表项1</li><li>列表项2</li></ul>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<ul>" in result
    assert "<li>" in result
    assert "列表项1" in result
    assert "列表项2" in result


def test_html_converter_convert_code():
    """测试代码块转换"""
    html_content = '<!doctype lake><card name="codeblock" value="data:%7B%22mode%22%3A%22python%22%2C%22code%22%3A%22print(%27hello%27)%22%7D"></card>'
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "</pre>" in result
    assert "</code>" in result
    assert "print" in result


def test_html_converter_convert_bold_italic():
    """测试粗体和斜体转换"""
    html_content = "<!doctype lake><p><strong>粗体</strong><em>斜体</em></p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<strong>" in result or "<b>" in result
    assert "<em>" in result or "<i>" in result


def test_html_converter_convert_link():
    """测试链接转换"""
    html_content = '<!doctype lake><p><a href="https://example.com">链接</a></p>'
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert '<a href="https://example.com"' in result
    assert "链接" in result


def test_html_converter_html_structure():
    """测试完整的 HTML 文档结构"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<!DOCTYPE html>" in result
    assert '<html lang="zh-CN">' in result
    assert "<head>" in result
    assert '<meta charset="UTF-8">' in result
    assert '<meta name="viewport"' in result
    assert "<body>" in result
    assert "</body>" in result
    assert "</html>" in result


def test_html_converter_css_styles():
    """测试 CSS 样式包含"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<style>" in result
    assert "font-family" in result
    assert "line-height" in result
    assert "max-width" in result


def test_html_converter_name_and_suffix():
    """测试转换器名称和后缀"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = HTMLConverter(html_content)

    assert converter.name == "html"
    assert converter.suffix == ".html"


def test_html_converter_convert_table():
    """测试表格转换"""
    html_content = '<!doctype lake><card name="table" value="data:%7B%22html%22%3A%22%3Ctable%3E%3Ctr%3E%3Cth%3E%E8%A1%A8%E5%A4%B4%3C%2Fth%3E%3C%2Ftr%3E%3Ctr%3E%3Ctd%3E%E5%86%85%E5%AE%B9%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E%22%7D"></card>'
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<table>" in result
    assert "<th>" in result
    assert "<td>" in result


def test_html_converter_convert_blockquote():
    """测试引用块转换"""
    html_content = "<!doctype lake><blockquote>引用内容</blockquote>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<blockquote>" in result
    assert "引用内容" in result


def test_html_converter_convert_horizontal_rule():
    """测试分隔线转换"""
    html_content = '<!doctype lake><card name="hr" value="data:%7B%7D"></card>'
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<hr" in result


def test_html_converter_convert_math():
    """测试数学公式转换"""
    html_content = '<!doctype lake><card name="math" value="data:%7B%22code%22%3A%22E%3Dmc%5E2%22%7D"></card>'
    converter = HTMLConverter(html_content)
    result = converter.convert()
    assert "E=mc^2" in result


def test_html_converter_convert_diagram():
    """测试图表转换"""
    html_content = '<!doctype lake><card name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%7D"></card>'
    converter = HTMLConverter(html_content)
    result = converter.convert()
    assert "graph" in result or "mermaid" in result.lower()


def test_html_converter_convert_image():
    """测试图片转换"""
    html_content = '<!doctype lake><card name="image" value="data:%7B%22src%22%3A%22https%3A%2F%2Fexample.com%2Fimage.png%22%7D"></card>'
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<img" in result
    assert "https://example.com/image.png" in result


def test_html_converter_convert_subscript():
    """测试下标转换"""
    html_content = "<!doctype lake><p>H<sub>2</sub>O</p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "<sub>" in result or "H₂O" in result


def test_html_converter_convert_superscript():
    """测试上标转换"""
    html_content = "<!doctype lake><p>X<sup>2</sup></p>"
    converter = HTMLConverter(html_content)

    result = converter.convert()
    assert "</sup>" in result or "X²" in result
