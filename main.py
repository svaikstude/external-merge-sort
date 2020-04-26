import os
import shutil
import tempfile
import glob

tempDir = os.path.join(os.getcwd(), "temp")
if os.path.exists(tempDir):
    shutil.rmtree(tempDir)
os.makedirs(tempDir)


def splitFile(fileName):
    with open(fileName) as f:
        for number in f:
            tempFile = tempfile.NamedTemporaryFile(dir=tempDir, delete=False, mode="w+")
            tempFile.write(number)
            tempFile.seek(0)


def compareTwoFiles(file1, file2):
    tempFile = tempfile.NamedTemporaryFile(dir=tempDir, delete=False, mode="w+")
    x = file1.readline()
    y = file2.readline()
    while True:
        if not x and not y:
            break
        elif not x:
            tempFile.write(y)
            for line in file2:
                tempFile.write(line)
            break
        elif not y:
            tempFile.write(x)
            for line in file1:
                tempFile.write(line)
            break

        if int(y.strip()) < int(x.strip()):
            tempFile.write(y)
            y = file2.readline()
        else:
            tempFile.write(x)
            x = file1.readline()

    tempFile.seek(0)
    file1.close()
    file2.close()


def mergeFiles(tempDir):
    while True:
        index = 1
        file1 = None
        file2 = None
        for fileName in glob.iglob(tempDir + "/*"):
            if index % 2 != 0:
                file1 = os.path.join(tempDir, fileName)
            else:
                file2 = os.path.join(tempDir, fileName)
                # try:
                compareTwoFiles(open(file1), open(file2))
                # except FileNotFoundError:
                #     break
                os.remove(file1)
                os.remove(file2)
                file1 = None
                file2 = None
            index += 1
        if index == 2:
            return


splitFile("largefile")
mergeFiles(tempDir)
