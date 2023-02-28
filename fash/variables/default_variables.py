import os, platform

from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import style_from_pygments_cls, Style
from pygments.styles import get_style_by_name

from .__init__ import Variables, VariablesEnum

#default variables
Variables[VariablesEnum.shell_name] = "fash"
Variables[VariablesEnum.PS1] = r"<bold><ansibrightred>\u</ansibrightred>@<ansibrightred>\h</ansibrightred></bold>:<bold><ansicyan>\w</ansicyan>\g</bold>\$ "
Variables[VariablesEnum.PS1_git_format] = " <ansibrightred>(%s)</ansibrightred>"
Variables[VariablesEnum.home] = os.environ.get("HOME") or os.environ.get("USERPROFILE") or None #not using pathlib.Path.expanduser allows the use of HOME on Windows in CPython 3.8+
Variables[VariablesEnum.username] = os.environ.get("USER") or os.environ.get("USERNAME") or "?"
Variables[VariablesEnum.hostname] = platform.node() or os.environ.get("COMPUTERNAME") or "?"

Variables[VariablesEnum.win_executable_extensions] = [".exe", ".bat", ".cmd", ".vbs", ".py", ".ps1", ".csx"]
Variables[VariablesEnum.completion_style] = CompleteStyle.READLINE_LIKE

#To find the keys for the following dict, in Python REPL:
"""
from prompt_toolkit.document import Document
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.shell import BashLexer
PygmentsLexer(BashLexer).lex_document(Document("[test line]"))(0)
"""
#made to support white on black, 16 colours - loosely following the default for naming: https://github.com/pygments/pygments/blob/master/pygments/styles/default.py
Variables[VariablesEnum.default_style] = Style.from_dict({
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
