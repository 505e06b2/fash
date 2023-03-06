import re

from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Punctuation, Text, Comment, Operator, Keyword, Name, String, Number, Generic

#based on Pygments' BashLexer - https://github.com/pygments/pygments/blob/f589ac658924518894e18a38061eb00793a3b0a9/pygments/lexers/shell.py#L25
class Lexer(RegexLexer):
	tokens = {
		"root": [
			include("basic"),
			(r"`", String.Backtick, "backticks"),
			include("data"),
			include("interp")
		],
		"interp": [
			(r"\$\(", Keyword.Subshell, "subshell"),
			(r"\$\{", String.Interpol, "curly"),
			(r"\$[a-zA-Z_]\w*", Name.Variable), # user variable
			(r"\$(?:\d+|[#$?!_*@-])", Name.Variable), # builtin
			(r"\$", Text),

			(r"@\(", Keyword.Eval, "eval"),
			(r"@", Text),
		],
		"basic": [
			(r"\b(alias|cd|eval|exit|path)(?=[\s)`])", Keyword), #builtins
			(r"\b(chmod|chown|cp|dd|df|du|ln|ls|mkdir|mv|rm|rmdir|touch|basename|cat|comm|cut|dirname|echo|expand|"
				r"unexpand|false|fmt|fold|head|join|md5sum|paste|pr|seq|sleep|sort|split|tail|tee|test|tr|true|uniq|wc|yes|"
				r"date|env|groups|hostname|id|nice|pwd|su|uname|who|whoami|chgrp|cksum|csplit|dir|dircolors|expr|factor|"
				r"hostid|install|link|logname|mkfifo|mknod|nl|nohup|od|pathchk|pinky|printenv|printf|ptx|shred|stty|sum|"
				r"sync|tac|tsort|tty|unlink|users|vdir)(?=[\s)`])",
				Name.Builtin), #coreutils - https://wiki.debian.org/coreutils
			(r"\A#!.+\n", Comment.Hashbang),
			(r"#.*$", Comment.Single),
			(r"\\[\w\W]", String.Escape),
			(r"(\b\w+)(\s*)(\+?=)", bygroups(Name.Variable, Text, Operator)),
			(r"[\[\]{}()=]", Operator),
			(r"<<<", Operator),  # here-string
			(r"<<-?\s*(\'?)\\?(\w+)[\w\W]+?\2", String),
			(r"&&|\|\|", Operator),
		],
		"data": [
			(r"(?s)\$?\"(\\.|[^\"\\$@])*\"", String.Double),
			(r"\"", String.Double, "string"),
			(r"(?s)\$'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
			(r"(?s)'.*?'", String.Single),
			(r";", Punctuation),
			(r"&", Punctuation),
			(r"\|", Punctuation),
			(r"\s+", Text),
			(r"\d+\b", Number),
			(r"[^=\s\[\]{}()$@\"\'`\\<&|;]+", Text),
			(r"<", Text),
		],
		"string": [
			(r"\"", String.Double.End, "#pop"),
			(r"(?s)(\\\\|\\[0-7]+|\\.|[^\"\\$@])+", String.Double),
			include("interp")
		],
		"curly": [
			(r"\}", String.Interpol.End, "#pop"),
			(r":-", Keyword),
			(r"\w+", Name.Variable),
			(r"[^}:\"\'`$@\\]+", Punctuation),
			(r":", Punctuation),
			include("root"),
		],
		"subshell": [
			(r"\)", Keyword.Subshell.End, "#pop"),
			include("root"),
		],
		"eval": [
			(r"\)", Keyword.Eval.End, "#pop"),
			(r"[-+*/%^|&]|\*\*|\|\|", Operator),
			(r"\d+#\d+", Number),
			(r"\d+#(?! )", Number),
			(r"\d+", Number),
			include("root"),
		],
		"backticks": [
			(r"`", String.Backtick.End, "#pop"),
			include("root"),
		],
	}
