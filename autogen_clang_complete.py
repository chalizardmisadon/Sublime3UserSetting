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


def addPreOrderSearch_v1(fd):
	print("File is generated using Pre Order Searching v1. Loop through all directories.")
	root = "./"
	for (dirpath, subdirs, files) in os.walk(root):
		if not any(ignore in dirpath for ignore in dirIgnore):
			fd.write("-I%s\n" % dirpath)


def addPreOrderSearch_v2(fd):
	print("File is generated using Pre Order Searching v2. Skip all ignored directories")
	root = "./"
	for (dirpath, subdirs, files) in os.walk(root):
		subdirs[:] = [d for d in subdirs if d not in dirIgnore]
		fd.write("-I%s\n" % dirpath)


def addFileToRootSearch(fd, currDir, childDir=''):
	if (currDir == ''):
		print("Root Folder reached in recursive search.")
		return

	for (dirpath, subdirs, files) in os.walk(currDir, topdown=True):
		if (dirpath in currDir):
			subdirs[:] = [d for d in subdirs if d not in childDir]
		subdirs[:] = [d for d in subdirs if d not in dirIgnore]
		fd.write("-I%s\n" % dirpath)

	addFileToRootSearch(fd, os.path.dirname(currDir), os.path.basename(currDir))


def main():
	fd = open(".clang_complete", "w")
	addPreOrderSearch_v2(fd)
	fd.close()
	printFinishGen()


def printFinishGen():
	print("Generated .clang_complete @ \"%s\"" % os.getcwd())


try:
	class GenClangCompleteCommand(sublime_plugin.WindowCommand):
		def run(self):
			self.addFileToRootSearch()

		def addFileToRootSearch(self):
			projVar = self.window.extract_variables()
			if projVar["folder"] not in projVar["file_path"]:
				print("\nCurrent opened Folder \"%s\"\ndoes not contain File \"%s\"\n" % (projVar["folder"], projVar["file_path"]))
				return
			
			os.chdir(projVar["folder"])
			fd = open(".clang_complete", "w")
			addFileToRootSearch(fd, "./" + os.path.relpath(projVar["file_path"], projVar["folder"]))
			fd.close()
			printFinishGen()

		def addPreOrderSearch(self):
			projVar = self.window.extract_variables()
			os.chdir(projVar["folder"])
			fd = open(".clang_complete", "w")
			addPreOrderSearch_v2(fd)
			fd.close()
			printFinishGen()


except Exception:
	print("Script is not running in a Sublime environment!\nGenerated .clang_complete in current script directory.")
	main()