"""
测试基本的 Lake 文档转换
"""

import pytest
import lakedoc
from pathlib import Path


def test_convert_from_file():
    """测试从文件转换"""
    result = lakedoc.convert("tests/articles/001.html")
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0


def test_convert_from_html_content():
    """测试从 HTML 内容转换"""
    html_content = "<!doctype lake><h1>测试标题</h1><p>测试段落</p>"
    result = lakedoc.convert(html_content)
    assert result is not None
    assert isinstance(result, str)
    assert "测试标题" in result or "测试段落" in result


def test_convert_with_save():
    """测试转换并保存到文件"""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        result = lakedoc.convert("tests/articles/001.html", saveto=temp_path)
        assert result is not None
        assert Path(temp_path).exists()

        with open(temp_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 0
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_convert_with_save_to_directory():
    """测试转换并保存到目录（自动命名）"""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        result = lakedoc.convert("tests/articles/001.html", saveto=temp_dir)
        assert result is not None

        md_files = list(Path(temp_dir).glob("*.md"))
        assert len(md_files) == 1

        with open(md_files[0], "r", encoding="utf-8") as f:
            content = f.read()
        assert len(content) > 0
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_convert_with_title():
    """测试添加标题"""
    html_content = "<!doctype lake><p>测试内容</p>"
    result = lakedoc.convert(html_content, title="# 自定义标题")
    assert result.startswith("# 自定义标题")


def test_convert_with_encoding():
    """测试指定编码"""
    result = lakedoc.convert("tests/articles/001.html", encoding="utf-8")
    assert result is not None


def test_convert_with_bs4_builder():
    """测试指定 BeautifulSoup 解析器"""
    html_content = "<!doctype lake><p>测试内容</p>"
    result = lakedoc.convert(html_content, bs4_builder="html.parser")
    assert result is not None

    from lakedoc import errors

    with pytest.raises(errors.LakeBuilderNotFoundError):
        lakedoc.convert(html_content, bs4_builder="lxml1")


def test_convert_with_remove_tags():
    """测试删除指定标签"""
    html_content = '<!doctype lake><p>测试内容</p><script>alert("test")</script>'
    result = lakedoc.convert(html_content, remove_tags={"script"})
    assert "alert" not in result or "script" not in result.lower()


def test_convert_empty_html_raises_error():
    """测试空 HTML 内容应该抛出错误"""
    from lakedoc.utils.errors import LakeSourceEmptyError

    with pytest.raises(LakeSourceEmptyError):
        lakedoc.convert("   ")


def test_convert_nonexistent_file_raises_error():
    """测试不存在的文件应该抛出错误"""
    from lakedoc.utils.errors import LakeFileNotFoundError

    with pytest.raises(LakeFileNotFoundError):
        lakedoc.convert("tests/nonexistent.html")
