class _Aliases(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

Aliases = _Aliases()

from .default_aliases import *
