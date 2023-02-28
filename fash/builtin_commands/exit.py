import os, sys

from ..variables import Variables, VariablesEnum

def exit(self, args=[], stdout=sys.stdout, stderr=sys.stderr):
	shell_name = Variables[VariablesEnum.shell_name]

	stdout.write("exit\n")

	if not args:
		args = ["0"]

	if len(args) > 1:
		stderr.write(f"{shell_name}: exit: too many arguments\n")
		args = ["1"]

	try:
		exit_code = int(args[0]) & 0xFF

	except ValueError:
		stderr.write(f"{shell_name}: exit: {args[0]}: numeric argument required\n")
		exit_code = 1

	sys.exit(exit_code)
