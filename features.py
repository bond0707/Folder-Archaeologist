import os
import sys
import subprocess
from rich.progress import Progress

def archive_all(
    file_list    : list,
    archive_name : str,
):
    if sys.platform in ["linux", "linux2", "darwin"]:
        command = ["zip", archive_name, *file_list]
    elif sys.platform == "win32":
        command = ["powershell", "Compress-Archive", "-Path", "@(", ", ".join(file_list), ")", "-DestinationPath", archive_name, "-Force"]

    with Progress() as progress:
        compress_task = progress.add_task("[red]Compressing : ", total=None)
        subprocess.run(command, shell=True)
        progress.update(compress_task, completed=True, description="[green]Completed!")

if __name__ == "__main__":
    # all paths to have aa single quote string inside a double quote string. (to avoid error in paths like "thing1 <space> thing2")
    archive_all(
        ["'C:\\Me\\Notes\\Timepass Projects\\Folder-Archaeologist\\categories.py'", 
         "'C:\\Me\\Notes\\Timepass Projects\\Folder-Archaeologist\\interface.py'"], 
        f"'{os.path.join(os.path.dirname(__file__), 'archive.zip')}'"
    )
