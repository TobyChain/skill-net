# TikZ Working Reference

This reference condenses the bundled 13-page Chinese TikZ cheatsheet. Use the
PDF in `../assets/tikz-cheatsheet.pdf` for the original rendered examples.
The source document identifies itself as "TikZ 速查表" by 五道口纳什 and
targets PGF/TikZ 3.1.11 with XeLaTeX.

## Contents

- Core commands, paths, coordinates, and styling
- Nodes, matrices, positioning, and reusable styles
- Libraries for graphs, plots, decorations, and 3D work
- Common figure patterns and compilation commands
- Debugging and export checks

## Core Commands

All drawing commands are path operations:

```latex
\path ...;                    % construct only
\draw ...;                    % \path[draw]
\fill ...;                    % \path[fill]
\filldraw ...;                % fill and stroke
\shade ...;                   % gradient fill
\node ...;                    % path shorthand for a node
\coordinate (name) at (...);  % named point
\pic ...;                     % reusable graphic
```

Common path operators:

```latex
(a) -- (b)                         % straight line
(a) -| (b)                         % horizontal then vertical
(a) |- (b)                         % vertical then horizontal
(a) .. controls (c1) and (c2) .. (b)
(a) to[out=30,in=150] (b)
(a) rectangle (b)
(a) circle (5mm)
(a) ellipse (8mm and 5mm)
(a) arc (90:0:10mm)
(a) -- cycle
```

Coordinates:

```latex
(2,1)              % Cartesian
(30:2)             % polar: angle:radius
++(.5,0)           % relative and move current point
+(.5,0)            % relative without moving current point
($(A)!.5!(B)$)     % midpoint/interpolation; calc library
($(A)!(C)!(B)$)    % projection of C onto AB
($(A)!1cm!90:(B)$) % distance and rotation
```

## Lines, Color, Fill, and Arrows

Useful line styles include `ultra thin`, `thin`, `thick`, `very thick`,
`ultra thick`, `double`, `dashed`, `dotted`, and `dashdotted`. For exact
patterns:

```latex
\draw[dash pattern=on 4pt off 1pt on 1pt off 1pt] ...;
\draw[line width=1.2pt,line cap=round] ...;
```

Colors use xcolor mixing:

```latex
blue!30
blue!40!orange
fill opacity=.25
draw opacity=.8
```

Prefer `arrows.meta`:

```latex
\usetikzlibrary{arrows.meta,bending}
\draw[-{Stealth}] ...;
\draw[{Stealth[length=4mm,width=3mm]}-{Latex}] ...;
\draw[-{Stealth[reversed]},shorten >=4pt,shorten <=4pt] ...;
```

Fills and effects:

```latex
\fill[pattern=north east lines,pattern color=blue] ...;
\shade[left color=red,right color=yellow] ...;
\shade[inner color=white,outer color=blue] ...;
\shadedraw[ball color=purple] ...;
```

Libraries: `patterns`, `patterns.meta`, `fadings`, `shadows`,
`shadows.blur`.

## Nodes and Layout

Define repeated roles as styles:

```latex
\begin{tikzpicture}[
  node distance=6mm and 10mm,
  box/.style={
    draw,
    rounded corners=2pt,
    fill=blue!8,
    minimum height=7mm,
    inner sep=4pt,
    font=\small
  }
]
  \node[box] (a) {Input};
  \node[box,right=of a] (b) {Process};
  \draw[-Stealth] (a) -- (b);
\end{tikzpicture}
```

Anchors include `.north`, `.south`, `.east`, `.west`, corner combinations,
`.center`, and arbitrary angles such as `.35`.

Place labels on paths with `midway`, `pos=.25`, `sloped`, `auto`, and `swap`.
Use explicit anchors when automatic routing is ambiguous.

Relevant libraries:

- `positioning`: `above=of`, `right=2cm of`
- `shapes.geometric`, `shapes.symbols`, `shapes.multipart`,
  `shapes.callouts`
- `matrix`: `matrix of nodes`, `matrix of math nodes`
- `chains`: `start chain`, `on chain`, `join`
- `fit`: group several nodes with one enclosing node
- `backgrounds`: draw groups and regions behind foreground nodes

## Structured Generation

Styles:

```latex
\tikzset{
  box/.style={draw,fill=#1!20},
  box/.default=blue,
  highlight/.style 2 args={draw=#1,line width=#2}
}
```

Scopes isolate transforms and styles:

```latex
\begin{scope}[xshift=2cm,rotate=15]
  ...
\end{scope}
```

Loops and calculations:

```latex
\foreach \x in {0,1,...,6} { ... }
\foreach \x/\color in {0/red,1/orange,2/green} { ... }
\foreach \name [count=\i] in {A,B,C} { ... }
\pgfmathsetmacro{\angle}{360/\n*\i}
```

Common math functions: `sin`, `cos`, `tan`, `atan2`, `sqrt`, `pow`, `exp`,
`ln`, `mod`, `div`, `int`, `round`, `min`, `max`, `abs`, `veclen`, `rnd`.

## Geometry and Layers

Intersections:

```latex
\usetikzlibrary{intersections}
\path[name path=a] ...;
\path[name path=b] ...;
\path[name intersections={of=a and b,total=\n}];
% Results: (intersection-1), ...
```

Angles:

```latex
\usetikzlibrary{angles,quotes}
\pic[draw,"$\alpha$",angle radius=8mm] {angle=B--A--C};
```

Clipping and repeated actions:

```latex
\clip (0,0) circle (1cm);
\draw[postaction={draw=white,dashed}] ...;
\fill[preaction={fill=black,opacity=.2,
  transform canvas={xshift=2pt,yshift=-2pt}}] ...;
```

Layering:

```latex
\usetikzlibrary{backgrounds}
\begin{scope}[on background layer]
  ...
\end{scope}
```

Bounding boxes and overlays:

```latex
\path[use as bounding box] (0,0) rectangle (4,3);
\begin{tikzpicture}[remember picture]
...
\draw[overlay] ...;
```

`remember picture` references require at least two compilation passes.

## Curves and Decorations

Curves:

```latex
\draw (a) .. controls (c1) and (c2) .. (b);
\draw (a) to[out=70,in=190] (b);
\draw plot[smooth] coordinates {(0,0) (1,1) (2,0)};
\draw[domain=0:6.28,samples=120,smooth]
  plot (\x,{sin(\x r)});
```

Decoration libraries:

- `decorations.pathmorphing`: snake, coil, zigzag, saw, bumps
- `decorations.pathreplacing`: brace, ticks
- `decorations.markings`: arrows, points, or nodes along a path
- `decorations.text`: text along a path

Apply decorations with `decorate,decoration={...}`. For midway arrows, use
`postaction={decorate,...}` so the original path remains intact.

## Common Diagram Recipes

### Flowchart

Use `positioning`, semantic node styles, and orthogonal `-|`/`|-` routing.
Use `diamond,aspect=2` for decisions and label outgoing edges directly.

### Neural Network

Generate layer nodes and dense edges with nested `\foreach` loops. Keep edges
light (`gray!40`) and nodes visually dominant.

### State Machine

Use:

```latex
\usetikzlibrary{automata,positioning,arrows.meta}
\node[state,initial] ...
\node[state,accepting] ...
\path[->] (q0) edge node{a} (q1)
                 edge[loop above] node{b} (q0);
```

### Tree

Use `child` syntax with level-specific `sibling distance` and
`level distance`. Define `edge from parent/.style` once.

### Commutative Diagram

Use `matrix of math nodes` and connect cells such as `(m-1-1)` with labeled
edges. Keep row and column spacing explicit.

### Plots

Use `pgfplots` for axes, legends, error bars, surfaces, and data-driven plots:

```latex
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\begin{axis}[xlabel=$x$,ylabel=$y$,grid=major]
  \addplot[blue,thick,domain=0:6,samples=80] {sin(deg(x))};
\end{axis}
```

Use pure TikZ loops only for compact fixed charts such as a small bar chart or
heatmap.

### 3D

- Simple tensor/block: define custom `x`, `y`, and `z` unit vectors.
- Spherical coordinates and angle arcs: use `tikz-3dplot`.
- Surface plot: use `pgfplots` with `\addplot3[surf]`.

## Library Map

- Arrows: `arrows.meta`, `bending`
- Coordinates: `calc`, `intersections`, `positioning`, `through`
- Shapes: `shapes.geometric`, `shapes.symbols`, `shapes.misc`,
  `shapes.multipart`, `shapes.arrows`, `shapes.callouts`
- Structure: `fit`, `matrix`, `chains`, `backgrounds`, `spy`
- Decoration: `decorations.pathmorphing`, `decorations.pathreplacing`,
  `decorations.markings`, `decorations.text`, `decorations.shapes`
- Fill: `patterns`, `patterns.meta`, `fadings`, `shadows`, `shadows.blur`
- Specialized: `automata`, `petri`, `trees`, `mindmap`, `graphs`, `calendar`,
  `angles`, `quotes`, `babel`, `external`
- Separate packages: `pgfplots`, `tikz-3dplot`

## Frequent Failure Modes

1. Missing semicolon after a path or node.
2. Expecting `scale` to scale text and stroke widths.
3. Confusing named nodes with plain coordinates.
4. Supplying radians to trigonometric functions without the `r` suffix.
5. Leaving comma-containing option values unbraced.
6. Using a loop or math macro outside its scope.
7. Compiling `remember picture` or references only once.
8. Allowing body text size to control all labels accidentally.
9. Applying a pattern and shading in one fill instead of layered paths.
10. Compiling Chinese labels without XeLaTeX/LuaLaTeX and `ctex`/`xeCJK`.

## Compile and Export

Standalone source:

```latex
\documentclass[tikz,border=2mm]{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
  ...
\end{tikzpicture}
\end{document}
```

Commands:

```bash
latexmk -pdfxe figure.tex
pdflatex figure.tex
lualatex figure.tex
pdftocairo -png -r 300 -singlefile figure.pdf figure
pdftocairo -svg figure.pdf figure.svg
dvisvgm --pdf --font-format=woff figure.pdf
```

For many figures, use `external` and `\tikzexternalize[prefix=figs/]`, then
compile with `-shell-escape`.
