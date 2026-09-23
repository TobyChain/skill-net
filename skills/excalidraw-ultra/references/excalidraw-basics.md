# Excalidraw 基础规范

Excalidraw 引擎的文件结构、元素生成约定与默认样式。生成 `.excalidraw` 前读取本文件；图类型布局与图标库见 `excalidraw-advanced.md`，完整字段定义见 `excalidraw-schema.md`。

## 使用时机（手绘风）

- 手绘风架构图、模块依赖图、业务流程图、数据流图
- 白板讨论、头脑风暴、发散式草图
- 用户提到「Excalidraw」「手绘图」「白板图」「sketch」

专业精确坐标、UML 规范、需导出 PNG/SVG/PDF 的场景走 Draw.io 引擎（见 SKILL.md 路由）。

## 生成步骤

1. **解析输入，构建抽象模型**：抽取节点（唯一 id、名称、类型）和关系（source、target、可选 label）。
2. **运行几何布局**：使用 layout_geometry.py 计算节点矩形、边界锚点、正交折线和标签框；不要直接从中心点猜箭头坐标。
3. **生成元素**：箭头使用计算出的相对 points，并写入 startBinding / endBinding；节点的 boundElements 同步记录箭头。
4. **校验 JSON 和几何结果**：语法、id、节点/标签不重叠，且箭头不穿过无关节点。

## 文件结构

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": 20 },
  "files": {}
}
```

## 元素约定

- **节点**：`rectangle` 或 `round rectangle` 图形 + 独立 `text` 文本元素（文本大致居中叠加在矩形上）；决策点用 `diamond`
- **所有 text 元素必须 `fontFamily: 5`（Excalifont）**，保证视觉一致
- **连线**：`arrow` 元素，points 从几何计算结果转换为相对坐标；主流程用较粗黑色箭头，辅助关系用细线或浅色；可加短 text 标注含义（「调用」「写入」）
- **分组**：用 `groupIds` 把同一子系统的节点归组，方便用户整体移动

## 默认配色（若用户未指定）

| 用途 | 样式 |
| --- | --- |
| 输入/输出节点 | 白底黑框：`backgroundColor: "transparent"`，`strokeColor: "#1e1e1e"` |
| 计算模块/中间层 | 浅色背景黑描边（如 `#f5f5ff`），同类模块颜色一致 |
| 分组大框 | 圆角矩形白底黑框，框内顶部 text 标注标题 |
| 主色板（复杂图） | 主元素 `#a5d8ff`，次要 `#b2f2bb`，中心/重要 `#ffd43b`，告警 `#ffc9c9` |

## 版式

- 元素水平间距 200-300px，行间距 100-150px
- 文字字号 16-24px
- 单图元素建议 ≤ 20；过多时主动聚合分组（多个内部模块归为一个「子系统」节点）或拆成多张图

## 输出格式

严格分两部分：

1. **图表说明**：中文说明层次结构、节点含义、主要连线关系（1-2 段）；如有补充或抽象假设在此说明
2. **Excalidraw JSON**：完整可直接保存为 `.excalidraw` 的 JSON，仅输出 JSON 本身，不加注释或代码块标记

## 校验清单

- [ ] 所有元素 id 唯一
- [ ] 节点和标签矩形不重叠
- [ ] 箭头起止点落在节点边界，且 startBinding / endBinding 正确
- [ ] 折线路由不穿过无关节点
- [ ] 文字可读（字号 ≥16，全部 fontFamily=5）
- [ ] 箭头方向符合数据流/调用方向
- [ ] 颜色遵循统一方案
- [ ] JSON 语法正确、无多余逗号

## 打开方式

访问 https://excalidraw.com → Open / 拖拽文件；或使用 Excalidraw VS Code / Obsidian 插件。Excalidraw 导出的 SVG/PNG 可再导入 Draw.io（反向不适用）。
