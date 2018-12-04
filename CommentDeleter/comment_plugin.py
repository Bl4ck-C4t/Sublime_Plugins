import sublime
import sublime_plugin
from os import path
import re

class CommentdeleterCommand(sublime_plugin.TextCommand):
	def regex_compiler(self, multi_start, multi_end, single):
		single_r = "|{0}.*\\n*\\s*".format(single)
		#single_multi = "{0}.*{1}\\n*\\s*".format(multi_start, multi_end)
		multi_full = "({0}(.*\\n)*?.*{1}\\n*\\s*)".format(multi_start, multi_end)
		if single is None:
			single = ""
		if multi_start == None and multi_end == None:
			return single_r[1:]
		#return "(\\/\\*(.*\\n)*.*\\*\\/)|\\/\\/.+\\n\\s*"
		return "{}{}".format(multi_full, single_r)
			
	def run(self, edit, one_delete=False, files=[]):
		name = self.view.file_name()
		name = path.split(name)
		ext = name[1].split(".")[1]
		if ext in ["c", "cpp", "csharp"]:
			rg = self.regex_compiler("\\/\\*", "\\*\\/", "\\/\\/")
		if ext == "py":
			rg = self.regex_compiler(None, None, "#")
		if ext == "rb":
			rg = self.regex_compiler("=start", "=end", "#")
		if ext == "html":
			rg = self.regex_compiler("<!--", "-->", None)
		if ext == "css":
			rg = self.regex_compiler("\\/\\*", "\\*\\/", None)
		print("New Call")
		while True: #\/\*.*\*\/\n\s*|(\/\*(.*\n)+.*\*\/)|\/\/.+\n\s*
			


			#"\\/\\*.*\\*\\/\\n\\s*|(\\/\\*(.*\\n)+.*\\*\\/)|\\/\\/.+\\n\\s*"
			#print(rg)

			region = self.view.find(rg, 0)
			if region.empty():
				break
			print("COM:", self.view.substr(region))
			line = self.view.line(region.a)
			part = sublime.Region(line.a, region.a)
			if not(part.empty()):
				s_part = self.view.substr(part)				
				if not(s_part.isspace()):
					region.b = line.b

			
			self.view.erase(edit, region)
			if one_delete:
				break
			
