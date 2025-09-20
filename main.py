# Timepass W with @Koffandaff begins....
# sure lol
# ig this is it broo, it's done

from rich.console import Console
from features import file_operations_menu
from categories import show_categories_menu
from utilities import parse_directory_path, clear_screen

console = Console()

def main():
    clear_screen()
    console.print("[bold cyan]Welcome to Folder Archaeologist![/bold cyan]")
    console.print("Ready your tools to excavate and analyze digital artifacts.\n")

    target_path = parse_directory_path()

    while True:
        file_list = show_categories_menu(target_path)

        if file_list == "exit": # Handle the new exit signal
             break

        if not file_list:
            # The user cancelled or no files were found, loop back to the menu
            continue

        continue_main_loop = file_operations_menu(file_list)

        if not continue_main_loop:
            break
    
    clear_screen()
    console.print("[bold magenta]Thank you for using Folder Archaeologist. The dig site is now closed.[/bold magenta]\n[green]Made for the [/green][red]❤ [/red][green] of code by Koffandaff and Bond0707[/green]")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[blue]Leaving the dig site already?🥺 See you at the next excavation!\n[green]Made for the [/green][red]❤ [/red][green] of code by Koffandaff and Bond0707[/green]")
