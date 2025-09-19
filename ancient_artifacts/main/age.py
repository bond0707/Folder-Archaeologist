# from ancient_artifacts.py

import os
import sys
from pathlib import Path 
import datetime
from collections import defaultdict
from utility import parse_directory_path

def by_age(target_path):
    """
    Groups and displays ancient artifacts (files older than 1 year) by file extension.
    
    Parameters:
    -----------
    target_path : str or Path
        Directory path to scan for old files.
    """
    print("Scanning Directory", target_path)

    file_groups = defaultdict(list) # Create a dictionary with default list for grouping 

    Ancient_artifacts = [] # here we gotta store all the old files path

    c_time = datetime.datetime.now() # storing current time 

    one_year_s = 365 * 24 * 60 * 60 # formula is year= (days * 24hrs * minuts * seconds)

    for root, dirs, files in os.walk(target_path): # this will scan through all the directory and sub directory starting at target_path
        for file in files: # iterates through all the files found in the directories 
            file_path = Path(root) / file # joining the whole file path root+ current file 
            
            mod_time = os.path.getmtime(file_path) # get the last modification time of the files in seconds 

            file_age = c_time.timestamp() - mod_time # caclulating the age of the files in seconds 

            if file_age > one_year_s:
                Ancient_artifacts.append(file_path) # so cool now a list will be appended if it's older 

    print("Ancient Artifacts (>1 year old) :")

    #for arti in Ancient_artifacts:
     #   print(arti) 

    # Group the files by extension
    for file_path in Ancient_artifacts:
        ext = file_path.suffix.lower() # get the lowercase of the extension 
        file_groups[ext].append(file_path) # appending to our dict

    # printing Summaries of categories and counts 
    print("\n Ancient Artifacts Categorized ")
    for i, (ext, files) in enumerate(file_groups.items(), start=1): # The enumerate() function wraps the iterable, adding an automatic counter. It returns tuples containing an index (starting at 1 here) together with each (key, value) pair.
        # removing the . 
        display_ext = ext[1:] if ext else 'else no extension '
        print(f"({i}) {display_ext}s (found {len(files)})")

    # For user to navigate through the catrgories 
    choice = int(input("\n Select the category number to list those files: ")) - 1  # -1 as our enum starts at index 1 

    selected_ext = list(file_groups.keys())[choice]
    selected_files = file_groups[selected_ext]
    # here we convert dict-keys to list so we can access it rhough index properly and then we store the choice 
    # Slected_files store the files of selected categories 

    # humanly readable age
    def format_age(seconds):
        days = seconds // (24*3600)
        years = days // 365
        days = days % 365
        return f"{int(years)} years , {int(days)} days old "

    # Sort selected files by modification time ascending (oldest first)
    selected_files.sort(key=lambda f: os.path.getmtime(f))
    
    # priniting from oldest to newest 
    print(f"\n Oldest {selected_ext[1:] if selected_ext else 'files'} : ")

    c_time2 = datetime.datetime.now().timestamp()
    
    # Display the files with their ages
    for idx, file_path in enumerate(selected_files, start=1):
        age_sec = c_time2 - os.path.getmtime(file_path)
        print(f"({idx}) {file_path.name} [{format_age(age_sec)}]")

    return selected_files, selected_ext  # Return files and extension for potential further use


if __name__ == '__main__':
    target_path = parse_directory_path()
    by_age(target_path)
