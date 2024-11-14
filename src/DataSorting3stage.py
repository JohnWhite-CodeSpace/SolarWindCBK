import os
import pathlib
import re



def ProcessHiTimes(self,Terminal, ProgressBar, ProgressLabel, SourceDirectory, SortedDirectory):
    # with open("HiCullGoodTimes", "r") as GoodHi:
    #     HIList = GoodHi.readlines()
    #     GoodHi.close()
    # for line in HIList:
    #     if not line.startswith("#") and line.strip():
    #         conditions = re.split("\s+", line)
    #         if len(conditions)>=11:
    #             ProgressLabel.setText(f"Processing data conditions: {line}")
    #             paths = GetHiDir(SourceDirectory, SortedDirectory, conditions)
    #             ProcessDataHi(self,conditions, paths[1], paths[0], Terminal, paths[2], ProgressBar)
    SumUpHi(self, Terminal,ProgressBar,ProgressLabel,SortedDirectory)
    # CheckDoubleObservation(SourceDirectory, SortedDirectory)

def GetHiDir(SourceDirectory, SortedDirectory, Conditions):
    CorrectFP = None
    pathG = None
    directory = None
    foldertype = Conditions[0]
    for root, dirs, files in os.walk(SourceDirectory):
        for dir in dirs:
            if foldertype in dir and int(Conditions[3]) ==0 and int(Conditions[4]) ==59 and int(Conditions[12])==2:
                CorrectFP = pathlib.Path(SortedDirectory) / pathlib.Path(os.path.relpath(root, SourceDirectory)) / dir
                pathlib.Path(CorrectFP).mkdir(parents=True, exist_ok=True)
                pathG = os.path.join(root, dir)
                directory = dir
    return CorrectFP, pathG, directory
def ProcessDataHi(self,Conditions, pathG, CorrectPath, Terminal, subdirectory, ProgressBar):
    Strgoodfiles = [Conditions[6], Conditions[7], Conditions[8],
    Conditions[9], Conditions[10], Conditions[11]]
    Intgoodfiles = [int(x) for x in Strgoodfiles]
    count = 0
    ProgressBar.setMaximum(len(Intgoodfiles))
    self.update_progress_signal.emit(count, 1)
    lines = 0
    nums = None
    for openf in Intgoodfiles:
        count += 1
        if openf==1 and subdirectory is not None:
            filepath = f"{pathG}{os.path.sep}{subdirectory}.hide-{count}.txt"
            Terminal.append(f"Processing file: {filepath}")
            try:
                with open(filepath, "r") as file:
                    nums = os.path.join(CorrectPath, "GoodTimesCounterHi.txt")
                    out = os.path.join(CorrectPath, os.path.basename(file.name))
                    lines = file.readlines()
                    file.close()
                    ProcessLinesHi(lines, out, nums, Conditions)
            except FileNotFoundError:
                pass
        self.update_progress_signal.emit(count, 1)


def ProcessLinesHi(lines, OutputFile, CounterFile, Conditions):
    goodlines = 0
    GoodTimes = []
    if not os.path.isfile(CounterFile):
        with open(CounterFile, "a") as Fcount:
            Fcount.writelines("T1 (UTC): \t T2 (UTC): \t Count: \t Freq: \t Location: \n")
            Fcount.close()
    if len(lines)>0:
        for line in lines:
            temparray = re.split("\s+", line)
            if float(Conditions[1]) <= float(temparray[0]) <= float(Conditions[2]):
                GoodTimes.append(line)
                goodlines += 1
        with open(OutputFile, "a") as Out:
            for i in GoodTimes:
                Out.write(i)
            Out.close()
        with open(CounterFile, "a") as Fcount:
            deltaT = float(Conditions[2]) - float(Conditions[1])
            freq = goodlines/deltaT
            Fcount.writelines(Conditions[1] + "\t" + Conditions[2] + "\t" + str(goodlines) + "\t" + str(freq) + "\t" + OutputFile + "\n")
            Fcount.close()

def ProcessLoTimes(self,Terminal, ProgressBar, ProgressLabel, SourceDirectory, SortedDirectory):
    # with open("LoGoodTimes.txt", "r") as GoodLo:
    #     LoList = GoodLo.readlines()
    #     GoodLo.close()
    # for line in LoList:
    #     if not line.startswith("#") and line.strip():
    #         conditions = re.split("\s+", line)
    #         if len(conditions)>=11:
    #             ProgressLabel.setText(f"Processing data conditions: {line}")
    #             paths = GetLoDir(SourceDirectory, SortedDirectory, conditions)
    #             ProcessDataLo(self,conditions, paths[1], paths[0], Terminal, paths[2], ProgressBar)
    SumUpLo(self, Terminal, ProgressBar, ProgressLabel, SortedDirectory)
def GetLoDir(SourceDirectory, SortedDirectory, Conditions):
    CorrectFP = None
    pathG = None
    directory = None
    foldertype = Conditions[0]
    for root, dirs, files in os.walk(SourceDirectory):
        for dir in dirs:
            if foldertype in dir and int(Conditions[3]) ==0 and int(Conditions[4]) ==59:
                CorrectFP = pathlib.Path(SortedDirectory) / pathlib.Path(os.path.relpath(root, SourceDirectory)) / dir
                pathlib.Path(CorrectFP).mkdir(parents=True, exist_ok=True)
                pathG = os.path.join(root, dir)
                directory = dir
    return CorrectFP, pathG, directory
def ProcessDataLo(self,Conditions, pathG, CorrectPath, Terminal, subdirectory, ProgressBar):
    Strgoodfiles = [Conditions[6], Conditions[7], Conditions[8],
    Conditions[9], Conditions[10], Conditions[11], Conditions[12], Conditions[13]]
    Intgoodfiles = [int(x) for x in Strgoodfiles]
    count = 0
    ProgressBar.setMaximum(len(Intgoodfiles))
    self.update_progress_signal.emit(count, 2)
    lines = 0
    out = []
    nums = None
    for openf in Intgoodfiles:
        count += 1
        if openf==1 and subdirectory is not None:
            filepath = f"{pathG}{os.path.sep}{subdirectory}.lode-{count}.txt"
            Terminal.append(f"Processing file: {filepath}")
            try:
                with open(filepath, "r") as file:
                    nums = os.path.join(CorrectPath, "GoodTimesCounterLo.txt")
                    out = os.path.join(CorrectPath, os.path.basename(file.name))
                    lines = file.readlines()
                    file.close()
                    ProcessLinesLo(lines, out, nums, Conditions)
            except FileNotFoundError:
                pass
        self.update_progress_signal.emit(count, 2)


def ProcessLinesLo(lines, OutputFile, CounterFile, Conditions):
    goodlines = 0
    GoodTimes = []
    if not os.path.isfile(CounterFile):
        with open(CounterFile, "a") as Fcount:
            Fcount.writelines("T1 (UTC): \t T2 (UTC): \t Count: \t Freq: \t Location: \n")
            Fcount.close()
    if len(lines)>0:
        for line in lines:
            temparray = re.split("\s+", line)
            if float(Conditions[1]) <= float(temparray[0]) <= float(Conditions[2]):
                GoodTimes.append(line)
                goodlines += 1
        with open(OutputFile, "a") as Out:
            for i in GoodTimes:
                Out.write(i)
            Out.close()
        with open(CounterFile, "a") as Fcount:
            deltaT = float(Conditions[2]) - float(Conditions[1])
            freq = goodlines/deltaT
            Fcount.writelines(Conditions[1] + "\t" + Conditions[2] + "\t" + str(goodlines) + "\t" + str(freq) + "\t" + OutputFile + "\n")
            Fcount.close()



def SumUpHi(self, Terminal, ProgressBar, ProgressLabel, SourceDirectory):
    Terminal.append("Summing up Hi GoodTimes...")
    for root, dirs, files in os.walk(SourceDirectory):
        for file in files:
            if file.endswith("CounterHi.txt"):
                filepath = os.path.join(root,file)
                with open(filepath, "r") as counter:
                    next(counter)
                    lines = counter.read().split('\n')
                    counter.close()
                path = os.path.join(root,"SumHICorrect.txt")
                ProgressLabel.setText(f"Summing up file: {file}")
                CalcSumHi(self,lines,path, ProgressBar)

def CalcSumHi(self, lines, path, ProgressBar):
    hide_counts = {}
    for line in lines:
        fields = re.split('\t', line)
        location = fields[-1]
        print(f"{fields}+\n")
        hide_file = re.search(r'hide-(\d+).txt', location)
        if hide_file:
            multiplyer = 1/6
            if "hide-3.txt" in location:
                if GetMultiplyerConstant(os.path.abspath(location)):
                    multiplyer = 1/3
            hide_number = hide_file.group(1)
            countT = int(fields[2])
            deltaT = float(fields[1]) - float(fields[0])
            hide_counts[hide_number] = hide_counts.get(hide_number, (0, 0, 0))
            hide_counts[hide_number] = (
                hide_counts[hide_number][0] + countT,
                hide_counts[hide_number][1] + deltaT,
                multiplyer
            )
    with open(path, "a") as sum:
        sum.write("File:\tCount:\tInverse Delta T:\t Frequency [counts/deltaT]:\t Multiplyer:\n")
        for hide_number, (count, invdelta, mul) in hide_counts.items():
            sum.write(f"hide-{hide_number}\t{count}\t{invdelta}\t{mul*(count/invdelta)}\t{mul}\n")

def SumUpLo(self, Terminal, ProgressBar, ProgressLabel, SourceDirectory):
    Terminal.append("Summing up Lo GoodTimes...")
    for root, dirs, files in os.walk(SourceDirectory):
        for file in files:
            if file.endswith("CounterLo.txt"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as counter:
                    next(counter)
                    lines = counter.read().split('\n')
                    counter.close()
                path = os.path.join(root,"SumLoCorrect.txt")
                ProgressLabel.setText(f"Summing up file: {file}")
                CalcSumLo(self,lines,path, ProgressBar)
def CalcSumLo(self, lines, path, ProgressBar):
    lode_counts = {}
    for line in lines:
        fields = re.split('\t', line)
        location = fields[-1]
        #print(f"{fields}+\n")
        lode_file = re.search(r'lode-(\d+).txt', location)
        if lode_file:
            lode_number = lode_file.group(1)
            countT = int(fields[2])
            deltaT = float(fields[1]) - float(fields[0])
            lode_counts[lode_number] = lode_counts.get(lode_number, (0, 0))
            lode_counts[lode_number] = (
                lode_counts[lode_number][0] + countT,
                lode_counts[lode_number][1] + deltaT
            )
    with open(path, "a") as sum:
        sum.write("File:\tCount:\tInverse Delta T:\t Frequency [counts/deltaT]:\n")
        for lode_number, (count, invdelta) in lode_counts.items():
            sum.write(f"lode-{lode_number}\t{count}\t{invdelta}\t{1/8*(count / invdelta)}\n")




def GetMultiplyerConstant(HideFile):
    IsObservedTwice = False
    with open("../instruction_files/DoubleObservationCheck.txt", 'r') as CheckDoubleFile:
        lines = CheckDoubleFile.readlines()
    CheckDoubleFile.close()
    for line in lines:
        if "Channel 3 was observed twice in" in line:
            dirinfo = line.split("Channel 3 was observed twice in ")
            dirtype = dirinfo[1].split('.')[0]
            print(dirtype + "   " + HideFile)
            if dirtype in HideFile:
                IsObservedTwice = True
                print("match!!!")
                break
    return IsObservedTwice












