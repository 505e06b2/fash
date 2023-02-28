import sys, string

class Path:
	def expand(path):
		if sys.platform == "win32":
			if path.startswith(tuple(f"/{x}/" for x in string.ascii_letters)):
				return f"{path[1]}:/{path[3:]}"

			elif path.startswith("/"):
				return f"C:/{path[1:]}"

			return path.replace("\\", "/")

		return path

	def collapse(path):
		if sys.platform == "win32" and path[0] in string.ascii_letters: #Windows + C:\ path
			#will look like /c/...
			return f"/{path[0].lower()}/{path[3:]}".replace("\\", "/").rstrip("/")

		return path
