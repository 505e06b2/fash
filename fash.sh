#!/bin/sh

#this allows sudo to work on genuine Linux
#to use cygwin+gsudo with fash, you must not have fash on a network drive, then type `gsudo "$SHELL"` - this may be handy in an alias
export SHELL="$(readlink -m -- "$0")"

PYTHONPATH="$(dirname -- "$SHELL")" exec python -m fash
