import sys, builtins

def eval(self, args=[], stdout=sys.stdout, stderr=sys.stderr):
	try:
		returned = builtins.eval(" ".join(args))
		if type(returned) == int:
			stdout.write(f"{returned} | 0x{returned:x} | 0b{returned:b}\n")

		else:
			stdout.write(f"{returned}\n")

	except Exception as e:
		stderr.write(f"{e.__class__.__name__}: {e}\n")
		return 1

	return 0
