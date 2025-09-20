import os
from datetime import datetime as dt
from pathlib import Path
from collections import defaultdict
import re
from utility import parse_directory_path

def categorize_by_extension(target_path):
    """
    Groups files by their extension (file type).

    Returns:
        dict: Dictionary mapping extensions to list of file paths
    """
    same_species = {}  # dict[str, list] -> Groups files sharing the same extension

    for (path, folders, files) in os.walk(target_path):  # Loop through all directories and files
        # path: current folder path; folders: list of subfolders; files: list of files in 'path'
        for file in files:  # Loop through each file in the current directory
            fossil = os.path.join(path, file)  # Full path for current file
            fossil_type = os.path.basename(fossil).split(".")[-1]  # Get file extension
            
            # Grouping by extension
            if fossil_type in same_species.keys():
                same_species[fossil_type].append(fossil)  # Add to existing group
            else:
                same_species[fossil_type] = [fossil]  # Create new group for this extension
    
    return same_species

def categorize_by_size(target_path):
    """
    Finds all files larger than 500 MB.

    Returns:
        list: List of tuples (file_path, size_in_bytes) sorted by size descending
    """
    large_fossils = []  # All files larger than 500 MB (tuples: (path, size))

    for (path, folders, files) in os.walk(target_path):  # Loop through directory tree
        for file in files:  # Each file found
            fossil = os.path.join(path, file)  # Get the full path of the file
            
            fossil_size = os.path.getsize(fossil)  # File size in bytes
            
            # Check for large file (greater than 500MB)
            if fossil_size > 524288000:  # 500 MB in bytes
                large_fossils.append((fossil, fossil_size))  # Add to large fossils list
    
    # Sort from biggest to smallest
    large_fossils.sort(key=lambda x: x[1], reverse=True)
    return large_fossils

def categorize_by_age(target_path):
    """
    Finds all files older than 1 year.

    Returns:
        list: List of tuples (file_path, age_in_seconds) sorted by age descending
    """
    ancient_artifacts = []  # All files older than 1 year (tuples: (path, age))

    for (path, folders, files) in os.walk(target_path):  # Directory tree traversal
        for file in files:  # Every file in dir
            fossil = os.path.join(path, file)  # Get full file path
            
            # Calculate age of file
            fossil_age = dt.now().timestamp() - os.path.getmtime(fossil)  # Age in seconds
            
            # Check for ancient artifact: older than 1 year
            if fossil_age > 31557600:  # 1 year in seconds
                ancient_artifacts.append((fossil, fossil_age))  # Add to ancient artifacts list
    
    # Sort from oldest to newest
    ancient_artifacts.sort(key=lambda x: x[1], reverse=True)
    return ancient_artifacts

def show_similarity_by_name(target_path, delimiters):
    """
    Provides interactive prompt for user to search by specific token or list grouped tokens
    """
    is_specific = input("\nAre you looking for a specific name/token? [y/n]: ").strip().lower()
    if is_specific == 'y':
        search_token = input("Enter the specific token to search for: ").strip()
        matched_files = search_by_specific_token(target_path, delimiters, search_token)
        if matched_files:
            print(f"\nFiles with token '{search_token}':")
            for idx, file_path in enumerate(matched_files, 1):
                print(f"{idx}. {file_path.name}")
        else:
            print(f"No files found with token '{search_token}'.")
    else:
        similar_groups = categorize_by_similar_names(target_path, delimiters)[:10]
        print(f"\n=== Top 10 Similar Name Groups ===")
        for idx, (token, files) in enumerate(similar_groups, 1):
            print(f"{idx}. {token} (similars found: {len(files)})")

def categorize_by_similar_names(target_path, delimiters):
    """
    Groups files by similar names using delimiters to extract leading tokens.

    We want to split a filename into parts using many different separators (delimiters), like space, dash, or underscore.

    - First, we have a list of separators, like [' ', '_', '-']
    - Each separator might be something special in regex (like '.' means 'any character'), so we make sure to 'escape' or 'protect' them
      using re.escape(), so they are treated exactly like normal characters, not special ones.
      For example, '.' becomes '\.' so it means a dot, not 'any character'.
    - Join all these escaped separators into one big pattern using '|', which means OR in regex.
      This pattern will say: split on this OR that OR this separator.
    - When we use re.split(pattern, string), it cuts the string by whichever separator it finds.

    Example:
    Separators: [' ', '_', '-']
    Escaped: ['\\ ', '_', '\\-']
    Pattern: '\\ |\\_|\\-'
    String: 'dbms_pr1-file'
    Split into: ['dbms', 'pr1', 'file']

    This way, we can easily find the main 'dbms' part of different filenames even if they use different separators.
    
    Args:
        target_path: Path to scan
        delimiters: List of delimiters to split filenames on

    Returns:
        list: List of tuples (token, [Path,...]) sorted by number of files descending
    """
    pattern = '|'.join(map(re.escape, delimiters))     # Regex pattern for splitting stem on delimiters
    group = defaultdict(list)      # Will hold group of files by tokens (token: [file paths])

    for file_path in Path(target_path).rglob("*"):     # Recursive loop over all files under target_path
        if file_path.is_file():
            # Split stem by delimiters, use first part (token) as group key
            token = re.split(pattern, file_path.stem)[0]    # stem: filename minus extension
            group[token].append(file_path)                  # group files by their first token

    # Only show groups with more than one file
    group_list = [
        (token, files) for token, files in group.items() if len(files) > 1
    ]

    # Sort groups by number of files (descending)
    group_list.sort(key=lambda x: len(x[1]), reverse=True)
    return group_list

def search_by_specific_token(target_path, delimiters, search_token):
    """
    Returns all files whose token matches 'search_token'
    
    Args:
        target_path: Path to search files
        delimiters: Delimiters to split by
        search_token: The token to search for (case-insensitive)
    """
    pattern = '|'.join(map(re.escape, delimiters))
    matched_files = []  # List to store matched files

    for file_path in Path(target_path).rglob("*"):
        if file_path.is_file():
            token = re.split(pattern, file_path.stem)[0]
            if token.lower() == search_token.lower():    # Case-insensitive match
                matched_files.append(file_path)

    return matched_files

#Important to interact wiht the user idk how i was stuck so used ai
def show_similarity_selection(target_path, delimiters):
    """
    Interactive similarity by names menu augmented to return selected files list.

    Uses:
    - categorize_by_similar_names()
    - search_by_specific_token()

    Returns:
        list: Selected files list or empty
    """
    is_specific = input("\nAre you looking for a specific name/token? [y/n]: ").strip().lower()
    
    if is_specific == 'y':
        search_token = input("Enter the specific token to search for: ").strip()
        matched_files = search_by_specific_token(target_path, delimiters, search_token)
        
        if matched_files:
            print(f"\nFiles with token '{search_token}':")
            for idx, file_path in enumerate(matched_files, 1):
                print(f"{idx}. {file_path.name}")
            # Ask user to select a file from these matched ones
            select = int(input("\nSelect file number to operate on, or 0 to cancel: "))
            if select == 0:
                return []
            if 1 <= select <= len(matched_files):
                return [matched_files[select - 1]]
            else:
                print("Invalid selection, returning no files.")
                return []
        else:
            print(f"No files found with token '{search_token}'. Returning no files.")
            return []
    else:
        # Show groups of similar files
        similar_groups = categorize_by_similar_names(target_path, delimiters)[:10]
        print(f"\n=== Top 10 Similar Name Groups ===")
        for idx, (token, files) in enumerate(similar_groups, 1):
            print(f"{idx}. {token} (similars found: {len(files)})")
        # User selects which group they'd like
        select = int(input("\nSelect token number to view files, or 0 to cancel: "))
        if select == 0:
            return []
        if 1 <= select <= len(similar_groups):
            return similar_groups[select - 1][1]  # Return list of files for that token group
        else:
            print("Invalid selection, returning no files.")
            return []


def show_categories_menu(target_path):
    """
    Shows the main categories menu and handles user selection.

    Args:
        target_path: Path to scan for files

    Returns:
        list: List of user-selected file paths (Path objects) or empty list if none selected or canceled
    """
    delimiters = [' ', '-', '_']  # List of possible separators to use in 'similar by name'
    
    print("\n=== File Categories ===")
    print("1. By Extension (File Types)")
    print("2. By Size (Large Files >500MB)")
    print("3. By Age (Files >1 year old)")
    print("4. By Similar Names (groups files based on first part of name split on delimiters)")
    
    # Prompt user to select a category
    try:
        choice = int(input("\nSelect a category to explore (1-4): "))
    except ValueError:
        print("Invalid input, please enter a number between 1 and 4.")
        return []
    
    if choice == 1:
        # Get dictionary of extension -> files
        extensions = categorize_by_extension(target_path)
        print(f"\n=== Top 10 File Extensions ===")
        
        # Sort top 10 extensions by number of files descending
        sorted_extensions = sorted(extensions.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        
        # Display the sorted extensions with counts
        for idx, (ext, files) in enumerate(sorted_extensions, 1):
            print(f"{idx}. {ext if ext else 'no extension'} ({len(files)} files)")
        
        # Allow user to select which extension group to get files from
        try:
            select = int(input("\nSelect extension number for files, or 0 to cancel: "))
        except ValueError:
            print("Invalid selection. Returning no files.")
            return []
        
        if select == 0:
            return []
        if 1 <= select <= len(sorted_extensions):
            return sorted_extensions[select - 1][1]  # Return list of files for selected extension
        else:
            print("Invalid selection, returning no files.")
            return []
    
    elif choice == 2:
        # List of (file_path, size) tuples for large files
        large_files = categorize_by_size(target_path)[:10]
        print(f"\n=== Top 10 Largest Files ===")
        
        # Display human readable size list to user
        for idx, (file_path, size) in enumerate(large_files, 1):
            size_mb = size / (1024 * 1024)
            print(f"{idx}. {os.path.basename(file_path)} ({size_mb:.1f} MB)")
        
        # Prompt user to select a file or cancel
        try:
            select = int(input("\nSelect file number to operate on, or 0 to cancel: "))
        except ValueError:
            print("Invalid selection. Returning no files.")
            return []
        
        if select == 0:
            return []
        if 1 <= select <= len(large_files):
            return [large_files[select - 1][0]]  # Return selected file in list
        else:
            print("Invalid selection, returning no files.")
            return []
    
    elif choice == 3:
        # List of (file_path, age) tuples for older files
        old_files = categorize_by_age(target_path)[:10]
        print(f"\n=== Top 10 Oldest Files ===")
        
        # Display age in years with filename
        for idx, (file_path, age) in enumerate(old_files, 1):
            age_years = age / 31557600  # Seconds to years
            print(f"{idx}. {os.path.basename(file_path)} ({age_years:.1f} years old)")
        
        # Prompt user to select file or cancel
        try:
            select = int(input("\nSelect file number to operate on, or 0 to cancel: "))
        except ValueError:
            print("Invalid selection. Returning no files.")
            return []
        
        if select == 0:
            return []
        if 1 <= select <= len(old_files):
            return [old_files[select - 1][0]]
        else:
            print("Invalid selection, returning no files.")
            return []
    
    elif choice == 4:
        # Call the enhanced similarity selection menu that returns selected files
        return show_similarity_selection(target_path, delimiters)
    
    else:
        print("Invalid category selection.")
        return []

if __name__ == "__main__":
    # Parse the path where files are stored; default is home directory
    target_path = parse_directory_path()
    show_categories_menu(target_path)
