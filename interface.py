import os
from rich.table import Table
from rich import print as rprint

def show_data(
    title: str,
    column_list: list[str],
    data_list: list[(str, str)]
):
    """
    This method prints a neat and clean table of the data provided.
    
    Parameters
    ----------
    title : str
        The title of the table.
    column_list: list[str]
        List containing the names of all columns of the table.
    data_list: list[(str, str)]
        List containing a tuple of two strings, I can use anything here.
        \nFor example: ```('C:\Me\Movies\Ballerina.mkv', '2.34')```
        \nHere, it's filepath and size so the 'column_list' will contain ```['filepath', 'size']```
    """
    table = Table(title=title)

    for column in column_list:
        table.add_column(column)

    for idx, (data, metadata) in enumerate(data_list, 1):
        table.add_row(f"{idx}", os.path.basename(data), metadata)
    rprint(table)

if __name__ == "__main__":
    pass