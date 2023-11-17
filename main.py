import sys, os, glob, shutil, pathlib





def InitDataFileSorting(Directory):
    for root, dirs, files in os.walk(Data_Dir):
        for file in files:
            if file.endswith('.attdba'):
                file_path = os.path.join(root, file)
                subdirectory_name = os.path.relpath(root, Data_Dir)
                print("Found file:"+ file_path + " in " + subdirectory_name + " directory")

                MoveFileTo(file_path, Sorted_Dir, subdirectory_name)



def MoveFileTo(filepath, Sorted_Directory, Child_Directory):
    if Child_Directory != Sorted_Directory:
        piece1 = Sorted_Directory
        piece2 = Child_Directory
        path=os.path.join(piece1,piece2)
        os.mkdir(path,0o666)
    else:
        Child_Directory=""
    shutil.move(filepath, Sorted_Directory + "/"+Child_Directory)
    print("File in:" +  filepath + " moved to: " + Sorted_Directory+"/"+Child_Directory)

if __name__ == "__main__":
    Data_Dir = "H:/SolarWindCBK/IBEX/"
    Sorted_Dir = "H:/SortedData/"
    InitDataFileSorting(Data_Dir)


