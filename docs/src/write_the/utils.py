from pathlib import Path
import libcst as cst
from black import FileMode, format_str


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


def load_source_code(file: Path):
    with open(file, "r") as file:
        return file.read()


def format_source_code(source_code):
    return format_str(source_code, mode=FileMode())


def create_tree(source_code):
    return cst.parse_module(source_code)
