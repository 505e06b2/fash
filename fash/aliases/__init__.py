class _Aliases(dict):
	from .default_aliases import setDefaults as _setDefaults

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._setDefaults()


Aliases = _Aliases()

from .default_aliases import *
