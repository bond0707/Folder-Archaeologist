from pathlib import Path
import argparse

# Helper function to convert size in bytes to human readable format (KB, MB, GB, etc.)
def format_size(bytes_size):
    """
    Converts byte size to human readable format.

    Parameters:
    -----------
    bytes_size : int
        Size in bytes.

    Returns:
    --------
    str
        Human readable size string.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024

def parse_directory_path(default_path=None):
    
    
    if default_path is None:
        default_path = str(Path.home()) # default path if the path is not given 
    
    parser = argparse.ArgumentParser(description="Scan Directory Path") 
    parser.add_argument(
        "path",
        nargs="?",
        default=default_path,
        help=f"Directory to scan (default: {default_path})"
    ) # Storinf the argument 
    args = parser.parse_args()
    return Path(args.path) # returning the path
