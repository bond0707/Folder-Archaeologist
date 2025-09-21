import os
import shutil
import datetime
import platform
import mimetypes
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from .utilities import format_size, clear_screen, show_data

console = Console()

try:
    import send2trash
except ImportError:
    send2trash = None

def select_files(file_paths):
    """Allows user to select specific files from a list by index."""
    clear_screen() # 3. Clear screen on select
    if not file_paths:
        console.print("[yellow]No files to select from.[/yellow]")
        return []
        
    selected_files = []
    
    rows = [[str(idx), Path(fp).name] for idx, fp in enumerate(file_paths, 1)]
    show_data("Available Files for Selection", ["#", "Filename"], rows)
    
    selection_input = input("\nEnter file numbers separated by spaces (e.g., 1 3 5), or 'all': ").strip()
    
    if selection_input.lower() == 'all':
        return file_paths

    selected_indices = selection_input.split()
    
    for index_str in selected_indices:
        try:
            index = int(index_str) - 1
            if 0 <= index < len(file_paths):
                selected_files.append(file_paths[index])
            else:
                console.print(f"[red]Invalid index: {index_str}[/red]")
        except ValueError:
            console.print(f"[red]Invalid input: {index_str} is not a number[/red]")
    
    return selected_files

def delete_files(file_paths):
    """Deletes all files in the provided list after user confirmation."""
    clear_screen() # 3. Clear screen on delete
    if not file_paths:
        console.print("[yellow]No files to delete.[/yellow]")
        return
    
    rows = [[str(idx), Path(fp).name] for idx, fp in enumerate(file_paths, 1)]
    show_data(f"Files to be Deleted ({len(file_paths)} total)", ["#", "Filename"], rows)
    
    confirm = input(f"\nAre you sure you want to delete these {len(file_paths)} files? [y/n]: ").strip().lower()
    
    if confirm != 'y':
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return
    
    for file_path in file_paths:
        file_path = Path(file_path)
        try:
            if send2trash:
                send2trash.send2trash(str(file_path))
                console.print(f"Moved '{file_path.name}' to trash.")
            else:
                os.remove(file_path)
                console.print(f"[yellow]Permanently deleted '{file_path.name}' (send2trash not installed).[/yellow]")
        except Exception as e:
            console.print(f"[red]Failed to delete '{file_path.name}': {e}[/red]")

def move_files(file_paths, target_folder):
    """Move given files to the target folder, creating it if missing."""
    clear_screen()
    target_folder = Path(target_folder)
    
    try:
        if not target_folder.exists():
            console.print(f"Target folder '{target_folder}' doesn't exist. Creating it...")
            target_folder.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[red]Could not create target folder: {e}[/red]")
        return

    for file_path in file_paths:
        file_path = Path(file_path)
        dest_path = target_folder / file_path.name
        
        count = 1
        original_stem = file_path.stem
        original_suffix = file_path.suffix
        
        while dest_path.exists():
            dest_path = target_folder / f"{original_stem}({count}){original_suffix}"
            count += 1
        
        try:
            shutil.move(str(file_path), str(dest_path))
            console.print(f"Moved '{file_path.name}' to '{dest_path}'")
        except Exception as e:
            console.print(f"[red]Failed to move '{file_path}': {e}[/red]")

def open_files(file_paths):
    """Opens multiple files with the default application."""
    clear_screen()
    for file_path in file_paths:
        try:
            system_name = platform.system()
            if system_name == "Windows":
                os.startfile(file_path)
            elif system_name == "Darwin":
                subprocess.run(["open", file_path], check=True, capture_output=True)
            else:
                subprocess.run(["xdg-open", file_path], check=True, capture_output=True)
            console.print(f"Attempting to open file: {Path(file_path).name}")
        except Exception as e:
            console.print(f"[red]Error opening file {Path(file_path).name}: {e}[/red]")

def get_files_details(file_paths):
    """Displays detailed information about the given files in a single table."""
    clear_screen()
    if not file_paths:
        console.print("[yellow]No files to get details for.[/yellow]")
        return

    columns = ["#", "Filename", "Size", "Created", "Modified", "MIME Type", "Full Path"]
    rows = []
    for idx, file_path in enumerate(file_paths, 1):
        file_path = Path(file_path)
        try:
            if not file_path.exists():
                rows.append([str(idx), file_path.name, "[red]File not found[/red]", "-", "-", "-", str(file_path)])
                continue
            
            stat_info = file_path.stat()
            size = stat_info.st_size
            ctime = stat_info.st_ctime
            mtime = stat_info.st_mtime
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            row_data = [
                str(idx),
                file_path.name,
                format_size(size),
                datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S'),
                datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S'),
                mime_type if mime_type else "unknown",
                str(file_path.resolve())  # full absolute path
            ]
            rows.append(row_data)
        except (FileNotFoundError, PermissionError) as e:
            rows.append([str(idx), file_path.name, f"[red]Error: {e}[/red]", "-", "-", "-", str(file_path)])

    show_data("File Details", columns, rows)
    input("\nPress Enter to return to the selection menu...")



def archive_files(file_list, archive_name=None):
    """
    Archives all specified files into a single zip file using Python's zipfile module.
    Prompts user for a destination directory (creates it if missing),
    uses home directory as default if no input given,
    then asks for archive name and shows final zip full path.
    """
    from os.path import expanduser
    import zipfile

    clear_screen()

    # Ask user for destination directory
    dest_dir = input("Enter destination directory for archive (leave empty for home directory): ").strip()
    if not dest_dir:
        dest_dir = expanduser("~")  # User home directory
    dest_path = Path(dest_dir)
    
    # Create directory if it doesn't exist
    if not dest_path.exists():
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
            console.print(f"[green]Created directory: {dest_path}[/green]")
        except Exception as e:
            console.print(f"[red]Error creating directory: {e}[/red]")
            return
    
    # Ask user for archive name if not provided
    if not archive_name:
        archive_name = input("Enter archive zip filename (without extension): ").strip()
        if not archive_name:
            console.print("[yellow]No archive name provided. Using default 'archive'.[/yellow]")
            archive_name = "archive"
    # Ensure it ends with .zip
    if not archive_name.endswith(".zip"):
        archive_name += ".zip"

    # Full archive path
    archive_full_path = dest_path / archive_name

    with Progress() as progress:
        task = progress.add_task("[red]Compressing files...", total=len(file_list))
        try:
            with zipfile.ZipFile(archive_full_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in file_list:
                    path_obj = Path(file_path)
                    zipf.write(path_obj, path_obj.name)
                    progress.update(task, advance=1, description=f"[cyan]Adding {path_obj.name}")
            progress.update(task, completed=True, description="[green]Archive created successfully!")
            console.print(f"Files archived to: [bold]{archive_full_path.resolve()}[/bold]")
        except Exception as e:
            progress.update(task, completed=True, description="[bold red]Error creating archive.[/bold red]")
            console.print(f"[red]Error creating archive: {e}[/red]")


def file_operations_menu(file_paths):
    """
    Interactive menu for performing operations on a list of files.
    Returns True to go back to categories, False to exit the program.
    """
    original_files = file_paths.copy()
    current_files = file_paths.copy()
    
    while True:
        # BUG FIX: If the selection is empty (e.g., after deleting files),
        # automatically redirect to the main menu without user input.
        if not current_files:
            return True # Signal to go back to categories

        clear_screen()
        console.print(f"\n[bold]{'='*26} FILE OPERATIONS MENU ({len(current_files)} files) {'='*26}[/bold]")
        
        file_rows = [[str(idx), Path(fp).name] for idx, fp in enumerate(current_files, 1)]
        show_data("Current Files for Operation", ["#", "Filename"], file_rows)
        
        console.print(f"\n[bold cyan]{'='*38} OPTIONS {'='*38}[/bold cyan]")
        print("[A] Select Specific Files")
        print("[B] Delete Current Files")
        print("[C] Open Current Files")
        print("[D] Move Current Files")
        print("[E] Archive Current Files")
        print("[F] Get Detailed Info")
        print("[G] Reset to Original Selection")
        # BUG FIX: Renamed menu option for clarity.
        print("[H] Back to Main Menu")
        print("[I] Exit Program")
        
        choice = input(f"\nSelect an option [A-I]: ").strip().upper()
        
        if choice == 'A':
            selected = select_files(current_files)
            if selected:
                current_files = selected
                console.print(f"[green]Selected {len(current_files)} files.[/green]")
        
        elif choice == 'B':
            delete_files(current_files)
            current_files = [] # Assume deletion was successful to clear list
        
        elif choice == 'C':
            open_files(current_files)
        
        elif choice == 'D':
            # BUG FIX: Keep asking for a path if the input is empty.
            target_folder = ""
            while not target_folder:
                target_folder = input("Enter destination folder path: ").strip()
                if not target_folder:
                    console.print("[red]Path cannot be empty. Please enter a destination folder.[/red]")
            move_files(current_files, target_folder)
            current_files = [] # Files have been moved, so the selection is now empty.
        
        elif choice == 'E':
            # BUG FIX: Keep asking for an archive name if the input is empty.
            archive_name = ""
            while not archive_name:
                archive_name = input("Enter archive name (e.g., my_archive.zip): ").strip()
                if not archive_name:
                    console.print("[red]Archive name cannot be empty. Please enter a name.[/red]")

            if not archive_name.lower().endswith('.zip'):
                archive_name += '.zip'
            archive_files(current_files, archive_name)
        
        elif choice == 'F':
            get_files_details(current_files)
        
        elif choice == 'G':
            current_files = original_files.copy()
            console.print(f"[green]Restored to {len(current_files)} original files.[/green]")
        
        elif choice == 'H':
            return True  # Signal to main loop to continue
        
        elif choice == 'I':
            return False # Signal to main loop to break
        
        else:
            console.print("[red]Invalid choice. Please select from A-I.[/red]")
