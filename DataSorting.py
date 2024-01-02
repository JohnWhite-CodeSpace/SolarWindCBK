import sys, os, glob, shutil, pathlib
import time
def InitDataFileSorting(self,Source_Directory, Sorted_Directory, Terminal, Label):
    count = 0
    # for root, dirs, files in os.walk(Source_Directory):
    #     Label.setText(f"Scanning directory: {root}")
    #     if any(file.endswith(".attdba") for file in files if os.path.isfile(os.path.join(root, file))) \
    #             and not any(file.endswith(".attd2a") for file in files if os.path.isfile(os.path.join(root, file))):
    #         source_directory = os.path.abspath(root)
    #         Terminal.append(f"Found '.attdba' file in: {source_directory}")
    #         destination_directory = os.path.join(Sorted_Directory, os.path.relpath(source_directory, Source_Directory))
    #         Label.setText(f"Copying data from {source_directory} to {destination_directory}...")
    #         Terminal.append("Copying correct data files for further processing...")
    #         CollectFiles(source_directory, destination_directory, Terminal)
    CheckDoubleObservation(Source_Directory,Terminal,Label,Sorted_Directory)

def ignore_directories(dir, files):
    return [d for d in files if os.path.isdir(os.path.join(dir, d))]

def CollectFiles(Source_Directory, Sorted_Directory, Terminal):
            Terminal.append(Source_Directory)
            try:
                shutil.copytree(Source_Directory,Sorted_Directory, ignore=ignore_directories)
                Terminal.append(f"Dataset successfully copied from {Source_Directory} to {Sorted_Directory}")
            except:
                Terminal.append("Cannot create a file when that file already exists: ")

def CheckDoubleObservation(SourceDirectory, Terminal, Label, SortedDirectory):
    for root, dirs, files in os.walk(SourceDirectory):
        CheckHi3 = ""
        CheckHi2 = ""
        for file in files:
            if file.endswith("hihb-2.txt"):
                CheckHi2 = file
                Terminal.append(f"Found file: {file}.")
            elif file.endswith("hihb-3.txt"):
                CheckHi3 = file
                Terminal.append(f"Found file: {file}.")
        if CheckHi3 != "" and CheckHi2 != "":
            if os.path.getsize(os.path.join(root, CheckHi3))>=1.5*os.path.getsize(os.path.join(root,CheckHi2)):
                Label.setText(f"Double observation occurred in {os.path.relpath(CheckHi3)} ")
                openfile = os.path.join(SortedDirectory, "DoubleObservationCheck.txt")
                with open(openfile, 'a') as IsDoubleFile:
                    IsDoubleFile.write(f"Channel 3 was observed twice in {os.path.relpath(CheckHi3)}.\n")
                IsDoubleFile.close()
            else:
                Label.setText(f"No double observations in {os.path.relpath(CheckHi3)} ")
                openfile = os.path.join(SortedDirectory, "DoubleObservationCheck.txt")
                with open(openfile, 'a') as IsDoubleFile:
                    IsDoubleFile.write(f"No double observations detected in {os.path.relpath(CheckHi3)}.\n")
                IsDoubleFile.close()
                time.sleep(0.0005)










