import sys
import os
import subprocess # to execute commands safely like open this 
import platform 

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


if __name__ == '__main__':
    file_path= [r'D:\Camera\CIMG0093.JPG', r'D:\Research and tasks\Tasks\Dhruvil\readme.txt',r'C:\Users\Piyush\OneDrive\Documents\Exoplanet Detection AI vs. Meteor madness.pdf']
    open_files(file_path)