# learn-ultra 设计系统说明

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

## 不要做的事

- 不要把页面背景改成纯白，破坏 paper 质感
- 不要在章节里堆 emoji 当列表标记
- 不要把代码块放进灰色或深色主题，与全文反差太大
- 不要用渐变色当强调色（保持手绘笔记感）
- 不要超过 2 张并排的图（移动端 < 900px 时已自动堆叠）
