import pytest
from write_the.__about__ import __version__
from pathlib import Path
from write_the.cli.main import app
from write_the.llm import LLM
from typer.testing import CliRunner
import unittest.mock as mock


@pytest.fixture(scope="function")
def file_path(tmp_path) -> Path:
    temp_file = tmp_path / "test_add.py"
    temp_file.write_text("def add(a, b):\n  return a + b")
    return temp_file


@pytest.fixture
def nodes():
    return ["add"]


def test_callback_version():
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])
    assert __version__ in result.stdout
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "save, context, pretty, force",
    [
        (True, True, True, True),
        (True, True, True, False),
        (True, True, False, True),
        (True, False, True, True),
        (False, True, True, True),
    ],
)
@mock.patch(
    "write_the.llm.LLM.run",
    return_value="\n\nadd:\n  Sums 2 numbers.\n  Args:\n    a (int): The first number to add.\n    b (int): The second number to add.\n  Returns:\n    int: The sum of `a` and `b`.\n  Examples:\n    >>> add(1, 2)\n    3\n\n",
)
def test_docs_mocked(mocked_run, file_path: Path, nodes, save, context, pretty, force):
    runner = CliRunner()
    args = ["docs", str(file_path)]

    if nodes:
        for node in nodes:
            args.append("--node")
            args.append(node)

    if save:
        args.append("--save")

    if context:
        args.append("--context")

    if pretty:
        args.append("--pretty")

    if force:
        args.append("--force")

    result = runner.invoke(app, args)
    assert result.exit_code == 0
    mocked_run.assert_called_once()
    if save:
        assert "Sums 2 numbers" in file_path.read_text()
        assert file_path.name in result.stdout
    else:
        assert "Sums 2 numbers" in result.stdout


def test_mkdocs(tmp_path: Path):
    runner = CliRunner()
    args = ["mkdocs", "tests/data", "--readme", "README.md", "--out", tmp_path]
    result = runner.invoke(app, args)
    print(result.stdout)
    assert result.exit_code == 0
    files = [f.name for f in tmp_path.glob("*")]
    assert "mkdocs.yml" in files
    assert ".github" in files
    assert "docs" in files


@pytest.mark.parametrize(
    "save, pretty, force",
    [
        (True, True, True),
        (True, True, True),
        (True, True, False),
        (True, False, True),
        (False, True, True),
    ],
)
@mock.patch(
    "write_the.llm.LLM.run",
    return_value="""@pytest.mark.parametrize(
    "a, b, expected", [(2, 3, 5), (0, 5, 5), (-2, -3, -5), (2.5, 3, 5.5), (2, -3, -1)]
)
def test_add(a, b, expected):
    assert add(a, b) == expected""",
)
def test_tests_mocked(mocked_run, file_path: Path, save, pretty, force):
    runner = CliRunner()
    test_dir = file_path.parent / "docs"
    args = ["tests", str(file_path), "--out", test_dir]

    if save:
        args.append("--save")

    if pretty:
        args.append("--pretty")

    if force:
        args.append("--force")

    result = runner.invoke(app, args)
    assert result.exit_code == 0
    mocked_run.assert_called_once()
    if save:
        test_file = next(test_dir.glob("*test_add.py"))
        assert "assert add(a, b) == expected" in test_file.read_text()
        assert str(file_path) in result.stdout
    else:
        assert "assert add(a, b) == expected" in result.stdout
