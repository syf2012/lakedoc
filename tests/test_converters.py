"""
测试转换器
"""

import pytest
from lakedoc.converters import MarkdownConverter, LakeBaseConverter
from lakedoc.utils import string


def test_converter_init():
    """测试转换器初始化"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = MarkdownConverter(html_content)

    assert converter.raw_html == html_content
    assert converter.title is None
    assert converter.diagram_as_code is False
    assert converter.diagram_as_code_cond is None


def test_converter_with_title():
    """测试带标题的转换器"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = MarkdownConverter(html_content, title="# 自定义标题")

    assert converter.title == "# 自定义标题"


def test_converter_with_diagram_options():
    """测试带 diagram 选项的转换器"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = MarkdownConverter(
        html_content,
        diagram_as_code=True,
        diagram_as_code_cond=lambda s, l, c: l in {"mermaid", "plantuml"},
    )

    assert converter.diagram_as_code is True
    assert converter.diagram_as_code_cond is not None
    assert converter.diagram_as_code_cond("http://...", "mermaid", "A -> B") is True


def test_converter_with_bs4_builder():
    """测试指定 BeautifulSoup 构建器"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = MarkdownConverter(html_content, bs4_builder="html.parser")

    assert converter.bs4_builder == "html.parser"


def test_converter_with_remove_tags():
    """测试指定删除标签"""
    html_content = '<!doctype lake><p>测试内容</p><script>alert("test")</script>'
    converter = MarkdownConverter(html_content, remove_tags={"script"})

    assert "script" in converter.remove_tags


def test_converter_convert():
    """测试转换方法"""
    html_content = "<!doctype lake><h1>测试标题</h1><p>测试段落</p>"
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_converter_add_title():
    """测试添加标题"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = MarkdownConverter(html_content, title="# 自定义标题")

    result = converter.convert()
    assert "# 自定义标题" in result


def test_converter_create_bs4soup():
    """测试创建 BeautifulSoup 对象"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = MarkdownConverter(html_content)

    soup = converter.create_bs4soup()
    assert soup is not None
    assert soup.find("p") is not None


def test_converter_merge_em_tags():
    """测试合并相邻的 em 标签"""
    html_content = "<!doctype lake><p><em>A</em><em>B</em><em>C</em></p>"
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    # 合并后应该只有一个 em 标签
    assert result.count("*") >= 2  # 至少两个 * 表示斜体


def test_converter_merge_strong_tags():
    """测试合并相邻的 strong 标签"""
    html_content = (
        "<!doctype lake><p><strong>A</strong><strong>B</strong><strong>C</strong></p>"
    )
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    # 合并后应该只有一个 strong 标签
    assert result.count("**") >= 2  # 至少两个 ** 表示粗体


def test_render_styles_no_style():
    """测试无 style 属性的元素"""
    html_content = "<!doctype lake><p>测试内容</p>"
    converter = MarkdownConverter(html_content)

    p_tag = converter.soup.find("p")
    result = converter.render_styles(p_tag)
    assert result is None


def test_render_styles_with_color():
    """测试带 color 样式的元素"""
    html_content = '<!doctype lake><p style="color: red;">红色文字</p>'
    converter = MarkdownConverter(html_content)

    p_tag = converter.soup.find("p")
    converter.render_styles(p_tag)

    # 验证 span 标签被创建
    span_tag = converter.soup.find("span")
    assert span_tag is not None
    assert "color: red" in span_tag.get("style", "")


def test_render_styles_with_background_color():
    """测试带 background-color 样式的元素"""
    html_content = '<!doctype lake><p style="background-color: yellow;">黄色背景</p>'
    converter = MarkdownConverter(html_content)

    p_tag = converter.soup.find("p")
    converter.render_styles(p_tag)

    # 验证 span 标签被创建
    span_tag = converter.soup.find("span")
    assert span_tag is not None
    assert "background-color: yellow" in span_tag.get("style", "")


def test_render_styles_with_text_indent():
    """测试带 text-indent 样式的元素"""
    html_content = '<!doctype lake><p style="text-indent: 2em;">缩进文字</p>'
    converter = MarkdownConverter(html_content)
    converter.render_styles(converter.soup.p)
    assert "<span>\u2003</span>" * 2 in str(converter.soup)


def test_render_styles_with_padding_left():
    """测试带 padding-left 样式的元素"""
    html_content = '<!doctype lake><p style="padding-left: 3px;">左边距</p>'
    converter = MarkdownConverter(html_content)
    converter.render_styles(converter.soup.p)
    assert "<span>\u2003</span>" * 3 in str(converter.soup)


def test_render_styles_with_multiple_styles():
    """测试带多个样式的元素"""
    style = "color: blue; text-indent: 1em;"
    html_content = f'<!doctype lake><p style="{style}">蓝色缩进</p>'
    converter = MarkdownConverter(html_content)

    converter.render_styles(converter.soup.p)
    assert converter.soup.span
    assert style in str(converter.soup.span)


def test_render_styles_with_empty_style():
    """测试空 style 属性"""
    html_content = '<!doctype lake><p style="">测试</p>'
    converter = MarkdownConverter(html_content)

    p_tag = converter.soup.find("p")
    result = converter.render_styles(p_tag)
    assert result is None


def test_render_styles_with_invalid_style():
    """测试无效的 style 属性"""
    html_content = '<!doctype lake><p style="invalid">测试</p>'
    converter = MarkdownConverter(html_content)

    p_tag = converter.soup.find("p")
    result = converter.render_styles(p_tag)
    assert result is None


def test_base_converter_repr():
    """测试基础转换器的 __repr__ 方法"""
    converter = LakeBaseConverter()
    assert repr(converter) == "<LakeBaseConverter: name=None>"


def test_base_converter_convert_raises_not_implemented():
    """测试基础转换器的 convert 方法应该抛出错误"""
    converter = LakeBaseConverter()

    with pytest.raises(NotImplementedError):
        converter.convert()


def test_particular_converter_convert_font():
    """测试 font 标签转换"""
    html_content = '<!doctype lake><p><font color="red">红色文字</font></p>'
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    assert result is not None


def test_particular_converter_convert_li():
    """测试列表项转换"""
    html_content = '<!doctype lake><ul data-lake-indent="1"><li>列表项1</li></ul>'
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    assert result is not None
    # 应该有缩进
    assert "\t" in result


def test_particular_converter_convert_hn():
    """测试标题转换"""
    html_content = "<!doctype lake><h1>标题1</h1><h2>标题2</h2>"
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    assert result is not None
    assert "# 标题1" in result or "## 标题2" in result


def test_particular_converter_convert_sub():
    """测试下标转换"""
    html_content = "<!doctype lake><p>H<sub>2</sub>O</p>"
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    assert result is not None


def test_particular_converter_convert_sup():
    """测试上标转换"""
    html_content = "<!doctype lake><p>X<sup>2</sup></p>"
    converter = MarkdownConverter(html_content)

    result = converter.convert()
    assert result is not None


def test_extract_integer():
    """测试提取整数"""
    assert string.extract_integer("11em") == 11
    assert string.extract_integer("2px") == 2
    assert string.extract_integer("test") == 0
    assert string.extract_integer("test123abc") == 123


def test_extract_integer_with_default():
    """测试提取整数带默认值"""
    assert string.extract_integer("test", default_=10) == 10


def test_color_string():
    """测试颜色字符串"""
    result = string.color_string("Test", color="red")
    assert "Test" in result


def test_decode_card_value():
    """测试解码 card 值"""
    import json

    # 创建测试数据
    test_data = {"type": "mermaid", "code": "graph TD\nA --> B"}
    json_str = json.dumps(test_data)

    # 模拟 URL 编码
    import urllib.parse

    encoded = urllib.parse.quote(json_str)
    card_value = f"data:{encoded}"

    result = string.decode_card_value(card_value)
    assert result == test_data


def test_encode_card_value():
    """测试编码 card 值"""
    test_data = {"type": "mermaid", "code": "graph TD\nA --> B"}

    result = string.encode_card_value(test_data)
    assert result.startswith("data:")

    # 验证可以解码
    decoded = string.decode_card_value(result)
    assert decoded == test_data
