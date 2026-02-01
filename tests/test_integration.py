"""
集成测试 - 测试完整的转换流程
"""

import pytest
import lakedoc
from lakedoc.context.mod import register
from pathlib import Path
import os


def test_full_conversion_workflow():
    """测试完整的转换工作流"""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        # 1. 从文件转换
        result1 = lakedoc.convert("tests/articles/001.html")
        assert result1 is not None
        assert len(result1) > 0

        # 2. 转换并保存到文件
        output_file = os.path.join(temp_dir, "output.md")
        result2 = lakedoc.convert("tests/articles/001.html", saveto=output_file)
        assert result2 is not None
        assert Path(output_file).exists()

        # 3. 读取保存的文件
        with open(output_file, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert len(saved_content) > 0

        # 4. 从 HTML 内容转换
        html_content = (
            "<!doctype lake><html><body><h1>集成测试</h1><p>测试内容</p></body></html>"
        )
        result3 = lakedoc.convert(html_content)
        assert result3 is not None
        assert "集成测试" in result3

        # 5. 带标题转换
        result4 = lakedoc.convert(html_content, title="# 集成测试标题")
        assert "# 集成测试标题" in result4

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_multiple_conversions_with_options():
    """测试多次转换使用不同选项"""
    html_content = "<!doctype lake><html><body><h1>测试</h1><p>内容</p></body></html>"

    # 转换 1: 默认选项
    result1 = lakedoc.convert(html_content)
    assert result1 is not None

    # 转换 2: 带标题
    result2 = lakedoc.convert(html_content, title="# 测试标题")
    assert "# 测试标题" in result2

    # 转换 3: 带自定义删除标签
    result3 = lakedoc.convert(
        '<!doctype lake><html><body><p>内容</p><script>alert("test")</script></body></html>',
        remove_tags={"script"},
    )
    assert "alert" not in result3 or "script" not in result3.lower()


def test_diagram_conversion_workflow():
    """测试 diagram 转换工作流"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>
    </body></html>"""

    # 1. 默认转换为图片
    result1 = lakedoc.convert(html_content)
    assert "![图表]" in result1 or "diagram.svg" in result1

    # 2. 转换为代码块
    result2 = lakedoc.convert(html_content, diagram_as_code=True)
    assert "```mermaid" in result2 or "```" in result2

    # 3. 转换特定类型
    result3 = lakedoc.convert(
        html_content,
        diagram_as_code=True,
        diagram_as_code_cond=lambda s, l, c: l == "mermaid",
    )
    assert "```mermaid" in result3 or "```" in result3


def test_context_switching():
    """测试上下文切换"""
    from lakedoc.context import get_context, set_context, LakeContext
    from lakedoc.converters import MarkdownConverter

    # 获取默认上下文
    ctx1 = get_context()
    assert ctx1 is not None

    # 创建新上下文
    ctx2 = LakeContext()
    ctx2.register("markdown", MarkdownConverter)
    set_context(ctx2)

    # 验证上下文已切换
    assert get_context() is ctx2

    # 使用新上下文转换
    html_content = "<!doctype lake><html><body><h1>测试</h1></body></html>"
    result = lakedoc.convert(html_content)
    assert result is not None

    # 恢复默认上下文
    set_context(ctx1)
    assert get_context() is ctx1


def test_converter_registration_workflow():
    """测试转换器注册工作流"""
    from lakedoc.context import LakeContext

    # 创建自定义转换器
    class CustomConverter:
        def __init__(self, raw_html, **options):
            self.raw_html = raw_html
            self.options = options

        def convert(self):
            return f"Custom: {self.raw_html[:50]}"

    # 创建上下文并注册转换器
    ctx = LakeContext()
    ctx.register("custom", CustomConverter)

    # 验证转换器已注册
    assert "custom" in ctx.converter_classes

    # 使用自定义转换器
    html_content = "<!doctype lake><html><body><p>测试内容</p></body></html>"
    result = ctx.convert_content(html_content, "custom")
    assert "Custom:" in result


def test_error_handling_workflow():
    """测试错误处理工作流"""
    # 1. 测试文件不存在错误
    from lakedoc.utils.errors import LakeFileNotFoundError

    with pytest.raises(LakeFileNotFoundError):
        lakedoc.convert("/nonexistent/file.html")

    # 2. 测试空 HTML 错误
    from lakedoc.utils.errors import LakeSourceEmptyError

    with pytest.raises(LakeSourceEmptyError):
        lakedoc.convert("   ")

    # 3. 测试转换器不存在错误
    from lakedoc.utils.errors import LakePickNotFoundError

    html_content = "<!doctype lake><html><body><p>测试</p></body></html>"
    with pytest.raises(LakePickNotFoundError):
        lakedoc.convert(html_content, converter="nonexistent")


def test_large_file_conversion():
    """测试大文件转换"""
    # 使用示例文件
    result = lakedoc.convert("tests/articles/001.html")
    assert result is not None
    assert len(result) > 1000  # 应该有足够的内容


def test_special_characters_conversion():
    """测试特殊字符转换"""
    html_content = """<!doctype lake><html><body>
    <p>测试特殊字符：< > & " '</p>
    <p>中文测试：你好世界</p>
    <p>Emoji测试：😀 🎉 🚀</p>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "你好世界" in result


def test_nested_elements_conversion():
    """测试嵌套元素转换"""
    html_content = """<!doctype lake><html><body>
    <div>
        <p>外层段落</p>
        <ul>
            <li>列表项1</li>
            <li>列表项2</li>
        </ul>
    </div>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "列表项1" in result or "列表项2" in result


def test_multiple_diagram_types():
    """测试多种 diagram 类型"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fmermaid.svg%22%7D"></card>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22plantuml%22%2C%22code%22%3A%22A%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fplantuml.svg%22%7D"></card>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22sequence%22%2C%22code%22%3A%22A%20-%3E%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fsequence.svg%22%7D"></card>
    </body></html>"""

    # 转换所有类型
    result = lakedoc.convert(html_content, diagram_as_code=True)
    assert result is not None
    # 应该包含多种 diagram 类型的代码块
    assert "```" in result


def test_save_to_directory_workflow():
    """测试保存到目录工作流"""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        # 转换并保存到目录（自动命名）
        result = lakedoc.convert("tests/articles/001.html", saveto=temp_dir)
        assert result is not None

        # 查找生成的文件
        md_files = list(Path(temp_dir).glob("*.md"))
        assert len(md_files) >= 1

        # 验证文件内容
        for md_file in md_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            assert len(content) > 0
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
