import os
import sys
from pathlib import Path 
import argparse
import datetime
from collections import defaultdict
import shutil


pars = argparse.ArgumentParser() # inbuilt function of argparse to parse the argument given in the cli
pars.add_argument("path", type=str) # adding a path argument to specifiy which directory to use for scanning 

target_path= pars.parse_args().path
print("Scanning Directory", target_path)

file_groups = defaultdict(list) # Create a dictionary with default list for grouping 




Ancient_artifacts= [] # here we gotta store all the old files path

c_time = datetime.datetime.now() # storing current time 

one_year_s = 365 * 24 * 60 * 60 # formula is year= (days * 24hrs * minuts * seconds)

for root, dirs, files, in os.walk(target_path): # this will scan through all the directory and sub directory starting at target_path
    for file in files: # iterates through all the files found in the directories 
        file_path = Path(root) / file # joining the whole file path root+ current file 
        
        mod_time = os.path.getmtime(file_path) # get the last modification time of the files in seconds 

        file_age= c_time.timestamp() - mod_time # caclulating the age of the files in seconds 

        if file_age > one_year_s:
            Ancient_artifacts.append(file_path) # so cool now a list will be appended if it's older 


print("Ancient Artifacts (>1 year old) :")

#for arti in Ancient_artifacts:
 #   print(arti) 


# Group the files by extension
for file_path in Ancient_artifacts:
    ext= file_path.suffix.lower() # get the lowercase of the extension 
    file_groups[ext].append(file_path) # appending to our dict

# printing Summaries of categories and counts 
print("\n Ancient Artifacts Categorized ")
for i, (ext, files) in enumerate(file_groups.items(), start=1): # The enumerate() function wraps the iterable, adding an automatic counter. It returns tuples containing an index (starting at 1 here) together with each (key, value) pair.
    # removing the . 
    display_ext = ext[1:] if ext else 'else no extension '
    print(f"({i}) {display_ext}s (found {len(files)})")

# For user to navigate through the catrgories 
choice = int(input("\n Select the category number to list those files: ")) -1  # -1 as our enum starts at index 1 

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

# priniting from oldest to newest 
print(f"\n Oldest {selected_ext[1:] if selected_ext else 'files'} : ")

c_time2 = datetime.datetime.now().timestamp()

  

# Create Archive Directory in USer's home if it does not exists 
archive_dir= Path.home() / "Archive"
archive_dir.mkdir(exist_ok=True) 

# The iterative interactive loop for the final boom bang 
while True:
    print("\n Select a file number to act on (or 0 to exits ): ")

    # Priniting the sorted files: 
    for idx, file_path in enumerate(selected_files, start=1):
        age_sec = c_time2 - os.path.getmtime(file_path)
        print(f"({idx}) {file_path.name} [{format_age(age_sec)}]")

    # ask user to select  a file number 
    file_choice = input("Enter The file Number: ")

    # Validation for better error Handling 
    if not file_choice.isdigit():
        print("Invalid input. Please enter a number. ")
        continue

    file_choice= int(file_choice)

    # Exiting the operation if that's the choice
    if file_choice == 0:
        print("Exiting File Interaction ")
        break

    # Check for valid Range 
    if not (1<= file_choice <= len(selected_files)):
        print("Invalid Selection Try again")
        continue

    chosen_file = selected_files[file_choice - 1]

    # All availabe Options 
    print(f"\nOptions for {chosen_file.name}:")
    print("[a] Read")
    print("[b] Delete")
    print("[c] Archive")
    print("[d] Ignore and exit")

    #  Storing user action and lowering if it he's dumb 
    action = input("Choose an action: ").strip().lower()

    # Inner loop to perform multiple actions on the same selected file
    while True:
        # Read Action 
        if action == 'a':
            try:
                # open and read first 1000 character of the file to display 
                with open(chosen_file, 'r', encoding='utf-8') as f:
                    print("\n ---- File content Start -------")
                    print(f.read(10000))
                    print("\n ------ File Content End ----------\n")
            except Exception as e:
                print(f"Error opening the file: {e}")
            
        # Delete Option 
        elif action == 'b':
            confirm= input(f"\nAre You sure you wanna delete this file {chosen_file}? [y/n]: ").strip().lower()
            if confirm == 'y':
                try:
                    os.remove(chosen_file) # Deleting the chosen file 
                    print(f"\n{chosen_file} was deleted successfully.")
                    selected_files.remove(chosen_file) # Removing the deleted files from the list 
                    break  # Exit inner loop as file no longer exists
                except Exception as e:
                    print(f"Error {e}")
            else:
                print("\nDeletion of the File Cancelled")
            
        # Archive Option 
        elif action == 'c':
            try:
                # moving the file to the archive directory 
                dest = archive_dir / chosen_file.name
                shutil.move(str(chosen_file), str(dest))
                print(f"\n{chosen_file} moved to Archive Folder at: {dest}")
                selected_files.remove(chosen_file) # removing from the main list 
                break  # Exit inner loop as file moved
            except Exception as e:
                print(f"\nError Archiving {chosen_file}: {e}")
        
        # Ignoring and exiting the action 
        elif action == 'd':
            print("\nIgnore Selected Exiting File Operation Interaction\n ")
            break

        else:
            print("Invalid Action. Choose from the options above dumbfuck ")

        # After performing any action except delete/archive/ignore, prompt for another action on same file
        action = input("\nChoose another action on this file (a, b, c, d): \n").strip().lower()
