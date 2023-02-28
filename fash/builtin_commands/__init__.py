class BuiltinCommands:
	from .exit import exit
	from .cd import cd
	from .eval import eval
	from .alias import alias
	from .path import path

	def __call__(self, command):
		if command.startswith("_"):
			return None

		try:
			return getattr(self, command)

		except AttributeError:
			return None
