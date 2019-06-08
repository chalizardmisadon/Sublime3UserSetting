#!/usr/bin/env python
# import sublime
try:
	import sublime_plugin
except Exception:
	pass
import os

dirIgnore = [
	".svn",
	".git",
	".vscode",
	"build",
	"release",
	"/."
]

def addPredefinedPath():
	root = "."
	fd = open(".clang_complete", "w")
	for (directory, dirname, filename) in os.walk(root):
		if not any(ignore in directory for ignore in dirIgnore):
			fd.write("-I%s\n" % directory)
			# print(directory)
	fd.close()

def main():
	addPredefinedPath()
	# print("Generated .clang_complete")

try:
	class ClangCompleteGenCommand(sublime_plugin.WindowCommand):
		def run(self):
			dirVar = self.window.folders()[0]
			os.chdir(dirVar)
			main()
			print("Generated .clang_complete @ %s" % dirVar)
except Exception:
	print("Script is not running in a Sublime environment!\nGenerated .clang_complete in current script directory.")
	main()