from pathlib import Path
import argparse

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
