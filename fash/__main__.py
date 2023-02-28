import traceback

from .__init__ import Shell

try:
	Shell().interactiveMode()

except Exception as e:
	traceback.print_exception(e)
	input("Press ENTER to exit")
