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
            if count % 100 == 0:
                print(count)
                print(datasize)
            self.update_progress_signal.emit(count)
            ProgressBar.setMaximum(datasize)
            Terminal.append(f"Scanning file: {os.path.join(root,file)}")
            try:
                count += 1
                self.update_progress_signal.emit(count)
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
                output_lines = process_lines(lines)
                if output_lines:
                    with open(correctfilepath, 'w') as output_file:
                        output_file.writelines(output_lines)

def setProgressBar(datasize):
    return datasize

def process_lines(lines):
    # Add your conditions for processing lines here
    # For example, let's copy lines containing the word 'example'
    return [line for line in lines if re.split('\s+', line)[4] in ["0A", "0E", "05", "40", "2*"]]
def ScanningProcess(self,lines,Terminal,ProgressBar,correctfilepath,file,filepath):
    datasize = len(lines)
    count = 0
    self.update_progress_signal.emit(count)
    ProgressBar.setMaximum(datasize)

    for line in lines:
        if count%100==0:
            print(count)
            print(datasize)
        try:
            count += 1
            self.update_progress_signal.emit(count)
        except Exception as e:
            print(e)
            Terminal.append(f"An error occurred while updating progress: {str(e)}")
            time.sleep(0.1)
            continue
        eventtype = re.split('\s+', line)[4]
        if eventtype in ["0A", "0E", "05", "40", "2*"]:
            #Terminal.append(f"Event type found: {eventtype} in line of data: {line}")
            try:
                with open(os.path.join(correctfilepath, file), "a") as correctfile:
                    correctfile.write(line + "\n")
            except Exception as e:
                print(e)
                Terminal.append(f"An error occurred while opening file or writing to file: {str(e)}")
                correctfile.close()
                time.sleep(0.1)
                continue
            # except Exception as e:
            #     print(e)
            #     Terminal.append(f"Error occured while opening file: {str(e)}")
            #     correctfile.close()
            #     time.sleep(0.1)
            #     continue

            finally:
                correctfile.close()
        #time.sleep(0.0008)
    Terminal.append(f"\nFinished scanning file: {filepath}")

    #Process finished with exit code -1073741819 (0xC0000005)