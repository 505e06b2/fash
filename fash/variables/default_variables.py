import os, platform

from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.styles import style_from_pygments_cls, Style
from pygments.styles import get_style_by_name

from .folder_list import FolderList

class _SystemVariables(object):
	pass

def _createProperty(parent, variable_name, default_value=""):
	def _get(self):
		return parent[variable_name]

	def _set(self, value):
		parent[variable_name] = value

	def _del(self):
		del parent[variable_name]

	parent[variable_name] = default_value

	return property(_get, _set, _del)

def setDefaults(self):
	_SystemVariables.shell_name     = _createProperty(self, "SHELL_NAME",     "fash")
	_SystemVariables.PS1            = _createProperty(self, "PS1",            r"<bold><ansibrightred>\u</ansibrightred>@<ansibrightred>\h</ansibrightred></bold>:<bold><ansicyan>\w</ansicyan>\g</bold>\$ ")
	_SystemVariables.PS1_git_format = _createProperty(self, "PS1_GIT_FORMAT", " <ansibrightred>(%s)</ansibrightred>")
	_SystemVariables.home           = _createProperty(self, "HOME",           os.environ.get("HOME") or os.environ.get("USERPROFILE") or "") #not using pathlib.Path.expanduser allows the use of HOME on Windows in CPython 3.8+
	_SystemVariables.username       = _createProperty(self, "USERNAME",       os.environ.get("USER") or os.environ.get("USERNAME") or "?")
	_SystemVariables.hostname       = _createProperty(self, "HOSTNAME",       platform.node() or os.environ.get("COMPUTERNAME") or "?")
	_SystemVariables.path           = _createProperty(self, "PATH",           FolderList(os.environ.get("PATH")))
	_SystemVariables.pwd            = _createProperty(self, "PWD",            os.getcwd)

	#Force these extensions to always be executable
	#	in Cygwin/MSYS2, exes are always set, and any script that begins with a shebang line is set implicitly
	_SystemVariables.win_executable_extensions = _createProperty(self, "WIN_EXECUTABLE_EXT", [".bat", ".cmd"])
	_SystemVariables.completion_style =          _createProperty(self, "COMPLETION_STYLE",   CompleteStyle.READLINE_LIKE)

	#To find the keys for the following dict, in Python REPL (PYTHONPATH may need to be set):
	"""
from prompt_toolkit.document import Document
from prompt_toolkit.lexers import PygmentsLexer
from fash.parsing.lexer import Lexer
PygmentsLexer(Lexer).lex_document(Document("[test line]"))(0)
	"""
	#made to support white on black, 16 colours
	_SystemVariables.default_style = _createProperty(self, "DEFAULT_STYLE", Style.from_dict({
		"pygments.keyword": "ansiblue",

		"pygments.comment": "ansibrightblack",

		"pygments.name": "ansibrightcyan",
		"pygments.name.builtin": "ansibrightgreen",

		"pygments.literal.string": "ansibrightyellow",
		"pygments.literal.string.escape": "ansibrightblack",
		"pygments.literal.string.interpol": "ansiblue",

		"pygments.literal.number": "ansibrightyellow",

		"shell.symlink": "ansicyan bold",
		"shell.directory": "ansiblue bold",
		"shell.executable": "ansigreen bold",
		"shell.file": "default",
		"shell.alias": "ansibrightyellow bold"
	}))

	return _SystemVariables()
