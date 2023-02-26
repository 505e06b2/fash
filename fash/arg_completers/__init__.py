import os, re, stat, shlex
from pathlib import Path as PathLib

from prompt_toolkit.completion import Completion, Completer

from ..path import Path

class _ArgCompleters(object):
	def _filePath(self, incomplete_path, only_directories=False):
		def createCompletionObject(path_obj, remove_first_x_chars=0):
			name = path_obj.name
			text = name[remove_first_x_chars:].replace(" ", r"\ ")
			display = f"'{name}'" if " " in name else name

			if path_obj.is_symlink():
				return Completion(text, display=display, style="class:shell.symlink")

			if path_obj.is_dir():
				return Completion(f"{text}/", display=display, style="class:shell.directory")

			#expand this to check r/w too?
			if os.access(path_obj, os.X_OK):
				return Completion(text, display=display, style="class:shell.executable")

			return Completion(text, display=display, style="class:shell.file")

		if incomplete_path.startswith(("-", "#", "\"")):
			return []

		#the .replace() will not account for "\\ "
		# the PromptToolKitCompleter should not allow a path with this to get here as the space was not escaped
		incomplete_path = Path.expand(incomplete_path).encode("raw_unicode_escape").decode("unicode_escape").replace(r'\ ', ' ')

		glob_pattern = "*"
		name_len = 0
		path_obj = PathLib(incomplete_path)
		if not incomplete_path.endswith("/"):
			glob_pattern = f"{path_obj.name}*"
			name_len = len(path_obj.name)
			path_obj = path_obj.parent

		found_items = path_obj.glob(glob_pattern)
		if only_directories:
			found_items = filter(lambda x: x.is_dir(), found_items)

		return [createCompletionObject(item, name_len) for item in sorted(found_items, key=lambda x: x.name)]

	def __call__(self, command):
		if command.startswith("_"):
			return None

		try:
			return getattr(self, command)

		except AttributeError:
			return None

	from .builtin_commands import cd

ArgCompleters = _ArgCompleters()

class PromptToolkitCompleter(Completer):
	def _configureFoundCompletions(self, completions):
		return [x if isinstance(x, Completion) else Completion(text=x) for x in completions]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._pattern_get_cursor_arg = re.compile(r"(?:^|\s)((?:[^\s\\]|\\.)+)$", re.S) #does not support quotes

	def get_completions(self, document, complete_event):
		if document.current_char.strip(): #don't complete if no whitespace under cursor
			return []

		arg_match = self._pattern_get_cursor_arg.search(document.text_before_cursor)
		if not arg_match:
			arg = ""
		else:
			arg = arg_match.group(1)

		if arg == document.text_before_cursor: #complete the command
			print(f"\nSEARCH PATH or CWD if starts with ./ + aliases/functions - {arg}")
			return []

		#check command specific args
		command, *_ = shlex.split(document.text_before_cursor)
		if completer := ArgCompleters(command):
			return self._configureFoundCompletions(completer(arg))

		#check filesystem
		if files_found := ArgCompleters._filePath(arg):
			return self._configureFoundCompletions(files_found)

		return []
