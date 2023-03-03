import os, re, stat, shlex
from pathlib import Path as PathLib

from prompt_toolkit.completion import Completion, Completer

from ..variables import Variables
from ..aliases import Aliases

def _createPathCompletionObject(path_obj, remove_first_x_chars=0, style=None):
	name = path_obj.name
	text = name[remove_first_x_chars:].replace(" ", r"\ ")
	display = f"'{name}'" if " " in name else name

	if style != None:
		return Completion(text, display=display, style=style)

	if path_obj.is_symlink():
		return Completion(text, display=display, style="class:shell.symlink")

	if path_obj.is_dir():
		return Completion(f"{text}/", display=display, style="class:shell.directory")

	#expand this to check r/w too?
	if Variables.FilePath.fileIsExecutable(path_obj):
		return Completion(text, display=display, style="class:shell.executable")

	return Completion(text, display=display, style="class:shell.file")

class _ArgCompleters(object):
	def _decodeText(self, text): #move this elsewhere
		return text.encode("raw_unicode_escape").decode("unicode_escape").replace(r"\ ", " ")

	def _filePath(self, incomplete_path, only_directories=False, only_executables=False):
		if incomplete_path.startswith(("-", "#", "\"")):
			return []

		#the .replace() will not account for "\\ "
		# the PromptToolKitCompleter should not allow a path with this to get here as the space was not escaped
		incomplete_path = Variables.FilePath.expandHome(self._decodeText(incomplete_path))

		glob_pattern = "*"
		name_len = 0
		path_obj = PathLib(incomplete_path)
		if not incomplete_path.endswith("/"):
			glob_pattern = f"{path_obj.name}*"
			name_len = len(path_obj.name)
			path_obj = path_obj.parent

		found_items = list(path_obj.glob(glob_pattern)) #must not be a generator or will be consumed
		ret_items = []
		if only_directories:
			ret_items += list(filter(lambda x: x.is_dir(), found_items))

		if only_executables:
			ret_items += list(filter(lambda x: x.is_file() and Variables.FilePath.fileIsExecutable(x), found_items))

		if not only_directories and not only_executables:
			ret_items = found_items

		return [_createPathCompletionObject(item, name_len) for item in ret_items]

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
	def _sortCompletions(self, completions):
		return list(sorted(completions, key=lambda x: x.text))

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
			if not arg:
				return []

			ret_executables = []

			#check for files
			if "/" in arg: #check cwd, might start with ./ or a folder name
				ret_executables += ArgCompleters._filePath(arg, only_directories=True, only_executables=True)

			else:
				executables_found = {}

				for path_str in reversed(Variables.System.path.collapsed_directories):
					executables_found.update({ completion.text: completion for completion in ArgCompleters._filePath(f"{path_str}/{arg}", only_executables=True) })

				#check for functions

				#check for aliases
				alias_name = ArgCompleters._decodeText(arg)
				for alias in Aliases.keys():
					if alias.startswith(alias_name):
						completion = _createPathCompletionObject(PathLib(alias), len(alias_name), style="class:shell.alias") #using PathLib here, just for the function to work, is a bit dodgy
						executables_found[completion.text] = completion

				ret_executables += list(executables_found.values())

			return self._sortCompletions(ret_executables)

		#check command specific args
		try:
			command, *_ = shlex.split(document.text_before_cursor)
			if completer := ArgCompleters(command):
				return self._sortCompletions(completer(arg))

		except ValueError:
			return []

		#check filesystem
		if files_found := ArgCompleters._filePath(arg):
			return self._sortCompletions(files_found)

		return []
