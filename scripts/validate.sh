#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
cd "$REPO_ROOT"

python3 scripts/validate_skills.py
python3 -m unittest -v tests/test_figure_tools.py skills/learn-ultra/scripts/test_validate_learning_html.py
if command -v ruff >/dev/null 2>&1; then
  ruff check scripts/validate_skills.py tests/test_figure_tools.py skills/learn-ultra/scripts skills/figure-ultra/scripts
else
  printf 'WARN ruff is unavailable; skipping optional lint. Python syntax was checked.\n'
fi
git diff --check
printf 'Ultra skill validation passed.\n'
