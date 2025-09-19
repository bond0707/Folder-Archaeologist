#similarities_in_names.py

from pathlib import Path
from collections import defaultdict
from utility import parse_directory_path
import  re # better than string split() this let's us od splitiing of string through multiple delimiters in patter 
# will use re.split()


def by_similar_names(target_path,delimiters):
    print(f"The targeted path: {target_path}")
    pattern = '|'.join(map(re.escape, delimiters))
    print("Our delimiters: ", delimiters)

    # Compile regex pattern to split on delimiters so we get our wanted string 

    """
We want to split a filename into parts using many different separators, like space, dash, or underscore.

- First, we have a list of separators, like [' ', '_', '-']
- Each separator might be something special in regex (like '.' means 'any character'), so we make sure to 'escape' or 'protect' them
  using re.escape(), so they are treated exactly like normal characters, not special ones.
  For example, '.' becomes '\.' so it means a dot, not 'any character'.
- We then join all these escaped separators into one big pattern using '|', which means OR in regex.
  This pattern will say: split on this OR that OR this separator.
- So now, when we use re.split(pattern, string), it cuts the string by whichever separator it finds.

Example:
Separators: [' ', '_', '-']
Escaped: ['\\ ', '_', '\\-']
Pattern: '\\ |\\_|\\-'
String: 'dbms_pr1-file'
Split into: ['dbms', 'pr1', 'file']

This way, we can easily find the main 'dbms' part of different filenames even if they use different separators.
"""
    

    group = defaultdict(list) # will hold group of files by tokens

    for file_path in Path(target_path).rglob("*"):
        if file_path.is_file():
            # Split stem by delimiters, first token as key
            token = re.split(pattern, file_path.stem)[0] # stem excludes the extension, and then it'll be splitted based on the delimiters and the leading one will be stored 
            group[token].append(file_path) # group files by their first token
    
    #groups = group_files_by_leading_token(target_path, delimiters)

    group_list = [(token,files) for token,
                  files in group.items() if len(files) > 1 ] # List consisting of tuple (toke,files) where number of files are greater than 1
    
    group_list.sort(key=lambda x: len(x[1]), reverse=1) # sort the files in descending order based on the np. of found siilar files 

    for idx, (token, files) in enumerate(group_list, 1):
        print(f"{idx}. {token} (similars found: {len(files)})") # Prints the list 

    choice = int(input("\n Select a File of Your Choice (by number): "))

    if 1 <= choice <= len(group_list):
        token, files = group_list[choice-1] # Adjust to 0 based indexing and the and then takes the toke eg 'dbms' and the files which contains paths

        print(f"\n Files under: '{token}'")
        for idx, file_path in enumerate(files,1):
            print(f"{idx}. {file_path.name}") # priniting the index and the file name instead of path 
    
    else:
        print("Invalid Selection")

    


if __name__ == '__main__':
    target_path =parse_directory_path()

    delimiters =[' ','-','_' ] # Setting up the Delimiters on which we will group those files 


    by_similar_names(target_path,delimiters)
