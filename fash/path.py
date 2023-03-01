import sys, string

class Path:
	def expand(path):
		if sys.platform == "win32":
			if path.startswith(tuple(f"/{x}/" for x in string.ascii_letters)):
				return f"{path[1]}:/{path[3:]}"

			elif path.startswith("/"):
				return f"C:/{path[1:]}"

		return path

	def collapse(path):
		if sys.platform == "win32" and len(path) >= 3 and path[0] in string.ascii_letters and path[1:3] == ":\\": #Windows + C:\ path
			#will look like /c/...
			return f"/{path[0].lower()}{path[2:]}".replace("\\", "/").rstrip("/")

		return path
