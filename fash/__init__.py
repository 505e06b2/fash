import os, sys, subprocess, shlex, re

from pygments.lexers.shell import BashLexer

from prompt_toolkit.lexers import PygmentsLexer

from .path import Path
from .builtin_commands import BuiltinCommands
from .prompt import Prompt
from .variables import Variables, VariablesEnum
from .aliases import Aliases

from .profile import *

class Shell:
	def __init__(self):
		self._builtin_commands = BuiltinCommands()
		self._prompt = Prompt()
		self._pattern_variables = re.compile(r"(?<!\\)\$(?:((?:[^\W\\]|\\.)+)|{(.*?)})", re.S)

		self._last_exit_code = 0

	def unrollAliases(self, line):
		try:
			command, *rest_of_line = line.split(maxsplit=1)
			rest_of_line = ''.join(rest_of_line)

			alias = Aliases.get(command)

			if alias:
				if alias.endswith(" "):
					rest_of_line = self.unrollAliases(rest_of_line)
				return f"{alias} {rest_of_line}"

		except ValueError:
			pass

		return line

	def expandVariables(self, line):
		while var_match := self._pattern_variables.search(line):
			start_index, end_index = var_match.span()
			try:
				name = next(filter(lambda x: x, var_match.groups())) # this will not remove the backslash from "$VAR\ 1"

			except StopIteration: #was given "${}"
				return None

			line = f"{line[:start_index]}{Variables[name]}{line[end_index:]}"

		return line

	def interactiveMode(self):
		while True:
			try:
				input_text = self._prompt(lexer=PygmentsLexer(BashLexer)) #temporary lexer

			except EOFError:
				sys.stdout.write("exit\n")
				self._last_exit_code = 0
				break

			except KeyboardInterrupt:
				continue

			#check if starts with whitespace, so history won't be written?

			input_text = input_text.strip()

			if input_text == "":
				continue

			#sort out piping, etc

			#strip out and set environment variables from the start of command, for use with subprocess
			#	merge Variables.environment + inputted vars into a dict for this

			#unrolling and expanding maybe needs to go after shlex, as variables won't update for ; - pipe does not have this issue though
			#	have to be careful for brackets
			input_text = self.unrollAliases(input_text)

			if not (input_text_expanded_vars := self.expandVariables(input_text)):
				sys.stderr.write(f"{Variables[VariablesEnum.shell_name]}: {input_text}: bad substitution\n")
				self._last_exit_code = 1
				continue
			else:
				input_text = input_text_expanded_vars

			try:
				command, *args = shlex.split(input_text, comments=True, posix=True)

			except ValueError as e:
				sys.stderr.write(f"{e.__class__.__name__}: {e}\n")
				continue

			args = [Path.expand(x) for x in args]

			try:
				if found_builtin := self._builtin_commands(command):
					self._last_exit_code = found_builtin(args) or 0

				else:
					proc = subprocess.run([command] + args, env=Variables.environment)
					self._last_exit_code = proc.returncode

			except FileNotFoundError:
				sys.stderr.write(f"{command}: command not found\n")
				self._last_exit_code = 1

			except KeyboardInterrupt:
				sys.stdout.write("\n")
				self._last_exit_code = 1

			except Exception as e:
				sys.stdout.write(f"{e.__class__.__name__}: {e}\n")
				self._last_exit_code = 1

		sys.exit(self._last_exit_code)
