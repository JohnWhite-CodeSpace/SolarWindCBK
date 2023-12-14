import os, sys
import re
import pathlib
import time
def FindCorrectDataSets(self,SortedDirectory,Terminal, SubSortedDirectory, ProgressBar, Label):
    print("Start method")
    for root, dirs, files in os.walk(SortedDirectory):
        count = 0
        datasize = len(files)
        for file in files:
            self.update_progress_signal.emit(count, 1)
            ProgressBar.setMaximum(datasize)
            Terminal.append(f"Scanning file: {os.path.join(root,file)}")
            try:
                count += 1
                self.update_progress_signal.emit(count, 1)
            except Exception as e:
                print(e)
                Terminal.append(f"An error occurred while updating progress: {str(e)}")
                time.sleep(0.1)
                continue
            if file.endswith(".txt") and os.path.isfile(os.path.join(root,file)) and not file.endswith(".attdba")\
                    and not file.endswith(".star-spin-nep.txt") and not file.endswith("ibex_state_GSE.txt"):
                filepath = os.path.join(root,file)
                Terminal.append(f"Found file in: {filepath}")
                Label.setText(f"Scanning file: {filepath}")
                source_directory = os.path.abspath(root)
                correctfilepath = os.path.join(SubSortedDirectory, os.path.relpath(source_directory,SortedDirectory))
                pathlib.Path(correctfilepath).mkdir(parents=True, exist_ok=True)
                with open(filepath, "r") as filedata:
                    lines = filedata.readlines()
                    filedata.close()
                output_lines = process_lines(lines)
                if output_lines:
                    with open(os.path.join(correctfilepath, file), 'w') as output_file:
                        output_file.writelines(output_lines)
                        output_file.close()


def process_lines(lines):
    return [line for line in lines if re.split('\s+', line)[4] in ["0A", "0E", "05", "40"]
            and re.split('\s+', line)[3].startswith('2') or re.split('\s+', line)[4] in ["0A", "0E", "05", "40"]
    and re.split('\s+', line)[3].startswith('1')]

    #Process finished with exit code -1073741819 (0xC0000005)