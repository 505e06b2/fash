import os, sys

from ..profile.variables import Variables, VariablesEnum

def cd(self, args=[], stdout=sys.stdout, stderr=sys.stderr):
	shell_name = Variables[VariablesEnum.shell_name]

	if not args:
		home_dir = Variables[VariablesEnum.home]
		if not home_dir:
			stderr.write(f"{shell_name}: cd: could not find HOME environment variable\n")
			return 1

		args = [home_dir]

	if len(args) > 1:
		stderr.write(f"{shell_name}: cd: too many arguments\n")
		return 1

	path = args[0]

	try:
		os.chdir(path)

	except FileNotFoundError:
		stderr.write(f"{shell_name}: cd: {path}: no such file or directory\n")
		return 1

	except NotADirectoryError:
		stderr.write(f"{shell_name}: cd: {path}: not a directory\n")
		return 1

	except Exception as e:
		stderr.write(f"{shell_name}: cd: {path}: {e.__class__.__name__}\n")
		return 1

	return 0
