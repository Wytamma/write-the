import typer
from write_the.__about__ import __version__
from write_the.docs import write_the_docs
from .utils import list_python_files
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from typing import List

app = typer.Typer()


@app.callback()
def callback():
    """
    Use GPT to code without having to copy-paste.
    """


@app.command()
def docs(
    file: Path = typer.Argument(..., help="Path to the file to generate docs."),
    inplace: bool = typer.Option(
        False, "--inplace", "-i", help="Replace the contents of the file."
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Generate docstings even if they already exist."
    ),
    context: bool = typer.Option(
        False, "--context", "-c", help="Send context with nodes."
    ),
    nodes: List[str] = typer.Option(
        None,
        "--node",
        "-n",
        help="Generate docs for specific nodes (functions and classes).",
    ),
):
    """
    Document and format your code!
    """
    if file.is_dir():
        files = list_python_files(file)
    else:
        assert file.suffix == ".py"
        files = [file]
    for file in files:
        if len(files) > 1:
            typer.secho(file, fg="green")
        result = write_the_docs(
            file, nodes=nodes, force=force, inplace=inplace, context=context
        )
        if inplace:
            with open(file, "w") as f:
                f.writelines(result)
        else:
            syntax = Syntax(result, "python")
            console = Console()
            console.print(syntax)


@app.command()
def tests():
    raise NotImplementedError()


@app.command()
def refactor():
    raise NotImplementedError()


@app.command()
def optimise():
    raise NotImplementedError()
