"""
测试错误处理
"""

import pytest
from lakedoc.utils.errors import (
    LakeBaseError,
    LakeFileNotFoundError,
    LakeIsNotFileError,
    LakeContentTypeError,
    LakeContextError,
    LakePickNotFoundError,
    LakeSourceEmptyError,
    LakeConverterNotFoundError,
    LakeBuilderNotFoundError,
)
from pathlib import Path


def test_lake_base_error():
    """测试基础错误类"""
    error = LakeBaseError("Test error message")
    assert "Test error message" in str(error)
    assert repr(error).startswith("<LakeBaseError: 0x")


def test_lake_file_not_found_error():
    """测试文件不存在错误"""
    path = Path("/nonexistent/path/file.html")
    error = LakeFileNotFoundError(path)

    error_msg = str(error)
    assert "不存在" in error_msg
    assert "nonexistent" in error_msg


def test_lake_is_not_file_error():
    """测试路径不是文件错误"""
    path = Path("/some/directory")
    error = LakeIsNotFileError(path)

    error_msg = str(error)
    assert "并非是文件类型" in error_msg
    assert "some" in error_msg
    assert "directory" in error_msg


def test_lake_content_type_error():
    """测试内容类型错误"""
    error = LakeContentTypeError("参数 test", "str", "int")

    error_msg = str(error)
    assert "参数 test" in error_msg
    assert "str" in error_msg
    assert "int" in error_msg


def test_lake_context_error():
    """测试上下文错误"""
    error = LakeContextError("Context error")
    assert "Context error" in str(error)


def test_lake_pick_not_found_error():
    """测试转换器未找到错误"""
    error = LakePickNotFoundError("custom")

    error_msg = str(error)
    assert "custom" in error_msg
    assert "转换器" in error_msg


def test_lake_html_empty_error():
    """测试 HTML 为空错误"""
    error = LakeSourceEmptyError()

    error_msg = str(error)
    assert "不能为空" in error_msg


def test_lake_converter_not_found_error():
    """测试转换器不存在错误"""
    error = LakeConverterNotFoundError()

    error_msg = str(error)
    assert "转换器类不存在" in error_msg


def test_lake_builder_not_found_error():
    """测试构建器不存在错误"""
    error = LakeBuilderNotFoundError("lxml")

    error_msg = str(error)
    assert "lxml" in error_msg
    assert "不存在" in error_msg


def test_lake_base_error_inheritance():
    """测试错误类继承"""
    # LakeFileNotFoundError 继承自 LakeBaseError 和 FileNotFoundError
    error = LakeFileNotFoundError(Path("/test.html"))
    assert isinstance(error, LakeBaseError)
    assert isinstance(error, FileNotFoundError)

    # LakeContentTypeError 继承自 LakeBaseError 和 TypeError
    error = LakeContentTypeError("test", "str", "int")
    assert isinstance(error, LakeBaseError)
    assert isinstance(error, TypeError)


def test_convert_with_nonexistent_file():
    """测试转换不存在的文件应该抛出错误"""
    import lakedoc

    with pytest.raises(LakeFileNotFoundError):
        lakedoc.convert("/nonexistent/file.html")


def test_convert_with_empty_html():
    """测试转换空 HTML 应该抛出错误"""
    import lakedoc

    with pytest.raises(LakeSourceEmptyError):
        lakedoc.convert("   ")


def test_convert_with_invalid_target_type():
    """测试使用无效的转换器类型应该抛出错误"""
    import lakedoc

    # 需要先注册一个转换器
    html_content = "<!doctype lake><html><body><p>测试</p></body></html>"

    with pytest.raises(LakePickNotFoundError):
        lakedoc.convert(html_content, converter="nonexistent_converter")


def test_context_pick_with_invalid_type():
    """测试上下文选择无效类型应该抛出错误"""
    from lakedoc.context import LakeContext

    ctx = LakeContext()

    with pytest.raises(LakeContentTypeError):
        ctx.pick(123)  # type: ignore
