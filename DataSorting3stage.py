import os
import pathlib
import re



def ProcessHiTimes(self,Terminal, ProgressBar, ProgressLabel, SourceDirectory, SortedDirectory):
    with open("HiCullGoodTimes", "r") as GoodHi:
        HIList = GoodHi.readlines()
        GoodHi.close()
    for line in HIList:
        if not line.startswith("#") and line.strip():
            conditions = re.split("\s+", line)
            if len(conditions)>=11:
                ProgressLabel.setText(f"Processing data conditions: {line}")
                paths = GetHiDir(SourceDirectory, SortedDirectory, conditions)
                ProcessDataHi(self,conditions, paths[1], paths[0], Terminal, paths[2], ProgressBar)
    SumUpHi(self, Terminal,ProgressBar,ProgressLabel,SortedDirectory)

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
                    ProcessLinesHi(self, lines, out, nums, Conditions, ProgressBar)
                    file.close()
            except FileNotFoundError:
                pass
        self.update_progress_signal.emit(count, 1)

def ProcessLinesHi(self,lines, OutputFile, CounterFile, Conditions, ProgressBar):
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
        with open(OutputFile, "a") as out:
            for i in GoodTimes:
                out.write(i)
            out.close()
        with open(CounterFile, "a") as Fcount:
            deltaT = float(Conditions[2]) - float(Conditions[1])
            freq = goodlines/deltaT
            Fcount.writelines(Conditions[1] + "\t" + Conditions[2] + "\t" + str(goodlines) + "\t" + str(freq) + "\t" + OutputFile + "\n")
            Fcount.close()

def ProcessLoTimes(self,Terminal, ProgressBar, ProgressLabel, SourceDirectory, SortedDirectory):
    with open("LoGoodTimes.txt", "r") as GoodLo:
        LoList = GoodLo.readlines()
        GoodLo.close()
    for line in LoList:
        if not line.startswith("#") and line.strip():
            conditions = re.split("\s+", line)
            if len(conditions)>=11:
                ProgressLabel.setText(f"Processing data conditions: {line}")
                paths = GetLoDir(SourceDirectory, SortedDirectory, conditions)
                ProcessDataLo(self,conditions, paths[1], paths[0], Terminal, paths[2], ProgressBar)
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
                    ProcessLinesLo(self, lines, out, nums, Conditions)
                    file.close()
            except FileNotFoundError:
                pass
        self.update_progress_signal.emit(count, 2)

def ProcessLinesLo(self,lines, OutputFile, CounterFile, Conditions):
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
        with open(OutputFile, "a") as out:
            for i in GoodTimes:
                out.write(i)
            out.close()
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
                path = os.path.join(root,"SumHI.txt")
                ProgressLabel.setText(f"Summing up file: {file}")
                CalcSumHi(self,lines,path, ProgressBar)

def CalcSumHi(self, lines, path, ProgressBar):
    hide_counts = {}
    # count = 0
    # ProgressBar.setMaximum(len(lines))
    # self.update_progress_signal.emit(count, 1)
    for line in lines:
        # count += 1
        # self.update_progress_signal.emit(count, 1)
        fields = re.split('\t', line)
        location = fields[-1]
        print(f"{fields}+\n")
        hide_file = re.search(r'hide-(\d+).txt', location)
        if hide_file:
            hide_number = hide_file.group(1)
            countT = int(fields[2])
            deltaT = float(fields[1]) - float(fields[0])
            hide_counts[hide_number] = hide_counts.get(hide_number, (0, 0))
            hide_counts[hide_number] = (
                hide_counts[hide_number][0] + countT,
                hide_counts[hide_number][1] + deltaT
            )
    with open(path, "a") as sum:
        sum.write("File:\tCount:\tInverse Delta T:\t Frequency [counts/deltaT]:\n")
        for hide_number, (count, invdelta) in hide_counts.items():
            sum.write(f"hide-{hide_number}\t{count}\t{invdelta}\t{count/invdelta}\n")

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
                path = os.path.join(root,"SumLo.txt")
                ProgressLabel.setText(f"Summing up file: {file}")
                CalcSumLo(self,lines,path, ProgressBar)
def CalcSumLo(self, lines, path, ProgressBar):
    hide_counts = {}
    for line in lines:
        fields = re.split('\t', line)
        location = fields[-1]
        print(f"{fields}+\n")
        hide_file = re.search(r'lode-(\d+).txt', location)
        if hide_file:
            hide_number = hide_file.group(1)
            countT = int(fields[2])
            deltaT = float(fields[1]) - float(fields[0])
            hide_counts[hide_number] = hide_counts.get(hide_number, (0, 0))
            hide_counts[hide_number] = (
                hide_counts[hide_number][0] + countT,
                hide_counts[hide_number][1] + deltaT
            )
    with open(path, "a") as sum:
        sum.write("File:\tCount:\tInverse Delta T:\t Frequency [counts/deltaT]:\n")
        for hide_number, (count, invdelta) in hide_counts.items():
            sum.write(f"hide-{hide_number}\t{count}\t{invdelta}\t{count / invdelta}\n")