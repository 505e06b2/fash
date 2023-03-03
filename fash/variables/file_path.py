import os, sys
from pathlib import Path

_home_char = "~"

class FilePath:
	def __init__(self, parent):
		self._parent = parent

	def expandHome(self, path_str):
		if path_str.startswith(_home_char):
			return self._parent.System.home + path_str[1:]

		return path_str

	def collapseHome(self, path_str):
		home = self._parent.System.home
		if path_str.startswith(home):
			return f"~{path_str[len(home):]}"

		return path_str

	def fileIsExecutable(self, path_str):
		path = Path(path_str)

		is_executable = os.access(path, os.X_OK)

		if is_executable and sys.platform == "win32":
			is_executable = (path.suffix.lower() in parent[VariableEnums.win_executable_extensions])

		return is_executable