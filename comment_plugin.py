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
			if ext == "c":
				single = "//"
				multi_start = "/*"
				multi_end = "*/"

			#rg = re.compile("\\/\\*.*\\*\\/\n\\s*|(\\/\\*(.*\n)+.*\\*\\/)|\\/\\/.+\n\\s*")
			region = self.view.find(r'\/\*.*\*\/\n\s*|(\/\*(.*\n)+.*\*\/)|\/\/.+\n\s*', 0)
			if region.empty():
				break
			self.view.erase(edit, region)
			

			

