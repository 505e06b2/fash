import os, sys

from ..variables import Variables, VariablesEnum

def path(self, args=[], stdout=sys.stdout, stderr=sys.stderr):
	shell_name = Variables[VariablesEnum.shell_name]
	path_var = Variables[VariablesEnum.path]

	if not args:
		if not path_var.len:
			stderr.write(f"{shell_name}: path: PATH variable is empty!?\n")
			return 1

		stdout.write(f"{path_var.string}\n")
		return 0

	#append/prepend dir, pop dirs (via index), etc

	return 0
