import os, sys
from pathlib import Path as PathLib

from .__init__ import Variables, VariablesEnum

_home_char = "~"

class SpecialPaths:
	def expandHome(path_str):
		if path_str.startswith(_home_char):
			return Variables[VariablesEnum.home] + path_str[1:]

		return path_str

	def collapseHome(path_str):
		home = Variables[VariablesEnum.home]
		if path_str.startswith(home):
			return f"~{path_str[len(home):]}"

		return path_str

	def fileIsExecutable(path_str):
		path = PathLib(path_str)

		is_executable = os.access(path, os.X_OK)

		if is_executable and sys.platform == "win32":
			is_executable = (path.suffix.lower() in Variables[VariablesEnum.win_executable_extensions])

		return is_executable
