#! /usr/bin/ python3 
import os 
import sys
import subprocess

def pathToString(path):
    #Remove the first slash
    return path[1:].replace("/", "-")

def getTmpDirPath():
    tmpDirName = pathToString(os.getcwd())

    return "/tmp/svn_stash/" + tmpDirName 
 
def isModified():
    result = subprocess.check_output(["svn", "status"])
    return len(result) > 0

def stash():
    if isModified() == False:
        print("No diff detected")
        return

    fullPath = getTmpDirPath()
    os.makedirs(fullPath, exist_ok=True)

    contents = os.listdir(fullPath)
    fileNumber = 1;
    if len(contents) > 0: 
        contents.sort(reverse = True)
        fileNumber = int(contents[0].split(".")[0]) + 1;

    fileName = str(fileNumber) + ".patch"

    fullPathAndFile = fullPath + "/" + fileName

    cmd = "svn diff --diff-cmd diff > {}; svn revert -R .".format(fullPathAndFile)
    os.system(cmd)

    print("Created stash")

def pop():
    fullPath = getTmpDirPath()
    if os.path.exists(fullPath) == False:
        print("No stash found")
        return

    contents = os.listdir(fullPath)

    if len(contents) < 1: 
        print("No stash found")
        return

    contents.sort(reverse = True)
    fullPathAndFile = fullPath + "/" + contents[0]
    cmd = "patch -p0 < {}".format(fullPathAndFile)
    os.system(cmd)
    os.system("rm " + fullPathAndFile)

    print("Applied stash. " + str(len(contents) - 1) + " stashes are still on the stack.")

if sys.argv[1] == "stash":
    stash()
else:
    pop()
