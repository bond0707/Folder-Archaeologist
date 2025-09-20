import os
import sys
import platform
import subprocess
import shutil
import datetime
import mimetypes
from pathlib import Path
from rich.progress import Progress        # For progress bar in archiving
from utility import format_size           # Make sure this exists/imported in utils

# ---------------- Feature A: Select Files ----------------
def select_files(file_paths):
    """
    Allows user to select specific files from a list by index.
    
    Args:
        file_paths (list[Path or str]): Original list of file paths
        
    Returns:
        list: Selected subset of file paths
    """
    selected_files = []  # Will store user's selected files
    
    # Show all available files with index numbers
    print("\nAvailable files:")
    for idx, file_path in enumerate(file_paths, 1):
        file_path = Path(file_path)
        print(f"{idx}. {file_path.name}")
    
    # Get user input for file selection
    selection_input = input("\nEnter file numbers separated by spaces (e.g., 1 3 5): ").strip()
    selected_indices = selection_input.split()  # Split by spaces to get individual numbers
    
    # Convert string indices to integers and get corresponding files
    for index_str in selected_indices:
        try:
            index = int(index_str) - 1  # Convert to 0-based index
            if 0 <= index < len(file_paths):  # Check if index is valid
                selected_files.append(file_paths[index])
            else:
                print(f"Invalid index: {index_str}")
        except ValueError:
            print(f"Invalid input: {index_str} is not a number")
    
    return selected_files

# ---------------- Feature B: Delete Files ----------------
def delete_files(file_paths):
    """
    Deletes all files in the provided list after user confirmation.
    OS-independent deletion with fallback options.
    
    Args:
        file_paths (list[Path or str]): List of file paths to delete
    """
    if not file_paths:  # Check if list is empty
        print("No files to delete.")
        return
    
    # Show files to be deleted
    print(f"\nFiles to be deleted ({len(file_paths)} total):")
    for idx, file_path in enumerate(file_paths, 1):
        file_path = Path(file_path)
        print(f"{idx}. {file_path.name}")
    
    # Get user confirmation before deletion
    confirm = input(f"\nAre you sure you want to delete these {len(file_paths)} files? [y/n]: ").strip().lower()
    
    if confirm != 'y':
        print("Deletion cancelled.")
        return
    
    # Try to move to recycle bin first, fallback to permanent deletion
    for file_path in file_paths:
        file_path = Path(file_path)
        try:
            # OS-specific recycle bin operations
            system_name = platform.system()
            
            if system_name == "Windows":
                # Use send2trash library if available, otherwise permanent delete
                try:
                    import send2trash
                    send2trash.send2trash(str(file_path))
                    print(f"Moved '{file_path.name}' to recycle bin")
                except ImportError:
                    # Fallback to permanent deletion
                    permanent_delete = input(f"Cannot move to recycle bin. Delete '{file_path.name}' permanently? [y/n]: ").strip().lower()
                    if permanent_delete == 'y':
                        os.remove(file_path)
                        print(f"Permanently deleted '{file_path.name}'")
                    
            elif system_name == "Darwin":  # macOS
                subprocess.run(["osascript", "-e", f'tell application "Finder" to delete POSIX file "{file_path}"'], check=True)
                print(f"Moved '{file_path.name}' to trash")
                
            else:  # Linux and others
                # Try using trash-cli if available
                try:
                    subprocess.run(["trash", str(file_path)], check=True)
                    print(f"Moved '{file_path.name}' to trash")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback to permanent deletion
                    permanent_delete = input(f"Cannot move to trash. Delete '{file_path.name}' permanently? [y/n]: ").strip().lower()
                    if permanent_delete == 'y':
                        os.remove(file_path)
                        print(f"Permanently deleted '{file_path.name}'")
                        
        except Exception as e:
            print(f"Failed to delete '{file_path.name}': {e}")

# ---------------- Feature C: Move Files ----------------
def move_files(file_paths, target_folder):
    """
    Move given files to the target folder, creating the folder if missing.

    Args:
        file_paths (List[Path or str]): List of file paths to move.
        target_folder (str or Path): Destination folder path.
    """
    target_folder = Path(target_folder)  # Ensure target is a Path object
    
    # Create target folder if it doesn't exist
    if not target_folder.exists():
        print(f"Target Folder '{target_folder}' doesn't exist. Creating it......")
        target_folder.mkdir(parents=True, exist_ok=True)  # Create folder and parent directories
    
    # Move each file to the target folder
    for file_path in file_paths:
        file_path = Path(file_path)  # Ensure file_path is Path object
        dest_path = target_folder / file_path.name  # Destination path for this file
        
        # Handle filename conflicts by adding numbers
        count = 1  # Counter for duplicate filename resolution
        original_stem = file_path.stem  # Filename without extension
        original_suffix = file_path.suffix  # File extension
        
        # Keep incrementing counter until we find available filename
        while dest_path.exists():
            dest_path = target_folder / f"{original_stem}({count}){original_suffix}"
            count += 1
        
        try:
            shutil.move(str(file_path), str(dest_path))  # Move the file
            print(f"Moved '{file_path.name}' to '{dest_path}'")
        except Exception as e:
            print(f"Failed to move '{file_path}': {e}")

# ---------------- Feature D: Open Files ----------------
def open_file(file_path):
    """
    Opens the specified file with the system's default application.
    Cross-platform support for Windows, macOS, Linux.

    Args:
        file_path (str or Path): Path to the file to open.
    """
    try:
        systername = platform.system()  # Get current operating system
        
        if systername == "Windows":
            os.startfile(file_path)  # Windows-specific file opening
        elif systername == "Darwin":  # macOS
            subprocess.run(["open", file_path], check=True)
        else:  # Linux and other Unix-like systems
            subprocess.run(["xdg-open", file_path], check=True)
        print(f"Opened File {file_path}")
    except Exception as e:
        print(f"Error opening the file: {e}")

def open_files(file_paths):
    """
    Opens multiple files with the default application.

    Args:
        file_paths (list[str or Path]): List of files to open.
    """
    # Loop through each file path and open it
    for file_path in file_paths:
        open_file(file_path)

# ---------------- Feature E: Get Details ----------------
def get_file_details(file_path):
    """
    Displays detailed information about the given file.

    Parameters:
    -----------
    file_path : str or Path
        Path to the file to query.
    """
    file_path = Path(file_path)  # Ensure file_path is a Path object
    
    # Check if file exists before getting details
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return
    
    # Gather file information
    size = os.path.getsize(file_path)  # File size in bytes
    ctime = os.path.getctime(file_path)  # Creation time (timestamp)
    mtime = os.path.getmtime(file_path)  # Last modification time (timestamp)
    mime_type, _ = mimetypes.guess_type(str(file_path))  # MIME type based on extension
    
    # Display file details in readable formats
    print(f"File: {file_path}")
    print(f"Size: {format_size(size)}")
    print(f"Created: {datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Modified: {datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"File extension: {file_path.suffix}")
    if mime_type:
        print(f"MIME type: {mime_type}")

def get_files_details(file_paths):
    """
    Iterates over a list of file paths and displays their details.

    Parameters:
    -----------
    file_paths : list[str or Path]
        List of file paths to query.
    """
    # Display details for each file with separators
    for file_path in file_paths:
        print("\n" + "-" * 50)  # Visual separator between files
        get_file_details(file_path)

# ---------------- Feature F: Archive All Files ----------------
def archive_files(file_list, archive_name):
    """
    Archives all specified files into a single zip file.
    Uses rich progress bar for visual feedback.
    
    Args:
        file_list   (list):      List of file paths to archive.
        archive_name (str):      Name for the zip file to be created.
    """
    # Convert all paths to strings for command execution
    file_strings = [str(Path(f)) for f in file_list]
    
    # OS-specific archive commands
    if sys.platform in ["linux", "linux2", "darwin"]:  # Linux/macOS
        command = ["zip", archive_name, *file_strings]
    elif sys.platform == "win32":  # Windows
        command = [
            "powershell", 
            "Compress-Archive", 
            "-Path", "@(" + ", ".join([f'"{f}"' for f in file_strings]) + ")",
            "-DestinationPath", archive_name,
            "-Force"
        ]
    
    # Show progress during compression
    with Progress() as progress:
        compress_task = progress.add_task("[red]Compressing files...", total=None)
        try:
            subprocess.run(command, shell=True, check=True)
            progress.update(compress_task, completed=True, description="[green]Archive created successfully!")
            print(f"Files archived to: {archive_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating archive: {e}")

# ---------------- Main Interactive Menu ----------------
def file_operations_menu(file_paths):
    """
    Interactive menu for performing operations on a list of files.
    Runs in a loop until user chooses to exit.
    
    Args:
        file_paths (list[Path or str]): Initial list of files to operate on
    """
    original_files = file_paths.copy()  # Keep reference to original file list
    current_files = file_paths.copy()   # Working list that can be modified
    
    while True:  # Main menu loop - continues until user exits
        print(f"\n{'='*50}")
        print(f"FILE OPERATIONS MENU ({len(current_files)} files)")
        print(f"{'='*50}")
        
        # Show current files being operated on
        print("\nCurrent files:")
        for idx, file_path in enumerate(current_files, 1):
            file_path = Path(file_path)
            print(f"{idx}. {file_path.name}")
        
        # Display menu options
        print(f"\n{'='*30} OPTIONS {'='*30}")
        print("[A] Select Files      - Choose specific files to work with")
        print("[B] Delete Files      - Delete all current files")
        print("[C] Open Files        - Open all current files")
        print("[D] Move Files        - Move all current files to folder")
        print("[E] Archive Files     - Create zip archive of current files")
        print("[F] Get Details       - Show detailed info of current files")
        print("[G] Go Back           - Return to original file list")
        print("[H] Exit              - Exit the program")
        
        # Get user choice
        choice = input(f"\nSelect an option [A-H]: ").strip().upper()
        
        if choice == 'A':  # Select specific files
            print("\n--- SELECT FILES ---")
            selected_files = select_files(current_files)
            if selected_files:
                current_files = selected_files  # Update working list
                print(f"Selected {len(current_files)} files.")
            else:
                print("No files selected. Keeping current list.")
        
        elif choice == 'B':  # Delete files
            print("\n--- DELETE FILES ---")
            delete_files(current_files)
            # Remove deleted files from current list (assuming they were deleted)
            current_files = []
        
        elif choice == 'C':  # Open files
            print("\n--- OPENING FILES ---")
            open_files(current_files)
        
        elif choice == 'D':  # Move files
            print("\n--- MOVE FILES ---")
            target_folder = input("Enter destination folder path: ").strip()
            if target_folder:
                move_files(current_files, target_folder)
            else:
                print("No folder specified. Operation cancelled.")
        
        elif choice == 'E':  # Archive files
            print("\n--- ARCHIVE FILES ---")
            archive_name = input("Enter archive name (with .zip extension): ").strip()
            if archive_name:
                if not archive_name.endswith('.zip'):
                    archive_name += '.zip'
                archive_files(current_files, archive_name)
            else:
                print("No archive name specified. Operation cancelled.")
        
        elif choice == 'F':  # Get file details
            print("\n--- FILE DETAILS ---")
            get_files_details(current_files)
        
        elif choice == 'G':  # Go back to original list
            print("\n--- RESTORING ORIGINAL LIST ---")
            current_files = original_files.copy()
            print(f"Restored {len(current_files)} original files.")
        
        elif choice == 'H':  # Exit program
            print("\n--- EXITING PROGRAM ---")
            print("Thank you for using File Operations! This site has been excavated.")
            break
        
        else:  # Invalid choice
            print("Invalid choice. Please select A-H.")

# ---------- Sample usage in main -------------
if __name__ == '__main__':
    # Test with sample files (uncomment to test)
    # sample_files = [r"C:\path\file1.txt", r"C:\path\file2.png"]
    # file_operations_menu(sample_files)

    test_files = [
        r"E:\DSA\Day1 1.1.cpp",
        r"D:\IAF\data\app.py",
        r"C:\Users\Piyush\OneDrive\Pictures\goalkick.mp4"
    ]
    file_operations_menu(test_files)
    pass
