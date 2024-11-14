import sys, os, glob, shutil, pathlib

def InitDataFileSorting(Source_Directory, Sorted_Directory):

    for root, dirs, files in os.walk(Source_Directory):
        if any(file.endswith(".attdba") for file in files if os.path.isfile(os.path.join(root, file))) \
                and not any(file.endswith(".attd2a") for file in files if os.path.isfile(os.path.join(root, file))):
                source_directory = os.path.abspath(root)
                print(f"Found '. attdba' file in: {source_directory}")
                destination_directory = os.path.join(Sorted_Directory, os.path.relpath(source_directory, Source_Directory))
                print(destination_directory)
                print("Copying correct data files for further processing...")
                CollectFiles(source_directory, destination_directory)

def ignore_directories(dir, files):
    return [d for d in files if os.path.isdir(os.path.join(dir, d))]

def CollectFiles(Source_Directory, Sorted_Directory):
            print(Source_Directory)
            shutil.copytree(Source_Directory,Sorted_Directory, ignore=ignore_directories)
            print(f"Dataset successfully copied from {Source_Directory} to {Sorted_Directory}")

# def Start_Sorting():
#     print("Enter source directory path with raw data:")
#     Source = input()
#     print("Enter directory path to which sorted data will be stored:")
#     Sorted = input()
#     InitDataFileSorting(Source,Sorted)


