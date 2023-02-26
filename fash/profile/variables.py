import os, platform

from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import style_from_pygments_cls, Style
from pygments.styles import get_style_by_name

#for accessing system vars without typos
class VariablesEnum(object):
	shell = "SHELL"
	PS1 = "PS1"
	PS1_git_format = "PS1_GIT_FORMAT"
	home = "HOME"
	username = "USERNAME"
	hostname = "HOSTNAME"

	#non-standard vars
	completion_style = "COMPLETION_STYLE"
	default_style = "DEFAULT_STYLE"

class _Variables(dict):
	def __getitem__(self, key):
		try:
			ret = super().__getitem__(key)
			if callable(ret):
				ret = ret()

			return ret

		except KeyError:
			return ""

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self[VariablesEnum.shell] = "pitsh"
		self[VariablesEnum.PS1] = r"<bold><ansibrightred>\u</ansibrightred>@<ansibrightred>\h</ansibrightred></bold>:<bold><ansicyan>\w</ansicyan>\g</bold>\$ "
		self[VariablesEnum.PS1_git_format] = " <ansibrightred>(%s)</ansibrightred>"
		self[VariablesEnum.home] = lambda: os.environ.get("HOME") or os.environ.get("USERPROFILE") or None #not using pathlib.Path.expanduser allows the use of HOME on Windows in CPython 3.8+
		self[VariablesEnum.username] = lambda: os.environ.get("USER") or os.environ.get("USERNAME") or "?"
		self[VariablesEnum.hostname] = lambda: platform.node() or os.environ.get("COMPUTERNAME") or "?"

		self[VariablesEnum.completion_style] = CompleteStyle.READLINE_LIKE

		#To find the keys for the following dict, in Python REPL:
		"""
		from prompt_toolkit.document import Document
		from prompt_toolkit.lexers import PygmentsLexer
		from pygments.lexers.shell import BashLexer
		PygmentsLexer(BashLexer).lex_document(Document("[test line]"))(0)
		"""
		#made to support white on black, 16 colours - loosely following the default for naming: https://github.com/pygments/pygments/blob/master/pygments/styles/default.py
		self[VariablesEnum.default_style] = Style.from_dict({
			"pygments.keyword": "ansibrightgreen",
			"pygments.name.builtin": "ansibrightgreen",
			"pygments.name.variable": "ansibrightcyan",
			"pygments.literal.string": "ansibrightyellow",
			"pygments.literal.string.escape": "ansibrightblue",

			"shell.symlink": "ansicyan bold",
			"shell.directory": "ansiblue bold",
			"shell.executable": "ansigreen bold",
			"shell.file": "default"
		})

Variables = _Variables()

try:
	from .user_variables import *

except ImportError as e:
	import sys
	from datetime import datetime, timezone
	from pathlib import Path
	path = Path(__file__)
	user_path = path.parent / f"user_{path.name}"

	if user_path.exists():
		print(f"Cannot import {user_path}")
		sys.exit(1)

	with user_path.open("w") as f:
		f.write("from .variables import Variables\n")
		f.write("\n")
		f.write(f"Variables[\"FIRST_LOGIN\"] = \"{datetime.now(timezone.utc).astimezone().isoformat()}\"\n")
