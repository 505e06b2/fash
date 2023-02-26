import os, sys, ctypes, subprocess, shlex

from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML

from xml.parsers.expat import ExpatError

from .arg_completers import PromptToolkitCompleter
from .path import Path
from .profile.variables import Variables, VariablesEnum

class Prompt(PromptSession):
	def _getPromptText(self):
		parsed_prompt_string = Variables[VariablesEnum.PS1]
		for key, func in self._prompt_vars.items():
			parsed_prompt_string = parsed_prompt_string.replace(key, func())
		try:
			return HTML(parsed_prompt_string)
		except ExpatError as e:
			sys.stderr.write(f"Unable to use the prompt_string defined in the settings:\n{e}\n")
			return f"{self._prompt_chars[self._havePrivilege()]} "

	def _getGitRepoInfo(self):
		def execGitCmd(command_line):
			process = subprocess.run(shlex.split(command_line), check=True, encoding="utf8", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
			return process.stdout.strip()

		git_format = Variables[VariablesEnum.PS1_git_format]
		try:
			if branch := execGitCmd("git branch --show-current"):
				return (git_format % branch)

			if rev_parse := execGitCmd("git rev-parse --short HEAD"):
				return (git_format % rev_parse)

		except (FileNotFoundError, subprocess.CalledProcessError):
			pass

		return ""

	def _havePrivilege(self):
		if sys.platform == "win32":
			return (ctypes.windll.shell32.IsUserAnAdmin() != 0)
		else:
			return (os.geteuid() == 0)

	def __call__(self, *args, **kwargs):
		return super().prompt(
			self._getPromptText(),
			*args,

			complete_while_typing=False,
			complete_in_thread=True,
			completer=self._completer,
			complete_style=Variables[VariablesEnum.completion_style],
			style=Variables[VariablesEnum.default_style],
			include_default_pygments_style=False,
			**kwargs
		)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._completer = PromptToolkitCompleter()

		self._prompt_chars = (
			"@", #standard
			"#" #privileged
		)

		self._prompt_vars = {
			r"\u": lambda: Variables[VariablesEnum.username],
			r"\h": lambda: Variables[VariablesEnum.hostname],
			r"\w": lambda: Path.collapse(os.getcwd()),
			r"\$": lambda: self._prompt_chars[self._havePrivilege()],
			#non-standard
			r"\g": lambda: self._getGitRepoInfo()
		}
