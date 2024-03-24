def openFile():
    with open(filePath, "r") as file:
        lines = file.readlines()
    # print(lines)
    return lines

runningTotal = 0
def totalDelete(folderNum: str):
    allFolder.remove(folderNum)
    global runningTotal

    file = open(filePath, "r")
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    lineStart = lines.index("Folder: " + folderNum)
    lineEnd = len(lines)
    nextFolder = "Folder: " + str(int(folderNum) + 1)
    if nextFolder in lines:
        lineEnd = lines.index(nextFolder)

    currentTotal = 0
    folderInside = []
    for line in lines[lineStart:lineEnd]:
        if line.startswith("-"):
            line_parts = line.split()
            if len(line_parts) == 3:
                currentTotal += int(line_parts[-1])
            if line_parts[-2] == "[FOLDER":
                folderInside.append(line_parts[-1][:-1])
    runningTotal += currentTotal

    while len(folderInside)>0:
        folder = folderInside.pop()
        extraData, extraFolder = totalDelete(folder)
        currentTotal += extraData
        if extraFolder is not None:
            folderInside.append(extraFolder)

    if folderInside == []:
        return runningTotal, None
    return runningTotal, folderInside

def normalTraversal(folderNum: str):
    file = open(filePath, "r")
    lines = file.readlines()
    lines = [x.strip() for x in lines]
    file.close()

    lineStart = lines.index("Folder: " + folderNum)
    lineEnd = len(lines)
    nextFolder = "Folder: " + str(int(folderNum) + 1)
    if nextFolder in lines:
        lineEnd = lines.index(nextFolder)

    currentTotal = 0
    folderInside = []
    for line in lines[lineStart:lineEnd]:
        if line.startswith("-"):
            line_parts = line.split()
            if (line.find("temporary") != -1 or line.find("delete") != -1):
                if len(line_parts) == 3:
                    currentTotal += int(line_parts[-1])
                if line_parts[-2] == "[FOLDER":
                    folderInside.append(line_parts[-1][:-1])
    return currentTotal, folderInside
#______________________________________________________________________________________________________________________#
"""
MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAINMAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN MAIN
"""

global filePath
filePath = "input7.txt"
global totalBytes
totalBytes = 0
global allFolder
allFolder = [x for x in range(5175, -1, -1)]
allFolder = [str(x) for x in allFolder]

while allFolder:
    lines = openFile()
    # [print(line) for line in lines]
    currentFolder = allFolder.pop()
    result, tempdelFolders = normalTraversal(currentFolder)
    totalBytes += result
    for folder in tempdelFolders:
        result, dummy = totalDelete(folder)
    totalBytes += runningTotal
    print("OVERALL FILE TOTAL:", totalBytes)
    runningTotal = 0
    print("___________________________________________________________________________________________________________")


print(totalBytes)