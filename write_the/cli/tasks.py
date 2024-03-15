from write_the.commands import write_the_docs
from write_the.errors import FileSkippedError
from write_the.utils import create_tree, format_source_code, load_source_code
from rich.syntax import Syntax
from rich.progress import Progress
from typing import List
from pathlib import Path
from openai.error import InvalidRequestError


async def async_cli_task(
    file: Path,
    nodes: List,
    update: bool,
    force: bool,
    save: bool,
    context: bool,
    background: bool,
    pretty: bool,
    batch: bool,
    print_status: bool,
    progress: Progress,
    model: str = "gpt-3.5-turbo-instruct",
) -> None:
    """
    Executes a task asynchronously.

    Args:
      file (Path): The file to process.
      nodes (List): The nodes to process.
      update (bool): Whether to update the task.
      force (bool): Whether to force the task.
      save (bool): Whether to save the task.
      context (bool): Whether to include context.
      background (bool): Whether to run the task in the background.
      pretty (bool): Whether to format the output.
      batch (bool): Whether to run in batch mode.
      print_status (bool): Whether to print the status.
      progress (Progress): The progress object.
      model (str, optional): The model to use for the task. Defaults to "gpt-3.5-turbo-instruct".

    Returns:
      None

    Side Effects:
      Writes to the file if save is True.
      Prints the pass/fail status if print_status is True.
      Pretty prints the result if pretty is True.

    Examples:
      >>> await async_cli_task(file, nodes, update, force, save, context, background, pretty, batch, print_status, progress)
      None
    """
    task_id = progress.add_task(description=f"{file}", total=None)
    failed = False
    skipped = False
    source_code = load_source_code(file=file)
    if pretty:
        source_code = format_source_code(source_code)
    tree = create_tree(source_code)
    max_batch_size = None
    msg = ""
    if batch:
        max_batch_size = 1
    try:
        result = await write_the_docs(
            tree,
            node_names=nodes,
            update=update,
            force=force,
            save=save,
            context=context,
            background=background,
            pretty=pretty,
            max_batch_size=max_batch_size,
            model=model,
        )
    except ValueError as e:
        msg = f" - {e}"
        failed = True
    except InvalidRequestError as e:
        msg = f" - {e}"
        failed = True
    except FileSkippedError as e:
        msg = f" - {e}"
        skipped = True
    
    progress.remove_task(task_id)
    progress.refresh()
    if print_status or save or failed or skipped:
        if skipped:
            icon = "⏭️"
            colour = "yellow"
        elif failed:
            icon = "❌"
            colour = "red" 
        else:
            icon = "✅"
            colour = "green"
        progress.print(
            f"[not underline]{icon} [/not underline][underline]{file}[/underline]{msg}",
            style=f"bold {colour}",
        )
    if failed or skipped:
        return None
    if save:
        with open(file, "w") as f:
            f.writelines(result)
        return None
    if pretty:
        syntax = Syntax(result, "python")
        progress.print(syntax)
    else:
        progress.print(result, highlight=False, markup=False)
