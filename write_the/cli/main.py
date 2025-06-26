import typer
import os
from write_the.models import models
from write_the.__about__ import __version__
from write_the.commands import write_the_tests, write_the_mkdocs, write_the_converters
from write_the.utils import list_python_files
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import List, Optional
from black import InvalidInput
from asyncio import run, gather
from functools import wraps

from .tasks import async_cli_task
from .model import get_default_model, set_default_model


class AsyncTyper(typer.Typer):
    def async_command(self, *args, **kwargs):
        def decorator(async_func):
            @wraps(async_func)
            def sync_func(*_args, **_kwargs):
                return run(async_func(*_args, **_kwargs))

            self.command(*args, **kwargs)(sync_func)
            return async_func

        return decorator


app = AsyncTyper()

def _get_model_callback(value: str):
    if value is None:
        return get_default_model()
    if value not in models:
        raise typer.BadParameter(f"Model '{value}' not found!")
    return value

def _print_version(ctx: typer.Context, value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback(context_settings={"help_option_names": ["-h", "--help"]})
def callback(
    version: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
        help="Show the pipeline version.",
        is_eager=True,
        callback=_print_version,
        show_default=False,
    )
):
    """
    AI-powered Code Generation and Refactoring Tool
    """


@app.async_command()
async def docs(
    file: List[Path] = typer.Argument(..., help="Path to the code file/folder."),
    nodes: List[str] = typer.Option(
        None,
        "--node",
        "-n",
        help="Generate docs for specific nodes (functions and classes).",
    ),
    save: bool = typer.Option(
        False,
        "--save/--print",
        "-s",
        help="Save the docstrings to file or print to stdout.",
    ),
    pretty: bool = typer.Option(
        False, "--pretty/--plain", "-p", help="Syntax highlight and format the output."
    ),
    context: bool = typer.Option(
        False,
        "--context/--no-context",
        "-c",
        help="Send context (other nodes) with nodes.",
    ),
    background: bool = typer.Option(
        True,
        "--background/--no-background",
        "-g",
        help="Send background (other code) with nodes.",
    ),
    force: bool = typer.Option(
        False,
        "--force/--no-force",
        "-f",
        help="Generate docstings even if they already exist.",
    ),
    update: bool = typer.Option(
        False,
        "--update/--no-update",
        "-u",
        help="Update the existing docstrings.",
    ),
    batch: bool = typer.Option(
        False, "--batch/--no-batch", "-b", help="Send each node as a separate request."
    ),
    model: str = typer.Option(
        None,
        "--model",
        "-m",
        help="The model to use for generating the docstrings.",
        callback=_get_model_callback,
    ),
):
    """
    Document your code with AI.
    """
    files = []
    for f in file:
        if f.is_dir():
            files.extend(list_python_files(f))
        else:
            if f.suffix != ".py":
                raise typer.BadParameter("File must be a .py file or a directory.")
            files.append(f)
    with Progress(
        SpinnerColumn(),
        TextColumn("{task.description}"),
        transient=True,
        auto_refresh=True,
    ) as progress:
        tasks = []
        print_status = len(files) > 1
        for file in files:
            tasks.append(
                async_cli_task(
                    file,
                    nodes=nodes,
                    force=force,
                    update=update,
                    save=save,
                    context=context,
                    background=background,
                    pretty=pretty,
                    batch=batch,
                    print_status=print_status,
                    progress=progress,
                    model=model,
                )
            )
        await gather(*tasks)


@app.command()
def mkdocs(
    code_dir: Path = typer.Argument(
        ...,
        help="Path to the projects code. Uses docstings to build API reference.",
        file_okay=False,
    ),
    readme: Optional[Path] = typer.Option(
        None, help="Path to projects README (used to create index.md).", dir_okay=False
    ),
    out_dir: Path = typer.Option(
        Path("."),
        "--out",
        "-o",
        help="Path to save output (docs/ and yaml). Defaults to current directory.",
    ),
):
    """
    Generate a mkdocs website for a project including the API reference.
    """
    write_the_mkdocs(code_dir=code_dir, readme=readme, out_dir=out_dir)


@app.async_command()
async def tests(
    file: Path = typer.Argument(..., help="Path to the code file/folder."),
    tests_dir: Path = typer.Option(
        "tests", "--out", "-o", help="Path to save the docs."
    ),
    save: bool = typer.Option(
        False,
        "--save/--print",
        "-s",
        help="Save the tests to the tests directory or print to stdout.",
    ),
    pretty: bool = typer.Option(
        False, "--pretty/--plain", "-p", help="Syntax highlight the output."
    ),
    group: bool = typer.Option(
        False,
        "--group/--flat",
        "-g",
        help="Group the tests into folder or keep them flat.",
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Generate tests even if they already exist."
    ),
    empty: bool = typer.Option(
        False,
        "--empty",
        "-e",
        help="Save empty files if a test creation fails. This will prevent write-the from regenerating failed test creations.",
    ),
    model: str = typer.Option(
        None,
        "--model",
        "-m",
        help="The model to use for generating the tests.",
        callback=_get_model_callback,
    ),
):
    """
    Generate tests for your code.
    """
    current_tests = list_python_files(tests_dir)
    if file.is_dir():
        files = list_python_files(file)
    else:
        if file.suffix != ".py":
            raise typer.BadParameter("File must be a .py file or a directory.")
        files = [file]
    for file in files:
        if file.stem.startswith("_"):
            continue
        parts = list(file.parts[1:-1])
        parts = ["test"] + parts
        test_file = f"{'_'.join(parts)}_{file.stem}.py"
        if group:
            parts.append(test_file)
            test_file = Path(os.path.join(*parts))
        test_file_path = tests_dir / test_file
        if (
            test_file_path.exists()
            and (not force and save)
            or (test_file in current_tests)
        ):
            continue
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            failed = False
            progress.add_task(description=f"{file}", total=None)
            try:
                result = await write_the_tests(file, model=model)
            except InvalidInput:
                failed = True
                result = ""
            progress.stop()
            if len(files) > 1 or save or failed:
                icon = "❌" if failed else "✅"
                colour = "red" if failed else "green"
                typer.secho(f"{icon} {file}", fg=colour)
            if failed and not empty:
                continue
            if save:
                # create test file
                tests_dir.mkdir(exist_ok=True)
                test_file_path.parent.mkdir(exist_ok=True, parents=True)
                with open(test_file_path, "w") as f:
                    f.writelines(result)
            elif pretty:
                syntax = Syntax(result, "python")
                console = Console()
                console.print(syntax)
            else:
                typer.echo(result)


@app.async_command()
async def convert(
    in_file: Path = typer.Argument(..., help="Path to the code file.", dir_okay=False, exists=True),
    out_file: Optional[Path] = typer.Argument(
        None,
        help="File to save the output to.",
        dir_okay=False,
    ),
    input_format: str = typer.Option(
        None,
        "--input-format",
        "-i",
        help="The input format of the file.",
    ),
    output_format: str = typer.Option(
        None,
        "--output-format",
        "-o",
        help="The format to convert the file to.",
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Generate output file even if they already exist."
    ),
    pretty: bool = typer.Option(
        False, "--pretty/--plain", "-p", help="Syntax highlight the output."
    ),
    model: str = typer.Option(
        None,
        "--model",
        "-m",
        help="The model to use for generating the tests.",
        callback=_get_model_callback,
    ),
):
    """
    Convert input file to a different format.
    """
    if not force and (out_file and out_file.exists()):
        typer.secho("Output file exists!", fg="red")
        return typer.Exit(1)
    if not input_format:
        input_format = in_file.suffix
    if not output_format and not out_file:
        typer.secho("Output format required!", fg="red")
        return typer.Exit(1)
    if not output_format:
        output_format = out_file.suffix
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        failed = False
        progress.add_task(description=f"converting {in_file.name} to {output_format}", total=None)
        try:
            result = await write_the_converters(
                in_file,
                input_format=input_format,
                output_format=output_format,
                model=model
            )
        except InvalidInput:
            failed = True
            result = ""
        progress.stop()
        if out_file or failed:
            icon = "❌" if failed else "✅"
            colour = "red" if failed else "green"
            typer.secho(f"{icon} {in_file} -> {out_file}", fg=colour)
        if failed:
            return typer.Exit(1)
        if out_file:
            with open(out_file, "w") as f:
                f.writelines(result)
        elif pretty:
            syntax = Syntax(result, "python")
            console = Console()
            console.print(syntax)
        else:
            typer.echo(result)


@app.command()
def model(
     desired_model: Optional[str] = typer.Argument(
        None,
        help="Set the default model.",
    ),
    list: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="List all available models.",
    ),
):
    """
    View or set the default model.
    """
    default_model = get_default_model()
    if list:
        from rich import table, print
        table_ = table.Table()
        table_.add_column("Name", justify="left", style="cyan")
        table_.add_column("Context", justify="left", style="magenta")
        table_.add_column("Default", justify="left", style="green")
        for name, model in models.items():
            if name == default_model:
                table_.add_row(name, f"{model['context_window']}", "✅")
            else:
                table_.add_row(name, f"{model['context_window']}", "")
        print(table_)
        return typer.Exit(0)
    if desired_model:
        if desired_model not in models:
            typer.secho(f"Model '{desired_model}' not found!", fg="red")
            return typer.Exit(1)
        set_default_model(desired_model)
        typer.echo(f"Default model: {desired_model}")
        return typer.Exit(0)
    typer.echo(default_model)




@app.command()
def refactor():
    """Refactor your code with AI (not implemented yet)."""
    raise NotImplementedError()


@app.command()
def optimise():
    """Optimise your code with AI (not implemented yet)."""
    raise NotImplementedError()
