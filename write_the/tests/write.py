from pathlib import Path
from black import format_str, FileMode
from .chain import run


def write_the_tests(
    filename: Path,
    gpt_4: bool = False
) -> str:
    """
    Formats and runs the tests for a given file.
    Args:
      filename (Path): The path to the file to be tested.
      gpt_4 (bool, optional): Whether to use GPT-4 for testing. Defaults to False.
    Returns:
      str: The formatted and tested code.
    Examples:
      >>> write_the_tests(Path("test.py"), gpt_4=True)
      "Formatted and tested code"
    """
    with open(filename, "r") as file:
        source_code = file.read()
    source_code = format_str(source_code, mode=FileMode())
    result = run(code=source_code, path=filename, gpt_4=gpt_4)
    code = result.strip().lstrip("Test Code:\n```python").lstrip("```python").lstrip("```").rstrip("```")
    return format_str(code, mode=FileMode())
