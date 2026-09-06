# ultra-skills

Ultra 系列 Agent Skills，用于 Qoder / Claude Code / 兼容 SKILL.md 规范的 Agent 平台。技能遵循「主文件做路由，细节按需加载」的渐进式披露设计，避免把全部规范塞进上下文。

## 技能列表

| 技能 | 用途 | 输出 |
| --- | --- | --- |
| [`prompt-ultra`](skills/prompt-ultra) | 建立当前任务契约，并把明确要求长期保留的约定迁移到原生持久指令文件 | Work Contract / Persistent Work Instructions |
| [`learn-ultra`](skills/learn-ultra) | 把仓库、论文、文章或多来源资料重构成可学习、可练习、可验证的中文教材 | 教材式单文件 HTML / 学习路径 / 例题与练习 |
| [`figure-ultra`](skills/figure-ultra) | 通用可视化与图片交付，三引擎自动路由 | `.drawio` / `.excalidraw` / PNG / SVG / PDF |
| [`tikz-ultra`](skills/tikz-ultra) | LaTeX 原生、源码可复现的 TikZ/PGF 绘图工作流 | `.tex` / PDF / PNG / SVG |
| [`paper-ultra`](skills/paper-ultra) | 修改、翻译与审阅论文，同时保护证据和贡献边界 | 修订稿 / 审阅意见 / 双语同步文本 |

---

## prompt-ultra

复杂任务的工作契约与持久规范技能。它既能在当前任务中澄清目标、权限和验收标准，也能把用户明确要求长期保留的工作约定迁移或保存到 `AGENTS.md`、`CLAUDE.md`、OMP context files 等原生持久指令中。

核心能力：

- 检查目标、背景、受众、输入、交付物、范围、约束、证据、权限、验收标准、优先级和异常处置
- 区分已知信息、安全假设、关键缺口和可延后决策
- 只追问会实质改变方案、权限、风险或验收结果的问题，避免无休止澄清
- 对高风险任务先确认契约；对信息充分的中等任务可声明假设后直接执行
- 将任务契约转换为直接、准确、无套话和无刻意修辞的执行 Prompt
- 区分当前任务契约、跨 session 交接信息和长期工作规范，避免把一次性经验固化为永久规则
- 按用户、项目、本地或子目录作用域选择原生文件，并审计加载优先级、覆盖关系和冲突
- 以单一共享规范源服务 Codex、Claude Code 和 OMP，只保留必要的平台适配内容
- 将需要硬性执行的要求路由到权限、hooks、policy 或 CI，而不是把 Markdown 指令误当成强制机制

触发场景：`prompt-ultra`、Prompt 优化、需求澄清、任务拆解、多阶段或高影响工作，以及“记住这个规则”“以后都这样”“保存/迁移工作规范”“创建或更新 AGENTS.md / CLAUDE.md”等持久化请求。简单、低风险且成功标准显然的请求默认跳过。

---

## learn-ultra

把 **GitHub 仓库**、**研究论文**、**技术文章**或一组内部/外部资料，重构成来源可追溯、依赖关系清晰、可练习和可验收的中文学习材料。目标不是复述来源，而是让第一次接触主题的读者形成可验证的能力。

章节数量由知识依赖图决定，通常为 6–14 章；每章从真实问题出发，依次提供直觉、定义、机制或推导、完整例题、反例、练习、答案和来源定位。

特征：

- 支持仓库、论文、文章、多来源语料和已有学习 HTML，并根据来源类型选择分析方法
- 先建立 teaching brief、来源清单、证据 ledger、概念 inventory 和先修依赖图，再确定课程结构
- 用完整例题、近迁移题、独立变式和综合题建立学习脚手架；每题提供答案或评分 rubric
- substantial 教材默认进行两轮完整写作、构建与复审，不把两次 lint 当成两轮审阅
- 提供 HTML 自动验收脚本，检查章节、锚点、目标覆盖、练习层级、答案、来源、移动端 viewport，以及按需启用的公式解释和关系图门禁

触发场景：`learn-ultra`、深入学习、学习路径、教程、教材式 HTML、交互式学习报告、例题与练习、课程重构，或要求把仓库、论文、文章和多来源资料整理为系统学习材料。

---

## figure-ultra

统一图表生成技能，**Draw.io + Excalidraw + Matplotlib 三引擎**，由路由按需求特征自动选择。

与 `tikz-ultra` 的边界由**交付介质**决定：需要通用图片或 `.drawio` / `.excalidraw` / Matplotlib 时使用 `figure-ultra`；需要 `.tex` / `tikzpicture`、LaTeX 原生嵌入或 TikZ 编译时使用 `tikz-ultra`。若用户只说“画架构图”“生成论文配图”而未指定技术，默认使用 `figure-ultra`。

| 需求特征 | 引擎 | 输出 |
| --- | --- | --- |
| 论文/技术文档配图、架构/流程/时序/ER/状态/思维导图、需导出 PNG/SVG/PDF | Draw.io | `.drawio` + 可导出 |
| 手绘风、白板讨论、草图发散、头脑风暴 | Excalidraw | `.excalidraw` |
| 提供数据要折线图/柱状图/散点图/雷达图（论文级） | Matplotlib | dpi=300 PNG |

**Draw.io 引擎**：双风格预设（学术风 / 产品风语义配色）· UML 时序图精确坐标规则 · 深度学习模型架构专用工作流（Transformer / CNN / 检测网络 / 感受野 / 注意力）· 7 科学科示意图 · 风格迁移（参考图 + 内容 → 新图）· 多图文章模式（一文 2-6 图，同文件多 page）

**Excalidraw 引擎**：9 种图类型路由（流程 / 关系 / 思维导图 / 架构 / DFD / 泳道 / 类图 / 时序 / ER）· 8 个起步模板 · AWS/GCP/K8s 图标库经 Python 脚本注入，图标 JSON 不进上下文

**Matplotlib 引擎**：8 种论文图风格（配对柱状 + 增益箭头、分组消融斜线柱、置信带折线、断点训练曲线、L 形 spine + inset、t-SNE 聚类、折断轴散点、双系列雷达），「选模板 + 替换数据区」工作流

触发词：画图、架构图、流程图、时序图、ER 图、状态图、思维导图、模型结构可视化、图片型论文配图、draw.io、Excalidraw、手绘/白板、Matplotlib、把数据画出来、折线/柱状/散点/雷达图。明确要求 TikZ/PGF/`.tex` 时转给 `tikz-ultra`。

---

## tikz-ultra

面向 LaTeX/TikZ 的可复现绘图技能，覆盖路径、节点、矩阵、图层、装饰、流程图、神经网络、有限状态机、树、交换图、统计图和三维图。技能包含精炼参考文档与 13 页原始 TikZ 速查表，并要求先编译、再检查最终尺寸、最后导出。

触发词：TikZ、PGF、PGFPlots、LaTeX 原生绘图、`tikzpicture`、TikZ 编译错误、修改 TikZ 源码、把示意图写成 `.tex`。仅“论文配图”“流程图”“架构图”等主题描述不触发本技能；未要求 LaTeX 源码时使用 `figure-ultra`。

---

## paper-ultra

面向中英文科研论文的读者优先写作与审阅技能。它可处理摘要、引言、方法、结果、结论、Highlights、图表说明、补充材料、Cover Letter 和审稿回复，并将结构、论证、术语、句子、证据与双语同步分开检查。

核心约束：

- 精确保留数字、分母、引文、术语和主张强度
- 尊重作者、期刊和用户指定的修改范围
- 区分研究或工程贡献、实现错误、调试投入和纠正性维护
- 不用错误版本作为改进基线，受错误影响的结果必须重跑或排除
- 最终交付前分别报告内容、证据、编译和成品检查

触发词：`paper-ultra`、论文润色、论文重写、摘要修改、审稿回复、Cover Letter、中英文同步、说人话、去模板化表达、贡献审计、只审不改。

---

## 快捷安装

先克隆仓库：

```bash
git clone https://github.com/TobyChain/ultra-skills.git
```

然后选择所用 Agent，一次安装全部技能：

### TraeCode

```bash
mkdir -p ~/.trae/skills
cp -R ultra-skills/skills/. ~/.trae/skills/
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R ultra-skills/skills/. ~/.claude/skills/
```

### Qoder

```bash
mkdir -p ~/.qoder/skills
cp -R ultra-skills/skills/. ~/.qoder/skills/
```

只安装单个技能时，把 `skills/.` 换成对应目录。例如：

```bash
cp -R ultra-skills/skills/figure-ultra ~/.trae/skills/
```

更新已克隆的仓库并重新覆盖安装：

```bash
git -C ultra-skills pull --ff-only
cp -R ultra-skills/skills/. ~/.trae/skills/
```

安装后重启 Agent 或新建会话，使技能列表重新加载。项目级安装可将技能目录复制到项目根目录的 `.agents/skills/`（Codex/TraeCode）或 `.claude/skills/`（Claude Code）。

**可选依赖**：

- Draw.io 导出 PNG/SVG/PDF 需本机 `drawio` CLI（未安装时保留源文件并给出手动命令）
- 数据图需 Python + matplotlib + numpy
- learn-ultra 的 Mermaid 与代码高亮走 CDN，断网时样式仍在、仅图表不渲染

## 设计原则

1. **渐进式披露**：SKILL.md 只放路由决策与核心规则，详细规范落在 `references/`，按任务需要读取
2. **模板优先于从零生成**：Excalidraw 从 `templates/` 起步，数据图从 `scripts/plot/` 复制改数据，降低出错率
3. **脚本承担确定性工作**：坐标变换、ID 生成、图标注入交给 Python 脚本，不消耗上下文也不会算错
4. **冲突显式裁决**：合并多来源技能时，规范冲突（如 XML value 是否允许 HTML）在主文件里给出唯一裁决，不留两套并行规则

## 来源与致谢

`figure-ultra` 整合自以下技能，冲突项已统一裁决：

| 来源 | 贡献 |
| --- | --- |
| 本地 `drawio-diagram` | 模型架构 / 学术图 / 学科图 ×7 / 风格迁移 / UML 时序精确坐标 |
| [Snailclimb/AIGuide](https://github.com/Snailclimb/AIGuide) `drawio-chart` | 产品风语义配色 / XML 纯文本规则 / 导出命令 / 多图文章模式 |
| 本地 `excalidraw-diagram` | 手绘图文件结构与默认配色 |
| [github/awesome-copilot](https://github.com/github/awesome-copilot) `excalidraw-diagram-generator` | 9 图类型路由 / 8 模板 / 图标库脚本 |
| [Trae1ounG/paper-plot-skills](https://github.com/Trae1ounG/paper-plot-skills) `plot-from-data` | 8 种论文数据图风格与复现脚本 |
| [ysyecust/write-reader-first-papers](https://github.com/ysyecust/write-reader-first-papers) | `paper-ultra` 的读者优先论文写作、证据保护和贡献归因规则 |
