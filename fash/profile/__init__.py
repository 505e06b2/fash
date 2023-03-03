"""
Make sure to import these for altering the state in any scripts:

from fash.variables import Variables
from fash.aliases import Aliases
"""

import sys, importlib

from pathlib import Path as PathLib

__profile_folder = PathLib(__file__).parent #profile/
__root_folder = __profile_folder.parent #fash/

for file in __profile_folder.glob("*.py"):
	if file.name.startswith("_"):
		continue

	module_name = f"{__root_folder.name}.{__profile_folder.name}.{file.stem}"
	module_spec = importlib.util.spec_from_file_location(module_name, file)
	module = importlib.util.module_from_spec(module_spec)

	sys.modules[module_name] = module
	module_spec.loader.exec_module(module)

	for attr in dir(module):
		if attr.startswith("_"):
			continue

		globals()[attr] = module.__dict__[attr]
