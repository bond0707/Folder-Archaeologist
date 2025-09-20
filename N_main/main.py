# Timepass W with @Dhruvil begins....
# sure lol
from utility import parse_directory_path, format_size
from categories import show_categories_menu
from features import file_operations_menu

def main():
    print("Welcome to File Management CLI!")
    print("Use this program to categorize, explore, and manage your files.\n")

    target_path = parse_directory_path()

    while True:  # Main menu loop
        # Show main categories menu and get the result
        file_list = show_categories_menu(target_path)
        # Here, show_categories_menu should return selected files list (to implement in categories.py)

        if not file_list:
            print("No files selected or found. Returning to main menu...\n")
            continue

        # Pass selected files list to features operations menu
        back_to_main = file_operations_menu(file_list)

        if not back_to_main:
            # User chose to exit completely from operations menu
            print("Exiting program. Thank you for using the tool.")
            break
        else:
            # User chose to go back to category selection menu
            print("\nReturning to Categories Menu...\n")

if __name__ == '__main__':
    main()


