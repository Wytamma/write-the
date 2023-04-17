from pathlib import Path
from black import format_str, FileMode
from .chain import run


def write_the_tests(
    filename: Path,
    gpt_4: bool = False
) -> str:
    with open(filename, "r") as file:
        source_code = file.read()
    source_code = format_str(source_code, mode=FileMode())
    result = run(code=source_code, path=filename, gpt_4=gpt_4)
    code = result.strip().lstrip("```python").lstrip("```").rstrip("```")
    return format_str(code, mode=FileMode())
