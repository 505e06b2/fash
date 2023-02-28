import sys

from ..path import Path

class FolderList:
	def __repr__(self):
		if sys.platform == "win32":
			return self._separator.join([Path.expand(collapsed_path) for collapsed_path in self._store])

		else:
			return self._separator.join(self._store)

	def __init__(self, original_str):
		self._store = []

		if sys.platform == "win32":
			self._separator = ";"
			for win_path in original_str.strip(self._separator).split(self._separator):
				self._store.append(Path.collapse(win_path))

		else:
			self._separator = ":"
			self._store = original_str.strip(self._separator).split(self._separator)
