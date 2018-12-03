import sublime
import sublime_plugin
from os import path
import re

class CommentdeleterCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		while True: #\/\*.*\*\/\n\s*|(\/\*(.*\n)+.*\*\/)|\/\/.+\n\s*
			name = self.view.file_name()
			name = path.split(name)
			ext = name[1].split(".")[1]
			if ext in ["c", "cpp", "csharp"]:
				single = "\\/\\/"
				multi_start = "\\/\\*"
				multi_end = "\\*\\/"

			#"\\/\\*.*\\*\\/\\n\\s*|(\\/\\*(.*\\n)+.*\\*\\/)|\\/\\/.+\\n\\s*"
			rg = "{0}.*{1}\\n\\s*|({0}(.*\\n)+.*{1})|{2}.+\\n\\s*".format(multi_start, multi_end, single)
			print(rg)
			region = self.view.find(rg, 0)
			if region.empty():
				break
			self.view.erase(edit, region)
			
