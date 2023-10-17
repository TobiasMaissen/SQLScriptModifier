# SQLScriptModifier
Say goodbye to manual script identification and updates. New Requirements -> effortlessly modify SQL scripts with SQLScriptModifier

**SQLScriptModifier** is a versatile Python tool designed to simplify the modification of SQL script files, especially when you have multiple instances of a specific statement to replace within your SQL code.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

## Features

- **Effortless SQL Script Modification**: With **SQLScriptModifier**, you can easily identify, create copies of, and replace specific occurrences of a statement within your SQL files.
- **Flexible Configuration**: Specify the root path for the search and provide the search term and the new statement to streamline your SQL script updates.
- **Exclusion Patterns**: Exclude specific paths, such as archive environments, to refine your search results.
- **Powerful Searching**: Utilize case-insensitive matching to find the desired statements within SQL files.
- **Modification Logs**: Get immediate feedback on modified files, making it easy to track changes.

## Installation

1. Clone or download this repository.
2. Ensure you have Python installed (Python 3 recommended).
3. Install the required Python packages by running: `pip install fnmatch re`

## Usage

### Running the Search Function

To analyze SQL files and identify instances of a specific search term (e.g., "weight_level"), use the function:

```python
find_sql_files
```

### Modifying SQL Scripts

To modify SQL scripts with **SQLScriptModifier**, follow these steps:

1. Define the root path from which the search will begin, including all its subfolders.
2. Specify the search term to identify specific occurrences within SQL files with the function:

```python
find_indexes_in_single_file
```
   
3. Provide the new statement that will replace the old occurrences.
5. use the function:

```python
find_and_modify_sql_files
```

**SQLScriptModifier** will locate the specified occurrences, create copies of the files, and replace the desired statements with the new ones in the copied files.
