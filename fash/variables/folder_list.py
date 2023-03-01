import sys

from ..path import Path

class FolderList:
	@property
	def string(self):
		return self._default_separator.join(self._store)

	@property
	def len(self):
		return len(self._store)

	@property
	def collapsed_directories(self):
		return self._store

	def __repr__(self):
		if sys.platform == "win32":
			return self._windows_separator.join([Path.expand(collapsed_path) for collapsed_path in self._store])

		else:
			return self.string

	def __init__(self, original_str):
		self._store = []
		self._default_separator = ":"
		self._windows_separator = ";"

		if sys.platform == "win32":
			for win_path in original_str.strip(self._windows_separator).split(self._windows_separator):
				self._store.append(Path.collapse(win_path))

		else:
			self._store = original_str.strip(self._default_separator).split(self._default_separator)
