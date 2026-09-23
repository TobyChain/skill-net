# 数据图表引擎：论文级 Matplotlib 绘图

为论文生成出版级数据图（折线图、柱状图、散点图、雷达图），全部输出 `dpi=300` PNG。工作方式是「选风格模板 + 替换数据」，不从零写 matplotlib 代码。

## 触发特征

- 用户提供数据（数字、数组、CSV）并想要一张学术风格的图
- 「把我的数据画出来」「plot this data」「画个柱状图/折线图/散点图/雷达图」
- 论文实验结果可视化（训练曲线、消融对比、聚类可视化）

注意：节点连线类的结构图（架构、流程、时序）走 Draw.io 引擎，不走本引擎。

## 风格目录（8 种）

| 风格 | 类型 | 脚本 | 适用场景 |
|------|------|------|---------|
| `bar_paired_delta` | 柱状图 | `scripts/plot/bar_memevolve.py` | Baseline vs method 配对对比 + 增益箭头 |
| `bar_grouped_hatch` | 柱状图 | `scripts/plot/bar_spice.py` | 多方法消融，主方法斜线填充，柱顶数值 |
| `line_confidence_band` | 折线图 | `scripts/plot/line_selfdistill.py` | 带置信区间的训练曲线 |
| `line_training_curve` | 折线图 | `scripts/plot/line_aime.py` | 垂直断点线 + 水平参考线 |
| `line_loss_with_inset` | 折线图 | `scripts/plot/line_loss_inset.py` | L 形 spine + 局部放大 inset |
| `scatter_tsne_cluster` | 散点图 | `scripts/plot/scatter_tsne.py` | t-SNE 聚类 + 注释框 |
| `scatter_broken_axis` | 散点图 | `scripts/plot/scatter_break.py` | 折断 X 轴，多 marker 系列 |
| `radar_dual_series` | 雷达图 | `scripts/plot/radar_dora.py` | 双方法多维对比，正八边形网格 |

## 工作流

1. 确认用户的图类型和数据
2. 选择对应风格（不确定时根据数据形状推断，或询问用户）
3. 读取 `references/plot/<style_name>.md` 获取精确参数（rcParams、配色、字号、spine、刻度方向）
4. 复制对应 `scripts/plot/<script>.py`，替换数据区（脚本顶部注释清晰标注数据区）
5. 运行 `python3 scripts/plot/<script>.py --out-dir OUTPUT_DIRECTORY`；省略参数时输出到当前目录
6. 检查输出，必要时微调颜色/标签/字号

## 数据替换规则

- 保持数组维度和类型不变
- 类别数变化（如 4 组改 6 组）时，同步调整颜色列表和宽度计算
- x 轴标签、图例标签直接修改对应字符串列表

## 校验

- [ ] 数据已正确替换，维度匹配
- [ ] 图例、轴标签、标题完整
- [ ] 输出为 dpi=300 PNG
- [ ] 风格与论文其他图一致（同字体字号体系）
