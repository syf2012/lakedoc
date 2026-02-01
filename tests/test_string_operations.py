"""
测试字符串操作
"""

import pytest
from lakedoc.utils import string
import json
import urllib.parse


def test_extract_integer_simple():
    """测试提取简单整数"""
    assert string.extract_integer("11em") == 11
    assert string.extract_integer("2px") == 2
    assert string.extract_integer("100%") == 100


def test_extract_integer_complex():
    """测试提取复杂整数"""
    assert string.extract_integer("1.5em") == 15
    assert string.extract_integer("2.3px") == 23
    assert string.extract_integer("10.5rem") == 105


def test_extract_integer_no_digits():
    """测试没有数字的字符串"""
    assert string.extract_integer("test") == 0
    assert string.extract_integer("abc") == 0
    assert string.extract_integer("") == 0


def test_extract_integer_with_default():
    """测试使用默认值"""
    assert string.extract_integer("test", default_=10) == 10
    assert string.extract_integer("abc", default_=99) == 99


def test_extract_integer_multiple_digits():
    """测试提取多个数字"""
    assert string.extract_integer("test123abc") == 123
    assert string.extract_integer("abc456def") == 456
    assert string.extract_integer("123test456") == 123456


def test_extract_integer_edge_cases():
    """测试边界情况"""
    assert string.extract_integer("0") == 0
    assert string.extract_integer("000") == 0
    assert string.extract_integer("999999") == 999999


def test_color_string_red():
    """测试红色字符串"""
    result = string.color_string("Test", color="red")
    assert "Test" in result


def test_color_string_green():
    """测试绿色字符串"""
    result = string.color_string("Test", color="green")
    assert "Test" in result


def test_color_string_blue():
    """测试蓝色字符串"""
    result = string.color_string("Test", color="blue")
    assert "Test" in result


def test_color_string_yellow():
    """测试黄色字符串"""
    result = string.color_string("Test", color="yellow")
    assert "Test" in result


def test_color_string_default():
    """测试默认颜色字符串"""
    result = string.color_string("Test")
    assert "Test" in result


def test_color_string_invalid_color():
    """测试无效颜色"""
    result = string.color_string("Test", color="invalid")
    assert "Test" in result


def test_color_string_chinese():
    """测试中文字符串"""
    result = string.color_string("测试", color="red")
    assert "测试" in result


def test_color_string_empty():
    """测试空字符串"""
    result = string.color_string("", color="red")
    assert result is not None


def test_decode_card_value_simple():
    """测试解码简单的 card 值"""
    test_data = {"type": "mermaid", "code": "graph TD\nA --> B"}
    json_str = json.dumps(test_data)
    encoded = urllib.parse.quote(json_str)
    card_value = f"data:{encoded}"

    result = string.decode_card_value(card_value)
    assert result == test_data


def test_decode_card_value_complex():
    """测试解码复杂的 card 值"""
    test_data = {
        "type": "mermaid",
        "code": "graph TD\nA --> B",
        "url": "https://example.com/diagram.svg",
        "id": "test123",
    }
    json_str = json.dumps(test_data)
    encoded = urllib.parse.quote(json_str)
    card_value = f"data:{encoded}"

    result = string.decode_card_value(card_value)
    assert result == test_data


def test_decode_card_value_chinese():
    """测试解码包含中文的 card 值"""
    test_data = {"type": "mermaid", "code": "graph TD\n测试节点A --> 测试节点B"}
    json_str = json.dumps(test_data, ensure_ascii=False)
    encoded = urllib.parse.quote(json_str)
    card_value = f"data:{encoded}"

    result = string.decode_card_value(card_value)
    assert result == test_data


def test_decode_card_value_special_characters():
    """测试解码包含特殊字符的 card 值"""
    test_data = {"type": "mermaid", "code": "graph TD\nA --> B\nC --> D"}
    json_str = json.dumps(test_data)
    encoded = urllib.parse.quote(json_str)
    card_value = f"data:{encoded}"

    result = string.decode_card_value(card_value)
    assert result == test_data


def test_decode_card_value_empty():
    """测试解码空的 card 值"""
    test_data = {}
    json_str = json.dumps(test_data)
    encoded = urllib.parse.quote(json_str)
    card_value = f"data:{encoded}"

    result = string.decode_card_value(card_value)
    assert result == test_data


def test_encode_card_value_simple():
    """测试编码简单的 card 值"""
    test_data = {"type": "mermaid", "code": "graph TD\nA --> B"}

    result = string.encode_card_value(test_data)
    assert result.startswith("data:")

    # 验证可以解码
    decoded = string.decode_card_value(result)
    assert decoded == test_data


def test_encode_card_value_complex():
    """测试编码复杂的 card 值"""
    test_data = {
        "type": "mermaid",
        "code": "graph TD\nA --> B",
        "url": "https://example.com/diagram.svg",
        "id": "test123",
    }

    result = string.encode_card_value(test_data)
    assert result.startswith("data:")

    # 验证可以解码
    decoded = string.decode_card_value(result)
    assert decoded == test_data


def test_encode_card_value_chinese():
    """测试编码包含中文的 card 值"""
    test_data = {"type": "mermaid", "code": "graph TD\n测试节点A --> 测试节点B"}

    result = string.encode_card_value(test_data)
    assert result.startswith("data:")

    # 验证可以解码
    decoded = string.decode_card_value(result)
    assert decoded == test_data


def test_encode_decode_roundtrip():
    """测试编码解码往返"""
    original_data = {
        "type": "mermaid",
        "code": "graph TD\nA --> B\nC --> D",
        "url": "https://example.com/diagram.svg",
        "id": "test123",
        "nested": {"key1": "value1", "key2": "value2"},
    }

    # 编码
    encoded = string.encode_card_value(original_data)

    # 解码
    decoded = string.decode_card_value(encoded)

    # 验证往返一致
    assert decoded == original_data


def test_encode_card_value_empty():
    """测试编码空的 card 值"""
    test_data = {}

    result = string.encode_card_value(test_data)
    assert result.startswith("data:")

    # 验证可以解码
    decoded = string.decode_card_value(result)
    assert decoded == test_data


def test_decode_card_value_invalid_json():
    """测试解码无效的 JSON"""
    invalid_card_value = "data:invalid_json"

    # 应该抛出 JSON 解析错误
    with pytest.raises(json.JSONDecodeError):
        string.decode_card_value(invalid_card_value)


def test_decode_card_value_missing_prefix():
    """测试解码缺少前缀的 card 值"""
    # 没有前缀应该抛出错误
    test_data = {"type": "mermaid", "code": "graph TD\nA --> B"}
    json_str = json.dumps(test_data)
    encoded = urllib.parse.quote(json_str)

    # 直接使用编码的字符串（没有 data: 前缀）应该抛出错误
    with pytest.raises(json.JSONDecodeError):
        string.decode_card_value(encoded[5:])  # 跳过 'data:'
