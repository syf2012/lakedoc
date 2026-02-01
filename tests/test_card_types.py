"""
测试各种 card 类型的转换
"""

import lakedoc


def test_card_image():
    """测试 image card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="inline" name="image" value="data:%7B%22src%22%3A%22https%3A%2F%2Fexample.com%2Fimage.png%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    print(result)
    assert result is not None
    assert "![图片未加载](https://example.com/image.png)" in result


def test_card_hr():
    """测试 hr card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="hr" value="data:%7B%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "---" in result


def test_card_table():
    """测试 table card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="table" value="data:%7B%22html%22%3A%22%3Ctable%3E%3Ctr%3E%3Ctd%3Etest%3C%2Ftd%3E%3C%2Ftr%3E%3C%2Ftable%3E%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "table" in result.lower()


def test_card_codeblock():
    """测试 codeblock card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="codeblock" value="data:%7B%22mode%22%3A%22python%22%2C%22code%22%3A%22print('hello')%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "```python" in result or "```" in result
    assert "print('hello')" in result


def test_card_math():
    """测试 math card 转换"""
    html_content = """<!doctype lake><html><body>
    <p style="text-align: center">
    <card type="inline" name="math" value="data:%7B%22code%22%3A%22E%20%3D%20mc%5E2%22%7D"></card>
    </p>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "$$" in result


def test_card_yuqueinline():
    """测试 yuqueinline card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="inline" name="yuqueinline" value="data:%7B%22src%22%3A%22https%3A%2F%2Fyuque.com%2Ftest%22%2C%22detail%22%3A%7B%22title%22%3A%22测试文档%22%2C%22type%22%3A%22doc%22%7D%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "测试文档" in result or "yuque.com" in result


def test_card_bookmark_inline():
    """测试 bookmarkInline card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="inline" name="bookmarkInline" value="data:%7B%22src%22%3A%22https%3A%2F%2Fexample.com%22%2C%22detail%22%3A%7B%22title%22%3A%22测试书签%22%7D%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "测试书签" in result or "example.com" in result


def test_card_localdoc():
    """测试 localdoc card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="localdoc" value="data:%7B%22src%22%3A%22test.pdf%22%2C%22name%22%3A%22测试文件%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "测试文件" in result or "test.pdf" in result


def test_card_image_gallery():
    """测试 imageGallery card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="imageGallery" value="data:%7B%22imageList%22%3A%5B%7B%22src%22%3A%22https%3A%2F%2Fexample.com%2Fimage1.png%22%2C%22title%22%3A%22图片1%22%2C%22original%22%3A%7B%22width%22%3A100%7D%7D%2C%7B%22src%22%3A%22https%3A%2F%2Fexample.com%2Fimage2.png%22%2C%22title%22%3A%22图片2%22%2C%22original%22%3A%7B%22width%22%3A100%7D%7D%5D%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "图片" in result or "image" in result.lower()


def test_card_flowchart2():
    """测试 flowchart2 card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="inline" name="flowchart2" value="data:%7B%22src%22%3A%22https%3A%2F%2Fexample.com%2Fflowchart.svg%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "![" in result or "flowchart" in result.lower()


def test_card_board():
    """测试 board card 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="inline" name="board" value="data:%7B%22src%22%3A%22https%3A%2F%2Fexample.com%2Fboard.png%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "![" in result or "board" in result.lower()


def test_card_diagram_with_url():
    """测试 diagram card 带 URL 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    # 默认情况下应该显示图片
    assert "![图表]" in result or "diagram.svg" in result


def test_card_diagram_without_url():
    """测试 diagram card 不带 URL 转换"""
    html_content = """<!doctype lake><html><body>
    <card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%7D"></card>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    # 没有 URL 时应该显示代码块
    assert "```mermaid" in result or "```" in result


def test_card_math_inline():
    """测试内联 math card 转换"""
    html_content = """<!doctype lake><html><body>
    <p>
    <card type="inline" name="math" value="data:%7B%22code%22%3A%22E%20%3D%20mc%5E2%22%7D"></card>
    </p>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    assert "$$" in result


def test_card_math_block():
    """测试块级 math card 转换"""
    html_content = """<!doctype lake><html><body>
    <p style="text-align: center">
    <card type="inline" name="math" value="data:%7B%22code%22%3A%22E%20%3D%20mc%5E2%22%7D"></card>
    </p>
    </body></html>"""

    result = lakedoc.convert(html_content)
    assert result is not None
    # 居中的数学公式应该有换行
    assert "$$" in result
