class _Aliases(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self["="] = "eval"
		self["ls"] = "ls --color"

Aliases = _Aliases()

try:
	from .user_aliases import *

except ImportError as e:
	import sys
	from pathlib import Path
	path = Path(__file__)
	user_path = path.parent / f"user_{path.name}"

	if user_path.exists():
		print(f"Cannot import {user_path}")
		sys.exit(1)

	with user_path.open("w") as f:
		f.write("from .aliases import Aliases\n")
		f.write("\n")
		for key, value in Aliases.items():
			f.write(f"Aliases[\"{key}\"] = \"{value}\"\n")
