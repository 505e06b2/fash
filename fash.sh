#!/bin/sh

export SHELL="$(realpath -- "$0")"
PYTHONPATH="$(dirname -- "$SHELL")" exec python -m fash
