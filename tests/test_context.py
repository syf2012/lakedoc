"""
测试上下文管理
"""

import pytest
from pathlib import Path
from lakedoc.context import LakeContext, get_context, set_context
from lakedoc.converters import MarkdownConverter


def test_get_context_singleton():
    """测试获取上下文是单例模式"""
    ctx1 = get_context()
    ctx2 = get_context()
    assert ctx1 is ctx2


def test_set_context():
    """测试设置上下文"""
    # 保存原始上下文
    original_context = get_context()

    # 创建新上下文
    new_context = LakeContext()
    set_context(new_context)

    # 验证上下文已更改
    assert get_context() is new_context

    # 恢复原始上下文
    set_context(original_context)


def test_context_register_converter():
    """测试注册转换器"""
    ctx = LakeContext()

    # 定义一个自定义转换器
    class CustomConverter:
        def __init__(self, raw_html, **options):
            self.raw_html = raw_html
            self.options = options

        def convert(self):
            return "Custom output"

    # 注册转换器
    ctx.register("custom", CustomConverter)

    # 验证转换器已注册
    assert "custom" in ctx.converter_classes
    assert ctx.converter_classes["custom"] is CustomConverter


def test_context_register_converter_with_cover():
    """测试覆盖已注册的转换器"""
    ctx = LakeContext()

    class Converter1:
        def __init__(self, raw_html, **options):
            pass

        def convert(self):
            return "Converter1"

    class Converter2:
        def __init__(self, raw_html, **options):
            pass

        def convert(self):
            return "Converter2"

    # 注册第一个转换器
    ctx.register("test", Converter1)
    assert ctx.converter_classes["test"] is Converter1

    # 用 is_cover=True 覆盖
    ctx.register("test", Converter2, is_cover=True)
    assert ctx.converter_classes["test"] is Converter2

    # 注册一个名称是错误类型的转换器
    from lakedoc import errors

    with pytest.raises(errors.LakeContentTypeError):
        ctx.register(1, Converter2)  # type: ignore


def test_context_register_converter_without_cover():
    """测试不覆盖已注册的转换器"""
    ctx = LakeContext()

    class Converter1:
        def __init__(self, raw_html, **options):
            pass

        def convert(self):
            return "Converter1"

    class Converter2:
        def __init__(self, raw_html, **options):
            pass

        def convert(self):
            return "Converter2"

    # 注册第一个转换器
    ctx.register("test", Converter1)
    assert ctx.converter_classes["test"] is Converter1

    # 用 is_cover=False 不覆盖
    ctx.register("test", Converter2, is_cover=False)
    # 应该保持为第一个转换器
    assert ctx.converter_classes["test"] is Converter1


def test_context_pick_converter():
    """测试选择转换器"""
    ctx = LakeContext()

    class TestConverter:
        def __init__(self, raw_html, **options):
            pass

        def convert(self):
            return "Test output"

    # 注册转换器
    ctx.register("test", TestConverter)

    # 选择转换器
    ctx.pick("test")

    # 验证转换器已选择
    assert ctx.converter_class is TestConverter


def test_context_pick_nonexistent_converter_raises_error():
    """测试选择不存在的转换器应该抛出错误"""
    from lakedoc.utils.errors import LakePickNotFoundError

    ctx = LakeContext()

    with pytest.raises(LakePickNotFoundError):
        ctx.pick("nonexistent")


def test_context_pick_invalid_type_raises_error():
    """测试选择无效类型的转换器应该抛出错误"""
    from lakedoc.utils.errors import LakeContentTypeError

    ctx = LakeContext()

    with pytest.raises(LakeContentTypeError):
        ctx.pick(123)  # type: ignore


def test_context_set_options():
    """测试设置选项"""
    ctx = LakeContext()

    options = {
        "title": "# Test Title",
        "bs4_builder": "html.parser",
        "remove_tags": {"script", "style"},
    }

    ctx.set_options(**options)

    # 验证选项已设置
    assert ctx.options == options


def test_context_convert_content():
    """测试转换 HTML 内容"""
    ctx = LakeContext()
    ctx.register("markdown", MarkdownConverter)

    html_content = "<!doctype lake><html><body><h1>测试标题</h1></body></html>"
    result = ctx.convert_content(html_content, "markdown")

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_context_convert_empty_content_raises_error():
    """测试转换空内容应该抛出错误"""
    from lakedoc.utils.errors import LakeSourceEmptyError

    ctx = LakeContext()
    ctx.register("markdown", MarkdownConverter)

    with pytest.raises(LakeSourceEmptyError):
        ctx.convert_content("   ", "markdown")


def test_context_convert_file():
    """测试转换文件"""
    ctx = LakeContext()
    ctx.register("markdown", MarkdownConverter)

    result = ctx.convert_file("tests/articles/001.html", "markdown")

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_context_convert_file_save():
    """测试转换文件并保存"""
    import tempfile
    import os

    ctx = LakeContext()
    ctx.register("markdown", MarkdownConverter)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        result = ctx.convert_file_save("tests/articles/001.html", temp_path, "markdown")

        assert result is not None
        assert Path(temp_path).exists()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_context_convert_content_save():
    """测试转换内容并保存"""
    import tempfile
    import os

    ctx = LakeContext()
    ctx.register("markdown", MarkdownConverter)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        html_content = "<!doctype lake><html><body><h1>测试标题</h1></body></html>"
        result = ctx.convert_content_save(html_content, temp_path, "markdown")

        assert result is not None
        assert Path(temp_path).exists()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
