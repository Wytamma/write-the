import pytest
from pathlib import Path
from write_the.utils import list_python_files


@pytest.fixture
def directory():
    return Path("tests/data")


def test_list_python_files(directory):
    python_files = list_python_files(directory)
    assert isinstance(python_files, list)
    assert len(python_files) == 3
    assert Path("tests/data/multiply_docstring.py") in python_files
    assert Path("tests/data/multiply.py") in python_files


@pytest.mark.parametrize(
    "directory, expected",
    [
        (Path("/home/user/code/empty_dir"), []),
        (Path("/home/user/code/no_py_files"), []),
    ],
)
def test_list_python_files_edge_cases(directory, expected):
    python_files = list_python_files(directory)
    assert python_files == expected
