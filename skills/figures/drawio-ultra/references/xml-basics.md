# Draw.io XML 基础规范

所有模式的共用 XML 规则。生成或修改 `.drawio` XML 前读取本文件；样式配色见 `style-academic.md` / `style-product.md`。

## 标签与转义

- 每个标签必须正确闭合：`<mxCell>` 对应 `</mxCell>`，不能写成 `</mCell>`
- 节点使用 `vertex="1"`，连线使用 `edge="1"`
- 每个元素必须有唯一 `id`，根元素为 `0` 和 `1`，图形元素从 `2` 开始递增
- 连线的 `source` 和 `target` 必须指向已存在的节点 id
- 所有普通元素都有 `parent="1"`（根元素 0、1 除外）
- 特殊字符转义：`&` → `&amp;`，`<` → `&lt;`，`>` → `&gt;`，`"` → `&quot;`
- XML 注释中不能使用 `--`

## value 纯文本规则

- `mxCell` 的 `value` 默认写纯文本，换行使用 XML 实体 `&#xa;`，禁止嵌入 `<b>`、`<br>` 等 HTML 标签
- 需要强调文字时用样式字段（`fontStyle=1` 加粗、`fontStyle=2` 斜体）或拆成独立文本节点
- 样式串中的 `html=1` 仅服务于 `whiteSpace=wrap` 等布局行为；除非用户明确要求富文本并确认渲染链支持，否则不要在 value 中使用 HTML
- 生成或修改后必须检查残留：重点搜索 `<b>`、`<br>`、`&lt;b&gt;`

## 基础文件模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Page-1" id="diagram-id">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 图表内容从 id="2" 开始 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

多图文章模式：一个 `<mxfile>` 内放多个 `<diagram>`，每个 diagram 是一个 page，页面名用英文小写中划线（如 `system-overview`、`core-flow`）。

## 连线标签规则

- 短连线不放长标签：两节点距离近时 `value` 留空，或只放「是 / 否 / 成功 / 失败」等 1-2 个词
- 分类说明、原因说明、动作说明优先写进目标节点或旁注节点，不压在连线上
- 连线标签不得覆盖箭头主体，重点检查菱形节点左右出口处的标签

## 3D 节点（特征图/卷积层等立体结构）

```xml
<mxCell id="3" value="" style="shape=cube;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;darkOpacity=0.05;darkOpacity2=0.1;size=20;fillColor=#B3D9E6;strokeColor=#333333;strokeWidth=1.5" vertex="1" parent="1">
  <mxGeometry x="300" y="50" width="50" height="140" as="geometry"/>
</mxCell>
<!-- 3D 节点的文本标签独立放置于图形下方 -->
<mxCell id="3_label" value="Conv" style="text;html=1;align=center;verticalAlign=middle;fontSize=11;" vertex="1" parent="1">
  <mxGeometry x="295" y="200" width="60" height="20" as="geometry"/>
</mxCell>
```

## 网格与几何路由

- 使用共享几何布局结果对齐节点，默认网格为 20px；不要为每条边单独目测坐标
- 用计算出的边界比例写入 `entryX` / `entryY` / `exitX` / `exitY`（0-1）指定锚点
- 正交边使用 `edgeStyle=orthogonalEdgeStyle` 和中间 `mxPoint`；残差、跳连等辅助连线走障碍物外侧
- 残差、跳连等辅助连线走外侧，避免穿过主节点

## 生成后检查清单

- [ ] 所有标签闭合，无 `</mCell>` 之类笔误
- [ ] id 唯一，source/target 指向存在节点
- [ ] value 无 HTML 残留
- [ ] 节点不重叠，连线不穿过关键文字

## 常见报错

- "Not a diagram file"：检查 `<mxfile>`、`<diagram>`、`<mxGraphModel>` 嵌套关系
- "Opening and ending tag mismatch"：标签闭合错误
- 节点/连线不显示：检查 `vertex`/`edge`、`parent`、`source`/`target`
- 中文乱码：UTF-8 编码 + XML 转义
