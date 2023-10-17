import os
import fnmatch
import re
import shutil


## FUNCTIONs ##########################################################################################

# patterns to exclude
abs_1 = r'abs[_ .-]'
abs_2 = r'_abs[_ .-]'
# copy = r'copy.'
archiv = r'\\archiv\\'
archiv_99 = r'\\99_archiv\\'


def find_sql_files(root_dir, search_term):
    """
    This is a search function used to locate a specific word or term within a SQL file.
    It employs case-insensitive matching. The contents within the re.search() function serve to exclude specific paths,
    such as files within an archive environment, in my case.

    Args:
        root_dir (str): root path from which the search begins, including all of its subfolders
        search_term (str): string to be search for within SQL Files

    Returns:
        list of str: A list of paths to the SQL files were the term was found
    """
    # Convert search term to lowercase
    search_term = search_term.lower()
    for root, dirs, files in os.walk(root_dir):
        for file in fnmatch.filter(files, "*.sql"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', errors='ignore') as f:
                # Convert file contents to lowercase
                file_contents = f.read().lower()
                # search but exclude (abs, archiv)
                if search_term in file_contents and \
                    not (re.search(abs_1, file) \
                        or re.search(abs_2, file) \
                        or re.search(archiv, file_path) \
                        or re.search(archiv_99, file_path)):
                    print(f"Found '{search_term}' in {file_path}")


############################################################################################

def find_indexes_in_single_file(file_path, search_term):
    """
    Find each index/instance from the search_term within a file

    Returns:
        list of str: A list of index
    """
    with open(file_path, 'r', errors='ignore') as f:
        file_contents = f.read()
    
    indexes = []
    index = file_contents.find(search_term)
    
    while index != -1:
        indexes.append(index)
        index = file_contents.find(search_term, index + len(search_term))
    
    return indexes


############################################################################################

def find_and_modify_sql_files(root_dir, search_term, new_case_statement):
    """
    If you have multiple instances of a statement in a SQL file, both in the SELECT and in subqueries or the GROUP BY clause,
    and you want to replace a specific occurrence, and you have numerous similar scripts -> standard or duplicate scripts with
    the same structure but different variables), the goal is to:

    1. Identify all scripts that contain the search term at a specific location.
    2. Create a copy of the file.
    3. Replace the desired occurrence (index) with the new statement in the copied file.

    Args:
        root_dir (str): root path from which the search begins, including all of its subfolders
        search_term (str): string to be search for within SQL Files
        new_case_statement (str): Replace the old statement with a new one

    Returns:
        list of str: A list of paths to the SQL files that were modified by replacing the specified occurrence with the new statement
    """
    for root, dirs, files in os.walk(root_dir):
        for file in fnmatch.filter(files, "*.sql"):
            file_path = os.path.join(root, file)

            # Read the content of the SQL file
            with open(file_path, 'r', errors='ignore') as f:
                file_contents = f.read()
                # print('file: ', file_contents)

            # Check if the search term "gewicht_stufe" exists in the file
            if search_term in file_contents:
                print(f"Modifying '{search_term}' in {file_path}")

                # Find the index of "gewicht_stufe" in the file contents
                index = file_contents.find(search_term)
                print('index: ', index)

                while index != -1 and index < 10920:
                    index = file_contents.find(search_term, index + len(search_term))
                    print('index in while: ', index)

                if index != -1:
                    # Search backward to find the start of the old case statement
                    start_index = file_contents.rfind("(case when nvl(snd_gew,0) = 0 then '--'", 0, index)

                    if start_index != -1:
                        # Extract the old case statement
                        old_case_statement = file_contents[start_index:index + len(search_term)]

                        # Create a modified copy of the file with "_v2" suffix
                        new_file_path = os.path.splitext(file_path)[0] + "_v2.sql"
                        shutil.copy(file_path, new_file_path)

                        # Replace the old case statement with the new one in the modified file
                        modified_contents = file_contents.replace(old_case_statement, new_case_statement)
                        with open(new_file_path, 'w') as new_file:
                            new_file.write(modified_contents)



## MAIN ##########################################################################################

if __name__ == "__main__":
    ## In Python: One backslash = 2 and a doubleslash = 4
    test_path = r"C:\\Users\\maissento\\Desktop\\ToadFiles\\Python\\SearchSpecificFileAndItsContent"

    ## run ONLY the search function (for analysis) ######################
    # find_sql_files(test_path, "weight_level")


    ### Find and Replace Filecontent in SQL File ########################
    ## Example: a case when statement which ends with the nameing ->  weight_level
    # Define the new case statement as a string
    new_case_statement = "(case when nvl(weight,0) = 0 then '--' when weight < 2001 then 'up_to_2kg' when weight < 5001 then .... ... end weight_level"
    find_and_modify_sql_files(test_path, "weight_level", new_case_statement)


    ## Find the index's of the the search term ##########################
    # indexes = find_indexes_in_single_file(test_path, search_term)

    # if indexes:
    #     print(f"Found '{search_term}' at the following indexes in the file:")
    #     for i, index in enumerate(indexes, start=1):
    #         print(f"Occurrence {i}: Index {index}")
    # else:
    #     print(f"'{search_term}' not found in the file.")

    # Output: #
    # Found 'weight_level' at the following indexes in the file:
    # Occurrence 1: Index 1275
    # Occurrence 2: Index 10920 --> here is the desired change
    # Occurrence 3: Index 2161