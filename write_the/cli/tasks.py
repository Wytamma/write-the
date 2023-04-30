from write_the.commands import write_the_docs
from write_the.utils import create_tree, format_source_code, load_source_code
from rich.syntax import Syntax
from rich.progress import Progress
from typing import List
from pathlib import Path
from openai.error import InvalidRequestError


async def async_cli_task(
    file: Path,
    nodes: List,
    force: bool,
    save: bool,
    context: bool,
    background: bool,
    pretty: bool,
    batch: bool,
    print_status: bool,
    progress: Progress,
) -> None:
    """
    Executes a task asynchronously.
    Args:
      file (Path): The file to process.
      nodes (List): The nodes to process.
      force (bool): Whether to force the task.
      save (bool): Whether to save the task.
      context (bool): Whether to include context.
      pretty (bool): Whether to format the output.
      batch (bool): Whether to run in batch mode.
      print_status (bool): Whether to print the status.
      progress (Progress): The progress object.
    Returns:
      None
    Side Effects:
      Writes to the file if save is True.
      Prints the pass/fail status if print_status is True.
      Pretty prints the result if pretty is True.
    Examples:
      >>> await async_cli_task(file, nodes, force, save, context, pretty, batch, print_status, progress)
      None
    """
    task_id = progress.add_task(description=f"{file}", total=None)
    failed = False
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
            force=force,
            save=save,
            context=context,
            background=background,
            pretty=pretty,
            max_batch_size=max_batch_size,
        )
    except ValueError as e:
        msg = f" - {e}"
        failed = True
    except InvalidRequestError as e:
        msg = f" - {e}"
        failed = True
    progress.remove_task(task_id)
    progress.refresh()
    if print_status or save or failed:
        icon = "❌" if failed else "✅"
        colour = "red" if failed else "green"
        progress.print(
            f"[not underline]{icon} [/not underline]{file}{msg}",
            style=f"bold {colour} underline",
        )
    if failed:
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
