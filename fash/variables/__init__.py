import os

#for accessing system vars without typos
class VariablesEnum(object):
	shell_name = "SHELL_NAME"
	PS1 = "PS1"
	PS1_git_format = "PS1_GIT_FORMAT"
	home = "HOME"
	username = "USERNAME"
	hostname = "HOSTNAME"
	path = "PATH"
	pwd = "PWD"

	#non-standard vars
	win_executable_extensions = "WIN_EXECUTABLE_EXT"
	completion_style = "COMPLETION_STYLE"
	default_style = "DEFAULT_STYLE"

class _Variables(dict): #case insensitive (due to Windows being insensitive)
	@property
	def environment(self):
		return {key: str(value) for key, value in self.items()}

	def _transform_key(self, key):
		return key.upper()

	def __getitem__(self, key):
		try:
			ret = super().__getitem__(self._transform_key(key))

		except KeyError:
			return ""

		if callable(ret):
			ret = ret()

		return ret

	def __setitem__(self, key, value):
		return super().__setitem__(self._transform_key(key), value)

	def __delitem__(self, key):
		return super().__delitem__(self._transform_key(key))

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		#enforce uppercase keys
		for key, value in self.copy().items():
			super().__delitem__(key)
			self[self._transform_key(key)] = value

	def get(self, key, default=None):
		return super().get(self._transform_key(key), default)

	def pop(self, key):
		return super().pop(self._transform_key(key))

Variables = _Variables(os.environ)

from .default_variables import *
from .special_paths import *
