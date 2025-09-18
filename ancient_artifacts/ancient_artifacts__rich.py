#large_fossil_rich

import os
import sys
from pathlib import Path 
import argparse
import datetime
from collections import defaultdict
import shutil
from rich.table import Table
from rich.console import Console
from rich import print as rprint


# Create a console instance for rich output
console = Console()


def show_data(title: str, column_list: list[str], data_list: list[tuple]):
    """
    This method prints a neat and clean table of the data provided.
    
    Parameters
    ----------
    title : str
        The title of the table.
    column_list: list[str]
        List containing the names of all columns of the table.
    data_list: list[tuple]
        List containing tuples of data to display in the table.
    """
    table = Table(title=title)
    
    for column in column_list:
        table.add_column(column)
    for idx, data_tuple in enumerate(data_list, 1):
        table.add_row(f"{idx}", *[str(item) for item in data_tuple])
    console.print(table)


pars = argparse.ArgumentParser()  # inbuilt function of argparse to parse the argument given in the cli
pars.add_argument("path", type=str)  # adding a path argument to specifiy which directory to use for scanning 

target_path = pars.parse_args().path
rprint(f"[bold green]Scanning Directory:[/bold green] {target_path}")

file_groups = defaultdict(list)  # Create a dictionary with default list for grouping 

Ancient_artifacts = []  # here we gotta store all the old files path

c_time = datetime.datetime.now()  # storing current time 

one_year_s = 365 * 24 * 60 * 60  # formula is year= (days * 24hrs * minuts * seconds)

for root, dirs, files in os.walk(target_path):  # this will scan through all the directory and sub directory starting at target_path
    for file in files:  # iterates through all the files found in the directories 
        file_path = Path(root) / file  # joining the whole file path root+ current file 
        
        mod_time = os.path.getmtime(file_path)  # get the last modification time of the files in seconds 

        file_age = c_time.timestamp() - mod_time  # caclulating the age of the files in seconds 

        if file_age > one_year_s:
            Ancient_artifacts.append(file_path)  # so cool now a list will be appended if it's older 

rprint("[bold yellow]Ancient Artifacts (>1 year old):[/bold yellow]")

# Group the files by extension
for file_path in Ancient_artifacts:
    ext = file_path.suffix.lower()  # get the lowercase of the extension 
    file_groups[ext].append(file_path)  # appending to our dict

# printing Summaries of categories and counts using Rich table
category_data = []
for ext, files in file_groups.items():
    display_ext = ext[1:] if ext else 'no extension'
    category_data.append((display_ext + 's', len(files)))

show_data(
    "Ancient Artifacts Categorized",
    ["Sr. No.", "File Type", "Count"],
    category_data
)

# For user to navigate through the categories 
choice = int(input("\nSelect the category number to list those files: ")) - 1  # -1 as our enum starts at index 1 

selected_ext = list(file_groups.keys())[choice]
selected_files = file_groups[selected_ext]
# here we convert dict-keys to list so we can access it through index properly and then we store the choice 
# selected_files store the files of selected categories 

# humanly readable age
def format_age(seconds):
    days = seconds // (24*3600)
    years = days // 365
    days = days % 365
    return f"{int(years)} years, {int(days)} days old"

# printing from oldest to newest using rich table
rprint(f"\n[bold cyan]Oldest {selected_ext[1:] if selected_ext else 'files'}:[/bold cyan]")

c_time2 = datetime.datetime.now().timestamp()

# Create Archive Directory in User's home if it does not exists 
archive_dir = Path.home() / "Archive"
archive_dir.mkdir(exist_ok=True) 

# The iterative interactive loop for the final boom bang 
while True:
    # Prepare data for rich table display
    file_data = []
    for file_path in selected_files:
        age_sec = c_time2 - os.path.getmtime(file_path)
        file_data.append((file_path.name, format_age(age_sec)))
    
    # Display files using rich table
    show_data(
        "Select a file to act on (or enter 0 to exit)",
        ["Sr. No.", "File Name", "Age"],
        file_data
    )

    # ask user to select a file number 
    file_choice = input("\nEnter the file number: ")

    # Validation for better error handling 
    if not file_choice.isdigit():
        rprint("[bold red]Invalid input. Please enter a number.[/bold red]")
        continue

    file_choice = int(file_choice)

    # Exiting the operation if that's the choice
    if file_choice == 0:
        rprint("[bold green]Exiting File Interaction[/bold green]")
        break

    # Check for valid range 
    if not (1 <= file_choice <= len(selected_files)):
        rprint("[bold red]Invalid selection. Try again[/bold red]")
        continue

    chosen_file = selected_files[file_choice - 1]

    # All available Options 
    console.print(f"\n[bold magenta]Options for {chosen_file.name}:[/bold magenta]")
    console.print("[cyan]a[/cyan] Read")
    console.print("[cyan]b[/cyan] Delete")
    console.print("[cyan]c[/cyan] Archive")
    console.print("[cyan]d[/cyan] Ignore and exit")

    #  Storing user action and lowering it 
    action = input("Choose an action: ").strip().lower()

    # Inner loop to perform multiple actions on the same selected file
    while True:
        # Read Action 
        if action == 'a':
            try:
                # open and read first 10000 characters of the file to display 
                with open(chosen_file, 'r', encoding='utf-8') as f:
                    console.print("\n[bold green]---- File content Start -------[/bold green]")
                    content = f.read(10000)
                    console.print(content)
                    console.print("[bold green]------ File Content End ----------[/bold green]\n")
            except Exception as e:
                console.print(f"[bold red]Error opening the file: {e}[/bold red]")

        # Delete Option 
        elif action == 'b':
            console.print(f"\n[bold yellow]Are you sure you want to delete this file {chosen_file}? [y/n]:[/bold yellow]")
            confirm = input().strip().lower()
            if confirm == 'y':
                try:
                    os.remove(chosen_file)  # Deleting the chosen file 
                    console.print(f"[bold green]{chosen_file} was deleted successfully.[/bold green]")
                    selected_files.remove(chosen_file)  # Removing the deleted file from the list 
                    break  # Exit inner loop as file no longer exists
                except Exception as e:
                    console.print(f"[bold red]Error {e}[/bold red]")
            else:
                console.print("[bold yellow]Deletion of the file cancelled[/bold yellow]")

        # Archive Option 
        elif action == 'c':
            try:
                # moving the file to the archive directory 
                dest = archive_dir / chosen_file.name
                shutil.move(str(chosen_file), str(dest))
                console.print(f"[bold green]{chosen_file} moved to Archive folder at: {dest}[/bold green]")
                selected_files.remove(chosen_file)  # removing from the main list 
                break  # Exit inner loop as file moved
            except Exception as e:
                console.print(f"[bold red]Error archiving {chosen_file}: {e}[/bold red]")

        # Ignoring and exiting the action 
        elif action == 'd':
            console.print("\n[bold yellow]Ignore selected. Exiting file operation interaction[/bold yellow]\n")
            break

        else:
            console.print("[bold red]Invalid action. Choose from the options above[/bold red]")

        # After performing any action except delete/archive/ignore, re-display options
        console.print("\n[bold magenta]Options for this file again:[/bold magenta]")
        console.print("[cyan]a[/cyan] Read")
        console.print("[cyan]b[/cyan] Delete")
        console.print("[cyan]c[/cyan] Archive")
        console.print("[cyan]d[/cyan] Ignore and exit")
        action = input("Your choice: ").strip().lower()
