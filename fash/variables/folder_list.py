import sys

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
		return self.string

	def __init__(self, original_str):
		self._store = []
		self._default_separator = ":"

		self._store = original_str.strip(self._default_separator).split(self._default_separator)
