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
		"**/build/*",  # don't ignore all files
	]
}

files = {
	"comment": "ignore files",
	"ignore": [
		"*.patch",
		"*.o",
		"*.symlink", # gitignore treat symlinks as files
		"*.bak",
	]
}

makefiles = {
	"comment": "include makefiles",
	"include": [
		"Makefile",
		"makefile",
		"*.mk",
		"*.make",
		"build/Makefile",
		"build/makefile",
		"build/*.mk",
		"build/*.make",
		"makerules"
	]
}

sublime_cache = {
	"comment": "ignore sublime cache",
	"ignore": [
		"Package Control*",
		"PythonTestRunner*",
		"Preferences.sublime-settings"
	]
}

sublime_packages = {
	"comment": "ignore sublime packages",
	"ignore": [
		"SBSCompare*",
	]
}

sublime_languages = {
	"comment": "ignore sublime languages",
	"ignore": [
		"R.sublime-settings",
		"ARM Assembly.sublime-settings",
	]
}

platformio = {
	"comment": "ignore / include platformio",
	"ignore": [
		"Deviot/",
		"deviot.*",
		".travis.yml",
	]
}

gitIgnore = [
	clang,
	directories,
	files,
	makefiles,
	platformio
]

def addGitIgnoreRules(fd, ignore):
	for dictionary in ignore:
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
	addGitIgnoreRules(fd, gitIgnore)
	fd.close()

def sublime_gitignore():
	if "sublime-text" in os.getcwd():
		sublimeIgnore = [
			sublime_cache,
			sublime_packages,
			sublime_languages,
		]
		fd = open(".gitignore", "a")
		addGitIgnoreRules(fd, sublimeIgnore)
		fd.close()

# start of program here
try:
	class GenGitignoreCommand(sublime_plugin.WindowCommand):
		def run(self):
			dirVar = self.window.folders()[0]
			os.chdir(dirVar)
			main()
			sublime_gitignore()
			print("Generated .gitignore @ %s" % dirVar)
except Exception:
	print("Script is not running in a Sublime environment!\nGenerated .gitignore in current script directory.")
	main()
	sublime_gitignore()
