## 议题

**简述：**

在处理 diagram 类型的卡片时，当卡片数据中缺少 URL 信息时，当前的转换逻辑会直接显示错误信息。这可能导致用户无法看到 diagram 卡片中的实际内容。

**提出者：**[pingban404](https://github.com/pingban404)

**链接：**https://github.com/gupingan/lakedoc/issues/1#issue-3009638889

**当前版本：**`1.0.4`



## 需求

当 `diagram` 卡片缺少 `url` 字段时，原逻辑无法展示有效内容，这会影响内容可读性



## 实现

**当前版本：**`1.0.5`

```python
if card_type == 'diagram':
    card_data = decode_card_value(el.attrs.get('value', ''))
    src = card_data.get('url', '')
    if src:
        return f'![图表]({src})\n'  # 保留图片渲染
    
    # 降级处理，无 URL 时展示代码块
    code_type = card_data.get('type', 'plaintext')  # 默认类型
    code_data = card_data.get('code', '')
    return f'\n```{code_type}\n{code_data}\n```\n'
```



## 状态

✅ 已修复

