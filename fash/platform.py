import sys

if sys.platform == "win32":
	print("Native Win32 is not supported. Please install Python3 in MSYS2 or Cygwin")
	input("Press ENTER to exit")
	sys.exit(1)

is_cygwin = (sys.platform == "cygwin")
