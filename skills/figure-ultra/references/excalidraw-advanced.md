# Excalidraw 进阶：图类型、模板与图标库

图类型选择路由、现成模板和图标库工作流。基础文件结构见 `excalidraw-basics.md`，元素字段定义见 `excalidraw-element-types.md`。

## 图类型路由

| 用户意图 | 图类型 | 关键词 |
| --- | --- | --- |
| 流程、步骤、过程 | 流程图 | workflow / process / steps |
| 连接、依赖、关联 | 关系图 | relationship / connections / dependencies |
| 概念层级、头脑风暴 | 思维导图 | mind map / concepts / breakdown |
| 系统设计、组件 | 架构图 | architecture / system / modules |
| 数据流转、变换 | 数据流图（DFD） | data flow / transformation；只表达数据流不表达顺序 |
| 跨职能流程、角色分工 | 泳道图 | swimlane / actors；角色为列，流程在泳道内 |
| 面向对象设计 | 类图 | class / inheritance；可见性 +、-、#，六种关系线型 |
| 交互时序、消息流 | 时序图 | sequence / messages；生命线 + 激活条 |
| 数据库实体 | ER 图 | entity / data model；PK 下划线、FK 标注、基数 1:1/1:N/N:M |

## 现成模板（templates/）

同类型图从模板起步，替换文本和坐标比从零拼 JSON 更可靠：

| 模板文件 | 用途 |
| --- | --- |
| `flowchart-template.excalidraw` | 流程图骨架 |
| `relationship-template.excalidraw` | 关系图骨架 |
| `mindmap-template.excalidraw` | 思维导图骨架 |
| `architecture` → 用 `relationship` 或 `flowchart` 组合 | 系统架构 |
| `data-flow-diagram-template.excalidraw` | DFD |
| `business-flow-swimlane-template.excalidraw` | 泳道图 |
| `class-diagram-template.excalidraw` | 类图 |
| `sequence-diagram-template.excalidraw` | 时序图 |
| `er-diagram-template.excalidraw` | ER 图 |

## 元素数量控制

| 图类型 | 建议 | 上限 |
| --- | --- | --- |
| 流程图步骤 | 3-10 | 15 |
| 关系图实体 | 3-8 | 12 |
| 思维导图分支 | 4-6 | 8（每支子题 2-4） |

超出时先给高层图（主组件），再为子系统出详细图，询问用户从哪张开始。

## 布局算法（内部估算用）

- 网格布局（关系图）：`columns = ceil(sqrt(n))`，`x = startX + (i % columns) * 水平间距`，`y = startY + floor(i / columns) * 垂直间距`
- 放射布局（思维导图）：`angle = 2π * i / branchCount`，`x = cx + r * cos(angle)`
- id 生成：时间戳36进制 + 随机串，保证唯一

## 图标库（AWS/GCP/K8s 等专业图标）

图标库未安装时：用基础形状 + 颜色编码 + 文字标签生成，告知用户可后补图标。用户想装图标库时给出步骤：

1. 到 https://libraries.excalidraw.com/ 下载 `.excalidrawlib` 文件
2. 放入本技能 `libraries/<图标集名>/` 目录
3. 运行拆分脚本生成 `reference.md` 与 `icons/` 独立文件：
   ```bash
   python scripts/split-excalidraw-library.py libraries/<图标集名>/
   ```

图标库已安装时（`libraries/` 下存在 `reference.md`），**优先用脚本操作，避免把图标 JSON 读进上下文**：

```bash
# 向图添加图标（自动处理坐标变换、UUID、防覆盖 .excalidraw.edit）
python scripts/add-icon-to-diagram.py <图路径> <图标名> <x> <y> --label "Web Server"

# 添加连线箭头
python scripts/add-arrow.py <图路径> <x1> <y1> <x2> <y2> --label "HTTPS" --style dashed --color "#7950f2"
```

脚本优势：图标 JSON（每个 200-1000 行）不进上下文、坐标变换确定性、自动 id 管理。脚本细节见 [icon-tools.md](icon-tools.md)。

## 常见问题

| 问题 | 解法 |
| --- | --- |
| 元素重叠 | 拉大坐标间距 |
| 文字放不下盒子 | 加宽盒子或缩小字号（≥16） |
| 元素太多 | 拆成多张图 |
| 布局混乱 | 网格布局或放射布局 |
| 颜色不统一 | 先定色板再生成 |
