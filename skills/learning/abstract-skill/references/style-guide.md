# abstract-skill 设计系统说明

> 这份文档是给生成报告时**参考**的，不要把它复制进最终报告。`template.html` 已经实现了所有样式，你只需要按既定 HTML 类名往里填内容。

## 设计哲学

- **温暖的纸感（warm paper）**：背景用米白 `#fbfaf6` 而非纯白，避免长时间阅读疲劳。强调色用一种暖橘 `#d96f3a`，让人想到铅笔标注，而不是常见的"AI 蓝紫渐变"。
- **结构压倒装饰**：每个章节是一个独立"卡片"，章节内部用一致的纵向节奏（标题 24px → 二级 18px → 正文 16px）。
- **代码即一等公民**：代码块用专门的等宽字体 JetBrains Mono，行高 1.6，留白比一般文档大，方便逐行扫读。
- **学习反馈循环可见**：自测题用 `<details>` 元素+绿色 `?`，答开后变橙色 `✓`，给学习者明确的"我点开了"反馈。

## 颜色

| 用途 | 变量 | 值 | 出现场景 |
|---|---|---|---|
| 主文字 | `--ink` | `#1a1c2c` | 正文 |
| 次要文字 | `--ink-2` | `#3b3f5c` | 引用、解释栏 |
| 弱化文字 | `--ink-3` | `#6c7395` | TOC 编号、Footer |
| 主色（橘） | `--accent` | `#d96f3a` | 章节编号、链接、强调 |
| 副色（紫） | `--accent-2` | `#7c5cff` | 链接、"大白话" 徽标 |
| 成功（绿） | `--good` | `#3a8f5d` | 自测题 `?` 图标 |
| 错误（红） | `--err` | `#b03a48` | 误区列表左边框 |

## 字号节奏

```
header h1   34 px / 1.25  — 标题
section h2  24 px / 1.4   — 章节标题（章数由知识依赖图决定）
section h3  18 px / 1.5   — 章节内子标题
正文        16 px / 1.75
table       14.5 px / 1.65
code        13.5 px / 1.6
TOC         14 px / 1.4
TOC 编号     11 px (mono)
徽标         11 px (mono, .18em)
```

## 间距节奏

- 章节之间留 64 px
- 章节标题下方 20 px 后开始正文
- 段落之间 14 px
- 代码块/表格上下 16-18 px

## 已内置的 HTML 模式（按下面的 class 直接用）

### 自测题
```html
<details class="quiz">
  <summary>Q1. 当 X 改变时，Y 会发生什么？</summary>
  <div class="answer">Y 会重新计算，因为 …</div>
</details>
```

### 代码 + 大白话
```html
<div class="code-pair">
  <pre><code class="language-python">def f(x): return x*x</code></pre>
  <div class="explain">
    <p>这个函数把输入平方再返回。</p>
    <p>之所以叫 f 而不是 square，是因为论文里的记号就是 f。</p>
  </div>
</div>
```

### Mermaid 图
```html
<div class="mermaid">
flowchart LR
  A[输入] --> B[处理]
  B --> C[输出]
</div>
```

### 误区
```html
<div class="pitfall">
  <span class="label">误区</span>
  <p>以为 X 是同步的</p>
  <p class="truth"><strong>真相：</strong>X 实际上是异步的，下文 Y 依赖它的回调。</p>
</div>
```

### 引用块（用于"为什么"等观点性段落）
```html
<blockquote>
  作者的核心观察是：注意力机制让模型可以在序列内任意位置交换信息……
</blockquote>
```

### 荧光笔行内标记（行内唯一的高亮方式）
```html
<p>把状态缓存记为 <span class="hl">KV cache</span>，失败分支用
<span class="hl-green">break-inside:avoid</span> 保护。</p>
```

### 多语言代码块（highlight.js 着色）
```html
<pre><code class="language-python">def f(x): return x * x</code></pre>
<pre><code class="language-bash">curl -sS -o out.json --data @req.json -w '%{time_total}\n' "$API"</code></pre>
<pre><code class="language-json">{ "queue": { "type": "choice" } }</code></pre>
```

## 布局与分栏（由内容决定）

- **默认单栏**。分栏（.two-col）和通栏（.bleed）都是可选项，唯一目的是更好地展示内容并充分利用页宽，不是装饰。
- 是否分栏以**文档为单位**决定（多页文档则以页为单位）；同一文档内不要混用分栏与单栏的正文区。完全可以整篇不分栏。
- 适合分栏：文字密集、元素小而并行的内容——方法清单、术语对照、多分支对比；读者逐栏扫读不吃力。
- 不适合分栏：代码块、宽表格、公式推导、长流程图为主的章节。它们需要整宽，硬塞进半栏会制造横向滚动；这类文档保持单栏，宽元素用 .bleed 通栏。
- 宽度优先级：让表格和代码在内容宽内完整显示 > .bleed 通栏用满页宽 > 横向滚动（仅窄屏回退）。不要给表格写 min-width 强制滚动条。
- 分栏时 pre/table/figure/公式必须 break-inside:avoid，不跨栏断裂；需要整宽的元素用 column-span:all。
- “第 1 页单栏、第 2 页双栏”只是示例布局，不是规定；每篇文档按内容重新判断。

## 行内标记（替代行内代码芯片）

- 不使用行内代码芯片——即 Markdown 反引号 `` `x` `` 渲染出的灰底等宽小块——标记术语、标识符或强调。
- 需要高亮或标记时用荧光笔样式：`<span class="hl">…</span>`（黄）/ `<span class="hl-green">…</span>`（绿）；普通强调用 `<strong>`/`<em>`。
- 不使用「」引号标记文本；用中文引号“”或直接不加标记。

## 代码渲染

- 代码块一律 `<pre><code class="language-xxx">…</code></pre>`，由 highlight.js 按语言着色（模板已引入）。常用语言：python、json、bash、sql、ts、plaintext。
- 代码块占满内容宽；行长的代码块外层加 .bleed 通栏，用满页宽。`overflow-x:auto` 只是最后回退——优先通过通栏、12.5–13.5px 字号或拆分长行让代码完整显示。

## 不要做的事

- 不要把页面背景改成纯白，破坏 paper 质感
- 不要在章节里堆 emoji 当列表标记
- 不要把代码块放进灰色或深色主题，与全文反差太大
- 不要用渐变色当强调色（保持手绘笔记感）
- 不要超过 2 张并排的图（移动端 < 900px 时已自动堆叠）
- 不要用行内代码芯片或「」来标记术语；行内高亮只用荧光笔样式
- 不要为了"好看"分栏；不要让代码或表格在桌面宽度出现横向滚动条
- 不要给表格或代码块写 min-width 强制横向滚动
