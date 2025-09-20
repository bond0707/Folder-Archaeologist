import re
from pathlib import Path
from rich.text import Text
from rich.console import Console
from datetime import datetime as dt
from collections import defaultdict
from utilities import format_size, clear_screen, show_data

console = Console()

def categorize_by_extension(target_path):
    """Groups files by their extension."""
    extensions = defaultdict(list)
    for file_path in Path(target_path).rglob("*"):
        if file_path.is_file():
            # Use file_path.suffix which includes the dot, or a placeholder
            ext_key = file_path.suffix[1:] if file_path.suffix else "no_extension"
            extensions[ext_key].append(str(file_path))
    return extensions

def categorize_by_size(target_path):
    """Finds all files larger than 500 MB."""
    large_files = []
    # 500 * 1024 * 1024 bytes
    size_threshold = 524288000
    for file_path in Path(target_path).rglob("*"):
        if file_path.is_file():
            try:
                size = file_path.stat().st_size
                if size > size_threshold:
                    large_files.append((str(file_path), size))
            except (FileNotFoundError, PermissionError):
                # Skip files that can't be accessed or might be deleted during scan
                continue
    large_files.sort(key=lambda x: x[1], reverse=True)
    return large_files

def categorize_by_age(target_path):
    """Finds all files older than 1 year."""
    old_files = []
    one_year_in_seconds = 31557600
    current_time = dt.now().timestamp()
    
    for file_path in Path(target_path).rglob("*"):
        if file_path.is_file():
            try:
                modified_time = file_path.stat().st_mtime
                age = current_time - modified_time
                if age > one_year_in_seconds:
                    old_files.append((str(file_path), age))
            except (FileNotFoundError, PermissionError):
                # Skip files that can't be accessed
                continue

    old_files.sort(key=lambda x: x[1], reverse=True)
    return old_files

def categorize_by_similar_names(target_path, delimiters):
    """
    Groups files by the first significant token in their names.
    This version is improved to handle various naming conventions more reliably.
    """
    # Create a regex pattern to split by any of the delimiters
    pattern = '|'.join(map(re.escape, delimiters))
    groups = defaultdict(list)

    for file_path in Path(target_path).rglob("*"):
        if file_path.is_file():
            # Split the filename (without extension) into parts
            tokens = re.split(pattern, file_path.stem)
            # Find the first non-empty token as the key
            group_key = next((token.lower() for token in tokens if token), None)
            
            if group_key:
                groups[group_key].append(str(file_path))

    # Filter out groups with only one file, as they are not "similar"
    similar_groups = [(token, files) for token, files in groups.items() if len(files) > 1]
    
    # Sort by the number of files in each group (most common first)
    similar_groups.sort(key=lambda x: len(x[1]), reverse=True)
    return similar_groups

def show_similarity_selection(target_path, delimiters):
    """
    Interactive menu for finding files with similar names.
    """
    clear_screen()
    is_specific = input("\nAre you looking for a specific inscription/token? [y/n]: ").strip().lower()
    
    if is_specific == 'y':
        search_token = input("Enter the specific inscription to search for: ").strip().lower()
        if not search_token:
            console.print("[yellow]No inscription entered.[/yellow]")
            return []

        matched_files = search_by_specific_token(target_path, delimiters, search_token)

        if matched_files:
            file_rows = [[str(idx), Path(fp).name] for idx, fp in enumerate(matched_files, 1)]
            show_data(f"Artifacts with inscription '{search_token}'", ["#", "Artifact Name"], file_rows)
            # Automatically return all matched files for operations
            return matched_files
        else:
            console.print(f"[yellow]No artifacts found with inscription '{search_token}'.[/yellow]")
            input("\nPress Enter to return to the menu.")
            return []
    else:
        # CORRECTED: Ensures the improved categorization logic is called correctly.
        similar_groups = categorize_by_similar_names(target_path, delimiters)[:10]
        if not similar_groups:
            console.print("[yellow]No pottery shard clusters found.[/yellow]")
            input("\nPress Enter to return to the menu.")
            return []
            
        group_rows = [[str(idx), token, str(len(files))] for idx, (token, files) in enumerate(similar_groups, 1)]
        show_data("Top 10 Pottery Shard Clusters", ["#", "Inscription", "Artifact Count"], group_rows)
        
        try:
            select = int(input("\nSelect cluster number to examine artifacts, or 0 to cancel: "))
            if 1 <= select <= len(similar_groups):
                return similar_groups[select - 1][1]
        except (ValueError, IndexError):
            pass # Handles invalid input gracefully
        
        console.print("[red]Invalid selection or cancelled.[/red]")
        return []

def search_by_specific_token(target_path, delimiters, search_token):
    """
    Returns all files where the search token appears in the filename stem.
    """
    pattern = '|'.join(map(re.escape, delimiters))
    matched_files = []

    for file_path in Path(target_path).rglob("*"):
        if file_path.is_file():
            tokens = [token.lower() for token in re.split(pattern, file_path.stem) if token]
            if search_token in tokens:
                matched_files.append(str(file_path))

    return matched_files

def show_categories_menu(target_path):
    """
    Shows the main categories menu and handles user selection.
    """
    clear_screen()
    delimiters = [' ', '-', '_', '.']
    
    # 1. ASCII Art and Path
    title_art = Text(
        r"""
 _____                                                                                                 _____
( ___ )                                                                                               ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   |
 |   |   ___  __        __   ___  __           __   __             ___  __        __   __     __  ___  |   |
 |   |  |__  /  \ |    |  \ |__  |__)     /\  |__) /  ` |__|  /\  |__  /  \ |    /  \ / _` | /__`  |   |   |
 |   |  |    \__/ |___ |__/ |___ |  \    /~~\ |  \ \__, |  | /~~\ |___ \__/ |___ \__/ \__> | .__/  |   |   |
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___|
(_____)                                                                                               (_____)
""", style="bold yellow"
    )
    console.print(title_art)
    console.print(f"[bold cyan]Excavation Site:[/] [green]{target_path}[/green]\n")

    # 2. Category Table
    menu_rows = [
        ["1", "By Material Type", "Group artifacts by composition (e.g., .txt, .jpg)."],
        ["2", "Large Fossils", "Find artifacts larger than 500MB."],
        ["3", "Ancient Artifacts", "Find artifacts older than 1 year."],
        ["4", "Pottery Shard Clusters", "Group artifacts with similar naming patterns."]
    ]
    show_data("Dig Site Map", ["#", "Find", "Description"], menu_rows)
    
    try:
        choice = int(input("\nSelect a dig site to explore (1-4), or 0 to leave the excavation: "))
    except ValueError:
        console.print("[red]Invalid input, please enter a number.[/red]")
        return []

    # Clear screen after user makes a valid choice before showing results
    if 1 <= choice <= 4:
        clear_screen()
    
    if choice == 1:
        extensions = categorize_by_extension(target_path)
        sorted_extensions = sorted(extensions.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        if not sorted_extensions: 
            console.print("[yellow]No artifacts found.[/yellow]")
            input("Press Enter to return to the dig map.")
            return []

        rows = [[str(idx), ext, str(len(files))] for idx, (ext, files) in enumerate(sorted_extensions, 1)]
        show_data("Top 10 Material Types by Count", ["#", "Material", "Artifact Count"], rows)
        
        try:
            select = int(input("\nSelect material number for artifacts, or 0 to go back: "))
            if 1 <= select <= len(sorted_extensions):
                return sorted_extensions[select - 1][1]
        except (ValueError, IndexError):
            pass
    
    elif choice == 2:
        large_files = categorize_by_size(target_path)[:10]
        if not large_files:
            console.print("[yellow]No large fossils (>500MB) found.[/yellow]")
            input("Press Enter to return to the dig map.")
            return []

        rows = [[str(idx), Path(fp).name, format_size(size)] for idx, (fp, size) in enumerate(large_files, 1)]
        show_data("Top 10 Largest Fossils (>500MB)", ["#", "Fossil Name", "Size"], rows)
        
        return [fp for fp, size in large_files]

    elif choice == 3:
        old_files = categorize_by_age(target_path)[:10]
        if not old_files:
            console.print("[yellow]No ancient artifacts (>1 year) found.[/yellow]")
            input("Press Enter to return to the dig map.")
            return []
        
        rows = [[str(idx), Path(fp).name, f"{(age / 31557600):.1f} years"] for idx, (fp, age) in enumerate(old_files, 1)]
        show_data("Top 10 Ancient Artifacts (>1 year)", ["#", "Artifact Name", "Age"], rows)
        
        return [fp for fp, age in old_files]

    elif choice == 4:
        return show_similarity_selection(target_path, delimiters)
    
    elif choice == 0:
        return "exit" 

    else:
        console.print("[red]Invalid dig site selection.[/red]")

    return []
