import sys
import os
import subprocess # to execute commands safely like open this 
import platform 
import shutil
import datetime
import mimetypes
from utility import format_size
from pathlib import Path


#4th feature --> move file 
def move_file(file_paths, target_folder):
    """
    Move given files to the target folder, creating the folder if missing.

    Args:
        file_paths (List[Path or str]): List of file paths to move.
        target_folder (str or Path): Destination folder path.
    """

    target_folder = Path(target_folder)
    if not target_folder.exists():
        print(f"Target Folder '{target_folder} Doesn't Exists. Creating it......'")
        target_folder.mkdir(parents=True, exist_ok=True) # create the folder if does not exists using mkdir

    for file_path in file_paths:
        file_path = Path(file_path)
        dest_path = target_folder/ file_path.name

    # Optionally handle filename conflicts here
        count = 1
        original_stem = file_path.stem
        original_suffix = file_path.suffix
        while dest_path.exists():
            # Rename file with number suffix if name conflict
            dest_path = target_folder / f"{original_stem}({count}){original_suffix}"
            count += 1

        try:
            shutil.move(str(file_path), str(dest_path)) # moving the file 
            print(f"Moved '{file_path.name}' to '{dest_path}'")
        except Exception as e:
            print(f"Failed to move '{file_path}': {e}")

# 5th Feature --> Open files 
def open_file(file_path):
    try:
        systername=platform.system() # Returns the Name of the Platform you are on linux, macos or Windows 
        if systername == "Windows":
            # uses start command to open the file in shell
            os.startfile(file_path)
        elif systername == "Darwin":
            # Open for Macos
            subprocess.run(["open", file_path], check=True)
        else:
            # Assume Linux use xdg
            subprocess.run(["xdg-open", file_path], check=True)
        print(f"Opened File {file_path}")
    except Exception as e:
        print(f"Error opening the file: {e}")

# 5th(multiple) feature -> open all selected Files
def open_files(file_path):
    for filepath in file_path:
        open_file(filepath)


# 6th feature --> get details of a single file
def get_file_details(file_path):
    """
    Displays detailed information about the given file.

    Parameters:
    -----------
    file_path : str or Path
        Path to the file to query.
    """
    file_path = Path(file_path)  # Ensure file_path is a Path object
    
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    # Fetch file size in bytes
    size = os.path.getsize(file_path)
    # Fetch creation time (epoch timestamp)
    ctime = os.path.getctime(file_path)
    # Fetch last modification time (epoch timestamp)
    mtime = os.path.getmtime(file_path)
    # Guess MIME type based on extension
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Display file details in readable formats
    print(f"File: {file_path}")
    print(f"Size: {format_size(size)}")
    print(f"Created: {datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modified: {datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"File extension: {file_path.suffix}")
    if mime_type:
        print(f"MIME type: {mime_type}")

#6th feature(multiple) --> get details of multiple files by calling get_file_details on each
def get_files_details(file_paths):
    """
    Iterates over a list of file paths and displays their details.

    Parameters:
    -----------
    file_paths : list[str or Path]
        List of file paths to query.
    """
    # Iterate through all provided files
    for file_path in file_paths:
        print("\n-----------------------")
        get_file_details(file_path)

if __name__ == '__main__':
    # for open files test case
    # file_path= [r'D:\Camera\CIMG0093.JPG', r'D:\Research and tasks\Tasks\Dhruvil\readme.txt',r'C:\Users\Piyush\OneDrive\Documents\Exoplanet Detection AI vs. Meteor madness.pdf']
    # open_files[(file_path)
    
    
    # For Move folder test case
    #file_paths = [r'D:\Camera\CIMG0093.JPG', r'C:\Users\Piyush\OneDrive\Pictures\da_quickcall_icon.jfif']

    #target_folder = (input('Enter Your Destination Dir: '))
    #move_file(file_paths, target_folder)


    # for get details
    # file_path = r'C:\Users\Piyush\OneDrive\Documents\Zoom\demo\da_quickcall_icon.jfif'
    # get_file_details(file_path)
    pass
