"""
测试文件操作
"""

import pytest
from lakedoc.utils import file
from pathlib import Path
import os


def test_readfile():
    """测试读取文件"""
    # 读取测试文件
    content = file.readfile("tests/articles/001.html")
    assert content is not None
    assert isinstance(content, str)
    assert len(content) > 0
    assert "<!doctype lake>" in content.lower()


def test_readfile_with_encoding():
    """测试使用指定编码读取文件"""
    content = file.readfile("tests/articles/001.html", encoding="utf-8")
    assert content is not None
    assert isinstance(content, str)


def test_readfile_nonexistent_raises_error():
    """测试读取不存在的文件应该抛出错误"""
    from lakedoc.utils.errors import LakeFileNotFoundError

    with pytest.raises(LakeFileNotFoundError):
        file.readfile("/nonexistent/file.html")


def test_readfile_directory_raises_error():
    """测试读取目录应该抛出错误"""
    from lakedoc.utils.errors import LakeIsNotFileError

    with pytest.raises(LakeIsNotFileError):
        file.readfile("tests/articles")


def test_savefile_to_file():
    """测试保存到文件"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        content = "# 测试内容\n\n这是一个测试文件。"
        file.savefile(content, temp_path)

        # 验证文件已创建
        assert Path(temp_path).exists()

        # 验证文件内容
        with open(temp_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == content
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_to_directory():
    """测试保存到目录（自动命名）"""
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        content = "# 测试内容"
        file.savefile(content, temp_dir)

        # 查找生成的文件
        md_files = list(Path(temp_dir).glob("*.md"))
        assert len(md_files) == 1

        # 验证文件内容
        with open(md_files[0], "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == content
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_savefile_with_suffix():
    """测试指定文件后缀"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        temp_path = f.name

    try:
        content = "测试内容"
        file.savefile(content, temp_path, suffix=".txt")

        # 验证文件已创建
        assert Path(temp_path).exists()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_with_encoding():
    """测试指定编码"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        content = "# 测试内容\n中文测试"
        file.savefile(content, temp_path, encoding="utf-8")

        # 验证文件内容
        with open(temp_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == content
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_bytes():
    """测试保存字节内容"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="wb", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        content = "# 测试内容".encode()
        file.savefile(content, temp_path)

        # 验证文件已创建
        assert Path(temp_path).exists()

        # 验证文件内容
        with open(temp_path, "rb") as f:
            saved_content = f.read()
        assert saved_content == content
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_invalid_type_raises_error():
    """测试保存无效类型应该抛出错误"""
    from lakedoc.utils.errors import LakeContentTypeError
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        content = 12345  # 无效类型

        with pytest.raises(LakeContentTypeError):
            file.savefile(content, temp_path)  # type: ignore
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_overwrite():
    """测试覆盖已存在的文件"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        # 第一次保存
        content1 = "# 原始内容"
        file.savefile(content1, temp_path)

        # 第二次保存（覆盖）
        content2 = "# 新内容"
        file.savefile(content2, temp_path)

        # 验证文件内容是新的
        with open(temp_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == content2
        assert saved_content != content1
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_empty_content():
    """测试保存空内容"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        content = ""
        file.savefile(content, temp_path)

        # 验证文件已创建
        assert Path(temp_path).exists()

        # 验证文件内容为空
        with open(temp_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == ""
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_large_content():
    """测试保存大内容"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        content = "# 大内容测试\n" + "\n".join(["行内容"] * 10000)
        file.savefile(content, temp_path)

        with open(temp_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == content
        assert len(saved_content) > 10000
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_savefile_special_characters():
    """测试保存特殊字符"""
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        content = "# 特殊字符测试\n\n<>&\"'\\n中文：你好世界\nEmoji：😀🎉"
        file.savefile(content, temp_path)

        # 验证文件内容
        with open(temp_path, "r", encoding="utf-8") as f:
            saved_content = f.read()
        assert saved_content == content
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
