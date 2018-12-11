import sublime
import sublime_plugin
from os import path


class Comment:
	types = []
	def regex_compiler(self, multi_start, multi_end, single):
		single_r = "|(?<!['\"]){0}.*\\n?".format(single)
		multi_full = "((?<!['\"]){0}(.*\\n)*?.*{1}\\n?)".format(multi_start, multi_end)
		if single is None:
			single = ""
		if multi_start == None and multi_end == None:
			return single_r[1:]
		return "{}{}".format(multi_full, single_r)

	def __init__(self, multi_start, multi_end, single, ext):
		self.ext = ext
		self.regex = self.regex_compiler(multi_start, multi_end, single)
		self.types.append(self)

Comment("\\/\\*", "\\*\\/", "\\/\\/", ["c", "cpp", "csharp", "rs", "hh", "cc"])
Comment(None, None, "#", ["py"])
Comment("=start", "=end", "#", ["rb"])
Comment("<!--", "-->", None, ["html"])
Comment("\\/\\*", "\\*\\/", None, ["css"])
Comment(None, None, ";", ["scm", "asm"])
Comment(None, None, ";;", ["clj"])
Comment(None, None, "%", ["prolog"])
Comment(None, None, "--", ["hs"])


def inComment(strings, region):
	return any(filter(lambda x: x.contains(region.a), strings))



class CommentDeleterCommand(sublime_plugin.TextCommand):
	
			
	def build_comment(self):
		name = self.view.file_name()
		if name is None:
			raise Exception("Not in a view")
		name = path.split(name)
		ext = name[1].split(".")[1]
		comments = [x for x in Comment.types if ext in x.ext]
		if len(comments) == 0:
			raise Exception("Extension '.{}' not supported.".format(ext))
		return comments[0]
		

	def run(self, edit, one_delete=False, from_cursor_pos=False, files=[]):
		
		start_pos = self.view.sel()[0].begin() if from_cursor_pos else 0
		removed=0
		comment = self.build_comment()
		while True:
			strings = self.view.find_all(r'(["\']).*\1', 0)
			region = self.view.find(comment.regex, start_pos)
			if region.empty():
				break
			if inComment(strings, region):
				start_pos = region.b
				continue
			line = self.view.line(region.a)
			part = sublime.Region(line.a, region.a)
			part2 = sublime.Region(region.b, line.b)
			s_before = self.view.substr(part)	
			s_after = self.view.substr(part2)
			clear_space = False
			if not(part.empty()):
				if s_before.isspace() and s_after.isspace():
					clear_space = True
				elif not(s_before.isspace()):
					region.b = line.b

			self.view.erase(edit, region)
			
			if clear_space:
				self.view.erase(edit, part)
			removed+=1
			if one_delete or removed >= 600:
				break
			
		print("Removed {} comment{}.".format(removed, "s" if removed > 1 else ""))
			
