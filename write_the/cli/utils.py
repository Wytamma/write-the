def list_python_files(directory):
    """
    Finds all Python files in a given directory.
    Args:
      directory (Path): The directory to search for Python files.
    Returns:
      list: A list of Path objects for each Python file found.
    Examples:
      >>> list_python_files(Path('/home/user/code'))
      [Path('/home/user/code/main.py'), Path('/home/user/code/utils.py')]
    """
    python_files = []
    for file in directory.glob("**/*.py"):
        python_files.append(file)
    return python_files
