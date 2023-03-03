import sys

if sys.platform == "win32":
	print("Native Win32 is not supported. Please install MSYS2 or Cygwin")
	sys.exit(1)

is_cygwin = (sys.platform == "cygwin")
