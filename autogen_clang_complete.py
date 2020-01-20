#!/usr/bin/env python
# import sublime
try:
	import sublime_plugin
except Exception:
	pass
import os


# ========================= Directory Dictionaries ========================= #

dirIgnore = [
	# ".svn",
	# ".git",
	# ".vscode",
	"build",
	"release",
	".",
]

dirInclude = [
	# ".vscode",
	".local",
]


dirArduino = {
	"comment": "Adding Arduino paths using Platformio packages",
	"path": [
		# "~/.platformio/packages/framework-arduinoteensy/cores/arduino/",
		# "~/.platformio/packages/framework-arduinoteensy/libraries/__cores__/arduino/",
		# "~/.platformio/packages/framework-arduinoteensy/cores/",
		"~/.local/share/umake/ide/arduino/hardware/arduino/avr/cores/arduino/",
		"~/.local/share/umake/ide/arduino/hardware/arduino/avr/libraries/",
		"~/.local/share/umake/ide/arduino/hardware/tools/avr/avr/include/",
		"~/.local/share/umake/ide/arduino/libraries/",
		# "~/.local/share/umake/ide/arduino/tools/"
	]
}

dirSTM32 = {
	"comment": "Adding STM32 driver paths within ~/STM32Cube directory",
	"path": [
		"~/STM32Cube/Repository/STM32Cube_FW_L4_V1.14.0/Drivers/",
		# "~/STM32Cube/Repository/STM32Cube_FW_L4_V1.14.0/Drivers/STM32L4xx_HAL_Driver/",
		# "~/STM32Cube/Repository/STM32Cube_FW_L4_V1.14.0/Drivers/CMSIS/Device/",
	]
}


dirExtraLib = [
	dirArduino,
	dirSTM32
]


# ========================= Search Algorithm ========================= #

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
		if (dirpath == currDir):
			subdirs[:] = [d for d in subdirs if d != childDir]
		subdirs[:] = [d for d in subdirs if all(i not in d for i in dirIgnore) or any(i in d for i in dirInclude)]
		fd.write("-I%s\n" % dirpath)

	addFileToRootSearch(fd, os.path.dirname(currDir), os.path.basename(currDir))


def checkFileExistPath(fd, newPath):
	fd.seek(0)  # reset file pointer to beginning
	line = fd.readlines()
	path = [p for p in newPath if all(p not in l for l in line)]
	# print(line)
	# print(path)
	return path


def addSpecificPath(fd, root, userPath=""):
	for (dirpath, subdirs, files) in os.walk(root):
		subdirs[:] = [d for d in subdirs if all(i not in d for i in dirIgnore) or any(i in d for i in dirInclude)]
		fd.write("-I%s\n" % dirpath.replace(userPath, "~"))


def addExtraLibPath(fd, userPath=""):
	for lib in dirExtraLib:
		print(lib["comment"])
		path = checkFileExistPath(fd, lib["path"])
		for p in path:
			addSpecificPath(fd, p.replace("~", userPath), userPath)


def main():
	with open(".clang_complete", "w") as fd:
		addPreOrderSearch_v2(fd)
	printFinishGen()


def printFinishGen():
	print("Generated .clang_complete @ \"%s\"" % os.getcwd())



# ========================= Sublime Plugins ========================= #

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
			with open(".clang_complete", "w") as fd:
				addFileToRootSearch(fd, "./" + os.path.relpath(projVar["file_path"], projVar["folder"]))
			printFinishGen()

		def addPreOrderSearch(self):
			projVar = self.window.extract_variables()
			os.chdir(projVar["folder"])
			with open(".clang_complete", "w") as fd:
				addPreOrderSearch_v2(fd)
			printFinishGen()

	class GenClangExtraLibCommand(sublime_plugin.WindowCommand):
		def run(self):
			self.addExtraLibPath()

		def addExtraLibPath(self):
			userPath = os.path.expanduser("~")
			with open(".clang_complete", "a+") as fd:
				addExtraLibPath(fd, userPath)
			printFinishGen()


except Exception:
	print(
		"Script is not running in a Sublime environment!\n"
		"Generated .clang_complete in current script directory."
	)
	main()