# Excalidraw icon and arrow tools

Use these scripts only when an Excalidraw task needs deterministic element
insertion. Both editing tools preserve the original diagram until the updated
JSON has been written successfully.

## Add an arrow

```bash
python scripts/add-arrow.py DIAGRAM.excalidraw FROM_X FROM_Y TO_X TO_Y \\
  [--style solid|dashed|dotted] [--color '#1e1e1e'] [--label TEXT]
```

The tools write to `.excalidraw.edit` and atomically replace the original only
after successful validation and serialization.

## Add an icon

First split a downloaded `.excalidrawlib` file:

```bash
python scripts/split-excalidraw-library.py LIBRARY_DIRECTORY
```

Then insert an icon:

```bash
python scripts/add-icon-to-diagram.py DIAGRAM.excalidraw ICON X Y \\
  --library-path LIBRARY_DIRECTORY [--label TEXT]
```

Third-party icon libraries remain subject to their original licenses. Do not
commit or redistribute generated icon files without checking those terms.
