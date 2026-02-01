"""
测试 diagram 转换为代码块
"""

import lakedoc
from pathlib import Path


def test_diagram_as_code_false_default():
    """测试默认情况下 diagram 转换为图片"""
    html_content = """<!doctype lake>
<card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>"""

    result = lakedoc.convert(html_content)
    assert result == "![图表](https://example.com/diagram.svg)"


def test_diagram_as_code_true_all():
    """测试 diagram_as_code=True 时所有 diagram 转换为代码块"""
    html_content = """<!doctype lake>
<card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5Cn%20%20%20%20%25%25%20%E5%AE%9A%E4%B9%89%E6%A0%B7%E5%BC%8F%5Cn%20%20%20%20classDef%20before%20fill%3A%23e1f3d8%2Cstroke%3A%2382c91e%2Cstroke-width%3A2px%2Ccolor%3A%23333%3B%5Cn%20%20%20%20classDef%20after%20fill%3A%23d0ebff%2Cstroke%3A%23339af0%2Cstroke-width%3A2px%2Ccolor%3A%23333%3B%5Cn%20%20%20%20classDef%20title%20font-size%3A18px%2Cfont-weight%3Abold%3B%5Cn%20%5Cnsubgraph%20After_Process%20%5BAFTER%3A%E6%B0%9B%E5%9B%B4%E5%BC%8F%E6%99%BA%E8%AF%86%E7%B3%BB%E7%BB%9F%5D%5Cn%20%20%20%20%20%20%20%20direction%20TB%5Cn%20%20%20%20%20%20%20%20A1%5B%E9%80%89%E6%8B%A9%E5%85%B4%E8%B6%A3%E6%A0%87%E7%AD%BE%20%E6%88%96%20%E8%BE%93%E5%85%A5%E4%BF%A1%E6%81%AF%5D%3A%3A%3Aafter%5Cn%20%20%20%20%20%20%20%20A2%5B%E5%A4%9A%E6%99%BA%E8%83%BD%E4%BD%93%E5%8D%8F%E4%BD%9C%E7%94%9F%E6%88%90%E2%80%9C%E6%9C%8B%E5%8F%8B%E5%9C%88%E2%80%9D%E5%BC%8F%E5%89%A7%E6%83%85%E6%B5%81%5D%3A%3A%3Aafter%5Cn%20%20%20%20%20%20%20%20A3%5B%E4%B8%8E%E5%8E%86%E5%8F%B2%E4%BA%BA%E7%89%A9%E5%9C%A8%E8%AF%84%E8%AE%BA%E5%8C%BA%E8%BE%A9%E8%AE%BA%E4%BA%92%E5%8A%A8%5D%3A%3A%3Aafter%5Cn%20%20%20%20%20%20%20%20A4%5B%E7%A9%BF%E6%88%B4%E8%AE%BE%E5%A4%87%E6%97%A0%E6%84%9F%E6%8E%A8%E9%80%81%EF%BC%8C%E5%88%A9%E7%94%A8%E7%A2%8E%E7%89%87%E6%97%B6%E9%97%B4%E2%80%9C%E5%88%B7%E2%80%9D%E7%9F%A5%E8%AF%86%5D%3A%3A%3Aafter%5Cn%20%20%20%20%20%20%20%20A5%5B%E7%B3%BB%E7%BB%9F%E8%87%AA%E5%8A%A8%E7%94%9F%E6%88%90%E6%A8%A1%E6%8B%9F%E7%9F%A5%E8%AF%86%E5%9B%BE%E8%B0%B1%2F%E5%AE%9E%E5%8A%A1%E6%96%87%E4%B9%A6%5D%3A%3A%3Aafter%5Cn%5Cn%20%20%20%20%20%20%20%20A1%20--%3E%20A2%5Cn%20%20%20%20%20%20%20%20A2%20--%3E%20A3%5Cn%20%20%20%20%20%20%20%20A3%20--%3E%20A4%5Cn%20%20%20%20%20%20%20%20A4%20--%3E%20A5%5Cn%20%20%20%20end%5Cn%5Cn%20%20%20%20subgraph%20Before_Process%20%5BBEFORE%3A%20%E4%BC%A0%E7%BB%9F%E5%AD%A6%E4%B9%A0%E4%B8%8E%E4%BF%A1%E6%81%AF%E6%A3%80%E7%B4%A2%5D%5Cn%20%20%20%20%20%20%20%20direction%20TB%5Cn%20%20%20%20%20%20%20%20B1%5B%E7%BF%BB%E9%98%85%E5%8E%9A%E9%87%8D%E4%B8%93%E4%B8%9A%E4%B9%A6%E7%B1%8D%2F%E6%9F%A5%E6%89%BE%E6%9E%AF%E7%87%A5%E6%95%B0%E6%8D%AE%5D%3A%3A%3Abefore%5Cn%20%20%20%20%20%20%20%20B2%5B%E8%A2%AB%E5%8A%A8%E6%8E%A5%E6%94%B6%E6%99%A6%E6%B6%A9%E7%9A%84%E9%95%BF%E6%96%87%E6%9C%AC%E4%B8%8E%E8%A7%86%E9%A2%91%5D%3A%3A%3Abefore%5Cn%20%20%20%20%20%20%20%20B3%5B%E7%BC%BA%E4%B9%8F%E8%AF%AD%E5%A2%83%EF%BC%8C%E7%8B%AC%E8%87%AA%E8%8B%A6%E6%80%9D%E9%80%BB%E8%BE%91%E4%B8%8E%E6%A1%88%E4%BE%8B%E5%85%B3%E8%81%94%5D%3A%3A%3Abefore%5Cn%20%20%20%20%20%20%20%20B4%5B%E7%A2%8E%E7%89%87%E6%97%B6%E9%97%B4%E9%9A%BE%E4%BB%A5%E5%88%A9%E7%94%A8%EF%BC%8C%E5%AD%A6%E4%B9%A0%E8%BF%87%E7%A8%8B%E6%9E%AF%E7%87%A5%E4%B8%AD%E6%96%AD%5D%3A%3A%3Abefore%5Cn%20%20%20%20%20%20%20%20B5%5B%E6%89%8B%E5%8A%A8%E6%95%B4%E7%90%86%E7%AC%94%E8%AE%B0%E6%88%96%E8%8A%B1%E8%B4%B9%E9%AB%98%E6%98%82%E8%B4%B9%E7%94%A8%E5%92%A8%E8%AF%A2%E8%A1%8C%E4%B8%9A%E4%B8%93%E5%AE%B6%5D%3A%3A%3Abefore%5Cn%20%20%20%20%20%20%20%20%5Cn%20%20%20%20%20%20%20%20B1%20--%3E%20B2%5Cn%20%20%20%20%20%20%20%20B2%20--%3E%20B3%5Cn%20%20%20%20%20%20%20%20B3%20--%3E%20B4%5Cn%20%20%20%20%20%20%20%20B4%20--%3E%20B5%5Cn%20%20%20%20end%5Cn%5Cn%20%20%22%2C%22url%22%3A%22https%3A%2F%2Fcdn.nlark.com%2Fyuque%2F__mermaid_v3%2F137a5ab3c42984e8e14ec5541b2af6eb.svg%22%2C%22collapse%22%3Atrue%2C%22id%22%3A%22ajDjx%22%7D"></card>"""

    result: str = lakedoc.convert(html_content, diagram_as_code=True)
    assert (
        result
        == "```mermaid\ngraph TD\n    %% 定义样式\n    classDef before fill:#e1f3d8,stroke:#82c91e,stroke-width:2px,color:#333;\n    classDef after fill:#d0ebff,stroke:#339af0,stroke-width:2px,color:#333;\n    classDef title font-size:18px,font-weight:bold;\n \nsubgraph After_Process [AFTER:氛围式智识系统]\n        direction TB\n        A1[选择兴趣标签 或 输入信息]:::after\n        A2[多智能体协作生成“朋友圈”式剧情流]:::after\n        A3[与历史人物在评论区辩论互动]:::after\n        A4[穿戴设备无感推送，利用碎片时间“刷”知识]:::after\n        A5[系统自动生成模拟知识图谱/实务文书]:::after\n\n        A1 --> A2\n        A2 --> A3\n        A3 --> A4\n        A4 --> A5\n    end\n\n    subgraph Before_Process [BEFORE: 传统学习与信息检索]\n        direction TB\n        B1[翻阅厚重专业书籍/查找枯燥数据]:::before\n        B2[被动接收晦涩的长文本与视频]:::before\n        B3[缺乏语境，独自苦思逻辑与案例关联]:::before\n        B4[碎片时间难以利用，学习过程枯燥中断]:::before\n        B5[手动整理笔记或花费高昂费用咨询行业专家]:::before\n        \n        B1 --> B2\n        B2 --> B3\n        B3 --> B4\n        B4 --> B5\n    end\n\n  \n```"
    )


def test_diagram_as_code_with_condition():
    """测试 diagram_as_code_cond 特定条件下转换"""
    html_content = """<!doctype lake><card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card><card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22sequenceDiagram%5CnAlice-%3E%3EJohn%3A%20Hello%20John%2C%20how%20are%20you%3F%5Cnloop%20HealthCheck%5Cn%20%20%20%20John-%3E%3EJohn%3A%20Fight%20against%20hypochondria%5Cnend%5CnNote%20right%20of%20John%3A%20Rational%20thoughts!%5CnJohn--%3E%3EAlice%3A%20Great!%5CnJohn-%3E%3EBob%3A%20How%20about%20you%3F%5CnBob--%3E%3EJohn%3A%20Jolly%20good!%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>"""

    result = lakedoc.convert(
        html_content,
        diagram_as_code=True,
        diagram_as_code_cond=lambda _, l, c: l == "mermaid" and "sequenceDiagram" in c,
    )

    assert (
        result
        == """![图表](https://example.com/diagram.svg)
```mermaid
sequenceDiagram
Alice->>John: Hello John, how are you?
loop HealthCheck
    John->>John: Fight against hypochondria
end
Note right of John: Rational thoughts!
John-->>Alice: Great!
John->>Bob: How about you?
Bob-->>John: Jolly good!
```"""
    )


def test_diagram_without_url_fallback_to_code():
    """测试没有 URL 的 diagram 降级为代码块"""
    html_content = """<!doctype lake><card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%7D"></card>"""

    result = lakedoc.convert(html_content)
    assert result == "```mermaid\ngraph TD\nA --> B\n```"


def test_diagram_complex_mermaid_code():
    """测试复杂的 mermaid 代码"""
    mermaid_code = """flowchart TD\nA[Christmas] -->|Get money| B(Go shopping)
B --> C{Let me think}
C -->|One| D[Laptop]
C -->|Two| E[iPhone]
C -->|Three| F[fa:fa-car Car]
"""

    import urllib.parse

    encoded_code = urllib.parse.quote(mermaid_code)

    html_content = f"""<!doctype lake><card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22{encoded_code}%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>"""

    result = lakedoc.convert(html_content, diagram_as_code=True)

    assert (
        result
        == """```mermaid
flowchart TD
A[Christmas] -->|Get money| B(Go shopping)
B --> C{Let me think}
C -->|One| D[Laptop]
C -->|Two| E[iPhone]
C -->|Three| F[fa:fa-car Car]

```"""
    )


def test_diagram_as_code_with_save():
    """测试 diagram_as_code 与保存功能结合"""
    import tempfile
    import os

    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        temp_path = f.name

    try:
        html_content = """<!doctype lake><card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>"""

        result = lakedoc.convert(html_content, saveto=temp_path, diagram_as_code=True)

        md_content = "```mermaid\ngraph TD\nA --> B\n```"
        assert result == md_content
        assert Path(temp_path).exists()

        with open(temp_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == md_content
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def test_diagram_as_code_cond_false():
    """测试 diagram_as_code_cond 返回 Flase 时不转换"""
    html_content = """<!doctype lake><card type="block" name="diagram" value="data:%7B%22type%22%3A%22mermaid%22%2C%22code%22%3A%22graph%20TD%5CnA%20--%3E%20B%22%2C%22url%22%3A%22https%3A%2F%2Fexample.com%2Fdiagram.svg%22%7D"></card>"""

    result = lakedoc.convert(
        html_content, diagram_as_code=True, diagram_as_code_cond=lambda s, l, c: False
    )
    assert result is not None
    assert "![图表]" in result or "diagram.svg" in result
