#!/usr/bin/env python
# import sublime
try:
	import sublime_plugin
except Exception:
	pass
import os

gitIgnore = []

clang = {
	"comment": "clang intellisense",
	"ignore": [".clang_complete"]
}

directories = {
	"comment": "ignore directories",
	"ignore": [
		".directory",
		".svn",
		".vscode",
		".*/",
		"**/release",
		"**/build",
		"Deviot/"
	]
}

files = {
	"comment": "ignore files",
	"ignore": [
		"*.patch",
		"*.o",
		"deviot.*"
	]
}

makefiles = {
	"comment": "include makefiles",
	"include": [
		"Makefile",
		"makefile",
		"*.mk",
		"*.make"
	]
}

sublime = {
	"comment": "ignore sublime cache",
	"ignore": [
		"Package Control*",
		"PythonTestRunner*",
		"Preferences.sublime-settings"
	]
}

gitIgnore = [
	clang,
	directories,
	files,
	makefiles,
	sublime
]

def addGitIgnoreRules(fd):
	for dictionary in gitIgnore:
		if "comment" in dictionary:
				fd.write("# %s\n" % dictionary["comment"])  # add comment of type
		if "ignore" in dictionary:
			for ignore in dictionary["ignore"]:  # add files to ignore
				fd.write("%s\n" % ignore)
		if "include" in dictionary:
			for include in dictionary["include"]:  # add files to NOT ignore
				fd.write("!%s\n" % include)
		fd.write("\n")

def main():
	fd = open(".gitignore", "w")
	addGitIgnoreRules(fd)
	fd.close()
	# print("Generated .clang_complete")

try:
	class GenGitignoreCommand(sublime_plugin.WindowCommand):
		def run(self):
			dirVar = self.window.folders()[0]
			os.chdir(dirVar)
			main()
			print("Generated .gitignore @ %s" % dirVar)
except Exception:
	print("Script is not running in a Sublime environment!\nGenerated .gitignore in current script directory.")
	main()
	if "sublime-text" in os.getcwd():
		gitIgnore = [sublime]
		fd = open(".gitignore", "a")
		addGitIgnoreRules(fd)
		fd.close()