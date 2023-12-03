import os
import pathlib
import re
import threading
import time


def ProcessGoodTimesHi(self, Terminal, SourceDirectory,SortedDirectory, ProgressBar, Progress):
    Terminal.append(f"Chosen source directory: {SourceDirectory}")
    Terminal.append("Collecting Hi good data...")
    with open("HiCullGoodTimes", "r") as GoodDataList:
        lines = GoodDataList.readlines()
        count = 0
        datasize = len(lines)
        self.update_progress_signal.emit(count)
        ProgressBar.setMaximum(datasize)
        for line in lines:
            try:
                count += 1
                self.update_progress_signal.emit(count)
            except Exception as e:
                Terminal.append(f"An error occurred while updating progress: {str(e)}")
                time.sleep(0.1)
                continue
            if not line.startswith("#"):
                conditions = re.split("\s+",line)
                Progress.setText(f"Processing data conditions: {line}")
                if len(conditions)>=10:
                    ConditionLogicHi(conditions, SourceDirectory, SortedDirectory)
    Terminal.append("Finished processing HiGoodTimes data type.")
    Terminal.append("Initialising LoGoodTimes data type processing...")
    threading.Thread(target = ProcessGoodTimesLo, args=(self,Terminal, SourceDirectory, SortedDirectory, ProgressBar,Progress)).start()
def ConditionLogicHi(Conditions, SourceDirectory, SortedDirectory):
    foldertype = Conditions[0]
    for root, dirs, files in os.walk(SourceDirectory):
        for dir in dirs:
            if foldertype in dir:
                if int(Conditions[3]) ==0 and int(Conditions[4]) ==59 and int(Conditions[12])==2:
                    CorrectFP = os.path.join(SortedDirectory,os.path.relpath(root,SourceDirectory))
                    CorrectPath = os.path.join(CorrectFP,dir)
                    pathlib.Path(CorrectPath).mkdir(parents=True, exist_ok=True)
                    pathG = os.path.join(root,dir)
                    OpenSpecificFilesHi(Conditions, pathG, CorrectPath,dir)

def OpenSpecificFilesHi(Conditions, pathG, CorrectPath,dir):
    if Conditions[5] == "Hi":
        Strgoodfiles = [Conditions[6], Conditions[7], Conditions[8],
        Conditions[9], Conditions[10], Conditions[11]]
        Intgoodfiles = [int(x) for x in Strgoodfiles]
        count =0
        for openf in Intgoodfiles:
            count+=1
            if openf == 1:
                filepath = pathG+"/"+dir+".hide-"+str(count)+".txt"
                if os.path.exists(filepath):
                    file = open(filepath, "r")
                    ReadSpecificFileHi(file, Conditions, CorrectPath)
                    file.close()

def ReadSpecificFileHi(fileD, Conditions,CorrectFP):
    lines = fileD.readlines()
    out = os.path.join(CorrectFP, os.path.basename(fileD.name))
    for line in lines:
        temparray = re.split("\s+", line)
        if float(Conditions[1]) <= float(temparray[0]) <= float(Conditions[2]):
            with open(out, "a") as output_file:
                output_file.write(line + "\n")




def ProcessGoodTimesLo(self, Terminal, SourceDirectory,SortedDirectory, ProgressBar, Progress):
    Terminal.append(f"Chosen source directory: {SourceDirectory}")
    Terminal.append("Collecting Hi good data...")
    with open("LoGoodTimes.txt", "r") as GoodDataList:
        lines = GoodDataList.readlines()
        count = 0
        datasize = len(lines)
        self.update_progress_signal.emit(count)
        ProgressBar.setMaximum(datasize)
        for line in lines:
            try:
                count += 1
                self.update_progress_signal.emit(count)
            except Exception as e:
                Terminal.append(f"An error occurred while updating progress: {str(e)}")
                time.sleep(0.1)
                continue
            if not line.startswith("#"):
                conditions = re.split("\s+",line)
                Progress.setText(f"Processing data conditions: {line}")
                if len(conditions)>=12:
                    ConditionLogicLo(conditions, SourceDirectory, SortedDirectory)
    Terminal.append("Finished third stage data processing successfully.")
def ConditionLogicLo(Conditions, SourceDirectory, SortedDirectory):
    foldertype = Conditions[0]
    for root, dirs, files in os.walk(SourceDirectory):
        for dir in dirs:
            if foldertype in dir:
                if int(Conditions[3]) ==0 and int(Conditions[4]) ==59:
                    CorrectFP = os.path.join(SortedDirectory,os.path.relpath(root,SourceDirectory))
                    CorrectPath = os.path.join(CorrectFP,dir)
                    pathlib.Path(CorrectPath).mkdir(parents=True, exist_ok=True)
                    pathG = os.path.join(root,dir)
                    OpenSpecificFilesLo(Conditions, pathG, CorrectPath,dir)


def OpenSpecificFilesLo(Conditions, pathG, CorrectPath,dir):
    if Conditions[5] == "Lo":
        Strgoodfiles = [Conditions[6], Conditions[7], Conditions[8],
        Conditions[9], Conditions[10], Conditions[11], Conditions[12], Conditions[13]]
        Intgoodfiles = [int(x) for x in Strgoodfiles]
        count =0
        for openf in Intgoodfiles:
            count+=1
            if openf == 1:
                filepath = pathG+"/"+dir+".lode-"+str(count)+".txt"
                if os.path.exists(filepath):
                    file = open(filepath, "r")
                    ReadSpecificFileLo(file, Conditions, CorrectPath)
                    file.close()

def ReadSpecificFileLo(fileD, Conditions,CorrectFP):
    lines = fileD.readlines()
    out = os.path.join(CorrectFP, os.path.basename(fileD.name))
    for line in lines:
        temparray = re.split("\s+", line)
        if float(Conditions[1]) <= float(temparray[0]) <= float(Conditions[2]):
            with open(out, "a") as output_file:
                output_file.write(line + "\n")
