from cgitb import text
import os, sys

from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import print_formatted_text

from ..variables import Variables, VariablesEnum
from ..aliases import Aliases

def alias(self, args=[], stdout=sys.stdout, stderr=sys.stderr):
	if not args:
		lines = []
		for key, value in Aliases.items():
			lines.append(FormattedText([
				("class:pygments.name.builtin", "alias"),
				("default", " "),
				("class:pygments.name.variable", key),
				("default", "="),
				("class:pygments.string", f"'{value}'")
			]))

		print_formatted_text(*lines, sep="\n", style=Variables[VariablesEnum.default_style])

	#either set aliases, or call them if the arg isn't like a="a"

	return 0
