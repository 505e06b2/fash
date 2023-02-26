import sys, string

from .profile.variables import Variables, VariablesEnum

class Path:
	def expand(path):
		home = Variables[VariablesEnum.home]

		if sys.platform == "win32":
			if path.startswith("~"):
				return home.replace("\\", "/") + path[1:]

			elif path.startswith(tuple(f"/{x}/" for x in string.ascii_letters)):
				return f"{path[1]}:/{path[3:]}"

			elif path.startswith("/"):
				return f"C:/{path[1:]}"

		else:
			if path.startswith("~"):
				#not following the Bash standard of being able to use other account's home directories
				return home + path[1:]

		return path

	def collapse(path):
		home = Variables[VariablesEnum.home] #home does not usually have a trailing slash for both Linux and Win32

		if path.startswith(home):
			path = f"~{path[len(home):]}"
			return (path.replace("\\", "/") if sys.platform == "win32" else path)

		if sys.platform == "win32":
			#will look like /c/...
			return f"/{path[0].lower()}/{path[3:]}".replace("\\", "/").rstrip("/")

		return path
