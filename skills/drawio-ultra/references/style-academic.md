# 学术风格规范（论文 / 深度学习模型架构）

适用于论文配图、审稿级示意图。目标是信息层次清楚、视觉统一、审稿人能快速读懂核心结构。产品风（业务架构/技术文章）见 `style-product.md`。

## 版式原则

- 页面 `grid="0"`，优先白色或透明背景（不用米黄色底）
- 画布建议 1400-1800 宽、900-1200 高；复杂图用 `page="0"` 自由画布
- 主模块宽度 300-420px，高度 56-72px
- 字号：主标题 28-32px，模块标题 24-26px，说明文字 18-20px（不要用 11px 小字）
- 模块间距至少 28-40px；分组容器内边距至少 40px，底/顶边留 30px 防节点越界
- 同一列内所有模块使用相同 x 坐标和相同宽度，以容器中心居中，左右内边距各 50-60px
- 并列结构（Encoder/Decoder、Backbone/Neck/Head）对齐基线和中心线
- 残差、跳连、跨模块连接走外侧，不穿过主节点
- 标题与图注放在图的**下方**（y > 最低节点底边 + 30px），符合论文图题惯例

## 样式速查

| 元素 | 样式 |
| --- | --- |
| 分组容器 | `rounded=1;arcSize=10;strokeWidth=3;fillColor=#FFFCFF;strokeColor=#B7E0FF` |
| 普通模块 | `rounded=1;arcSize=10;strokeWidth=2;fillColor=#FCF7FF;strokeColor=#666666` |
| 注意力/关键计算 | `fillColor=#EBDFF2;strokeColor=#9673A6` |
| 前馈/卷积/变换层 | `fillColor=#FFFBE6;strokeColor=#CFC286` |
| 归一化/融合 | `fillColor=#C9E9D2;strokeColor=#67AB9F` |
| 输入/嵌入 | `fillColor=#FAE2D4;strokeColor=#B89E8A` |
| 输出/预测 | `fillColor=#B7E0FF;strokeColor=#6C8EBF` |
| 说明框 | `fillColor=#FFFBE6;strokeColor=#CFC286` |
| 主连线 | `edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#000000;strokeWidth=2;endArrow=classic` |
| 残差/辅助连线 | 主连线 + `dashed=1;dashPattern=8 6;strokeColor=#666666` |

### 备用学术配色（经典教材风，背景 `#F5F5DC`）

输入/嵌入 `#F4CCCC` · 卷积/变换 `#B3D9E6` · 归一化 `#FFEB99` · 输出 `#B6D7A8` · 特殊操作 `#E6E6FA` · 拼接/融合 `#FFD966` · 参数说明框 `#FFF9E6`

## 模块 XML 示例

```xml
<mxCell id="2" value="模块名称" style="rounded=1;arcSize=10;whiteSpace=wrap;html=1;strokeWidth=2;fillColor=#FCF7FF;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="360" height="64" as="geometry"/>
</mxCell>
<mxCell id="3" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor=#000000;strokeWidth=2;endArrow=classic;" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 质量标准

- 内容准确：每个模块都能追溯到用户描述、论文结构或代码实现；不确定的结构不要凭空补全
- 层次清晰：主路径、辅助路径、重复结构一眼可分辨
- 视觉统一：同类模块同色、同尺寸、同字号，连线样式一致
- 审稿友好：字号足够大、留白充足，装饰不压过结构
- 可维护：输出未压缩 XML，便于后续在 Draw.io 中继续编辑

## 输出模板

图表说明（2-3 行）→ 核心组件 → 布局与配色 → 文件位置 → Draw.io 打开方式 → 论文图题建议与引用示例。
