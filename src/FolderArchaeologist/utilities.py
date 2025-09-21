import os
import argparse
from typing import List
from pathlib import Path
from rich.table import Table
from rich.console import Console

console = Console()

def show_data(title: str, column_list: List[str], data_rows: List[List[str]]):
    """
    This method prints a neat and clean table of the data provided.
    
    Parameters
    ----------
    title : str
        The title of the table.
    column_list: list[str]
        List containing the names of all columns of the table.
    data_rows: list[list[str]]
        A list of rows, where each row is a list of strings for the columns.
    """
    if not data_rows and title == "Currently Excavated Artifacts":
        console.print("[yellow]There are no artifacts in the current selection.[/yellow]")
        return

    if not data_rows:
        console.print(f"[yellow]No data to display for '{title}'.[/yellow]")
        return

    table = Table(title=f"[bold cyan]{title}[/bold cyan]", show_header=True, header_style="bold magenta")

    for column in column_list:
        table.add_column(column, justify="left", no_wrap=False)
    
    for row in data_rows:
        table.add_row(*row)
        
    console.print(table)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_size(bytes_size):
    """Converts byte size to a human-readable format."""
    if bytes_size is None:
        return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def parse_directory_path(default_path=None):
    """Parses directory path from command-line arguments, with a default."""
    if default_path is None:
        default_path = str(Path.home())
    
    parser = argparse.ArgumentParser(
        description="A CLI tool for digital archaeology and file excavation.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=default_path,
        help="The target dig site to excavate."
    )
    args = parser.parse_args()
    
    path = Path(args.path)
    if not path.is_dir():
        print(f"Error: The path '{path}' is not a valid dig site. Exiting.")
        exit(1)
        
    return path
