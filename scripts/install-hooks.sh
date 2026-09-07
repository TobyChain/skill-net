#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
git -C "$REPO_ROOT" config core.hooksPath .githooks
printf 'Installed repository hooks from .githooks.\n'
