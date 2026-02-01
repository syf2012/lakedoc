"""
测试 debug 模式
"""

import lakedoc
from io import StringIO
import sys


def test_convert_with_debug_disabled():
    """测试禁用 debug 模式"""
    html_content = (
        "<!doctype lake><html><body><h1>测试标题</h1><p>测试段落</p></body></html>"
    )

    # 确保调试模式已禁用
    lakedoc.disable_debug()

    # 捕获标准输出
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        result = lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    # debug 禁用时应该没有输出
    assert result is not None
    assert "[DEBUG]" not in output


def test_convert_with_debug_enabled():
    """测试启用 debug 模式"""
    html_content = (
        "<!doctype lake><html><body><h1>测试标题</h1><p>测试段落</p></body></html>"
    )

    # 启用调试模式
    lakedoc.enable_debug()

    # 捕获标准输出
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        result = lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        # 恢复默认状态
        lakedoc.disable_debug()

    # debug 启用时应该有输出
    assert result is not None
    assert "[DEBUG]" in output
    assert "Markdown 转换开始" in output
    assert "Markdown 转换完成" in output


def test_debug_output_contains_sections():
    """测试 debug 输出包含章节信息"""
    html_content = "<!doctype lake><html><body><h1>测试</h1></body></html>"

    # 启用调试模式
    lakedoc.enable_debug()

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 检查章节标题
    assert "创建 BeautifulSoup 对象" in output
    assert "处理 HTML 内容" in output
    assert "合并相邻标签" in output
    assert "添加标题" in output


def test_debug_with_card_types():
    """测试 debug 模式下 card 类型的转换信息"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="codeblock" value="data:%7B%22mode%22%3A%22python%22%2C%22code%22%3A%22print('hello')%22%7D"></card>
    </body></html>"""

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含 card 转换信息
    assert "转换 card: type=codeblock" in output


def test_debug_with_diagram():
    """测试 debug 模式下 diagram 的转换信息"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>
    </body></html>"""

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含 diagram 转换信息
    assert "转换 card: type=diagram" in output
    assert "diagram: type=mermaid" in output


def test_debug_with_diagram_as_code():
    """测试 debug 模式下 diagram_as_code 的信息"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>
    </body></html>"""

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content, diagram_as_code=True)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含 diagram 转代码的信息
    assert "to_code=True" in output


def test_debug_with_title():
    """测试 debug 模式下标题的信息"""
    html_content = "<!doctype lake><html><body><p>测试内容</p></body></html>"

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content, title="# 自定义标题")
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含标题信息
    assert "标题: # 自定义标题" in output
    assert "添加标题: # 自定义标题" in output


def test_debug_with_file_conversion():
    """测试 debug 模式下文件转换的信息"""
    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert("tests/articles/002.html")
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含转换过程信息
    assert "[DEBUG]" in output
    assert "Markdown 转换开始" in output


def test_debug_output_structure():
    """测试 debug 输出的结构"""
    html_content = "<!doctype lake><html><body><h1>测试</h1></body></html>"

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 检查输出结构
    lines = output.split("\n")

    # 应该有章节分隔符
    has_separator = any("=" * 20 in line for line in lines)
    assert has_separator

    # 应该有子章节分隔符
    has_subsection = any("---" in line for line in lines)
    assert has_subsection


def test_debug_with_multiple_card_types():
    """测试 debug 模式下多种 card 类型的信息"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="hr" value="data:%7B%7D"></card>
    <card type="inline" name="image" value="data:%7B%22src%22%3A%22https%3A%2F%2Fexample.com%2Fimage.png%22%7D"></card>
    <card type="block" name="codeblock" value="data:%7B%22mode%22%3A%22python%22%2C%22code%22%3A%22print('hello')%22%7D"></card>
    </body></html>"""

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含多种 card 类型
    assert "转换 card: type=hr" in output
    assert "转换 card: type=image" in output
    assert "转换 card: type=codeblock" in output


def test_debug_with_list_items():
    """测试 debug 模式下列表项的信息"""
    html_content = '<!doctype lake><html><body><ul data-lake-indent="1"><li>列表项1</li></ul></body></html>'

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含列表项信息
    assert "转换列表项: indent=1" in output


def test_debug_with_style_processing():
    """测试 debug 模式下样式处理的信息"""
    html_content = (
        '<!doctype lake><html><body><p style="color:red;">红色文字</p></body></html>'
    )

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含样式处理信息
    assert "处理样式" in output or "应用颜色样式" in output


def test_debug_with_tag_removal():
    """测试 debug 模式下标签删除的信息"""
    html_content = '<!doctype lake><html><body><p>内容</p><script>alert("test")</script></body></html>'

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含标签删除信息
    assert "删除标签" in output or "script" in output


def test_debug_output_length_info():
    """测试 debug 输出包含长度信息"""
    html_content = "<!doctype lake><html><body><h1>测试</h1></body></html>"

    lakedoc.enable_debug()
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        lakedoc.convert(html_content)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
        lakedoc.disable_debug()

    # 应该包含长度信息
    assert "长度" in output or "字符" in output
