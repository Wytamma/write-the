import asyncio
import libcst as cst
from black import format_str, FileMode

from write_the.cst import nodes_to_tree
from write_the.cst.docstring_adder import add_docstrings_to_tree
from write_the.cst.function_and_class_collector import get_node_names
from write_the.cst.node_extractor import extract_nodes_from_tree
from write_the.cst.node_batcher import create_batches
from write_the.commands.docs.utils import extract_block
from write_the.errors import FileSkippedError
from write_the.llm import LLM
from .prompts import write_docstrings_for_nodes_prompt, update_docstrings_for_nodes_prompt


async def write_the_docs(
    tree: cst.Module,
    node_names=[],
    update=False,
    force=False,
    save=False,
    context=False,
    background=True,
    pretty=False,
    max_batch_size=False,
    model="gpt-3.5-turbo-instruct",
) -> str:
    """
    Generates docstrings for a given tree of nodes using a specified model.

    Args:
      tree (cst.Module): The tree of nodes to write docs for.
      node_names (list, optional): The list of nodes names to write docs for. Defaults to an empty list.
      update (bool, optional): Whether to update existing docstrings. Defaults to False.
      force (bool, optional): Whether to force writing of docs. Defaults to False.
      save (bool, optional): Whether to save the docs. Defaults to False.
      context (bool, optional): Whether to include context nodes. Defaults to False.
      background (bool, optional): Whether to run the process in the background. Defaults to True.
      pretty (bool, optional): Whether to format the code. Defaults to False.
      max_batch_size (bool, optional): Max number of nodes in each batch. Defaults to False.
      model (str, optional): The model to use for the generation. Defaults to "gpt-3.5-turbo-instruct".

    Returns:
      str: The source code with the generated docstrings.

    Raises:
      FileSkippedError: If no nodes are found.

    Notes:
      If `node_names` is provided, `force` is set to `True` and `context` is set to `False`.

    Examples:
      >>> write_the_docs(tree, model="gpt-3.5-turbo-instruct")
      "def add(a, b):
          \"\"\"Sums 2 numbers.
          Args:
              a (int): The first number to add.
              b (int): The second number to add.
          Returns:
              int: The sum of `a` and `b`.
          \"\"\"
          return a + b"
    """
    extract_specific_nodes = False
    if node_names:
        extract_specific_nodes = True
        force = True
    else:
        node_names = get_node_names(tree, force=force, update=update)
    if not node_names:
        raise FileSkippedError("No nodes found, skipping file...")
    if update:
        remove_docstrings = False
        llm = LLM(update_docstrings_for_nodes_prompt, model_name=model)
    else:
        remove_docstrings = True
        llm = LLM(write_docstrings_for_nodes_prompt, model_name=model)

    batches = create_batches(
        tree=tree,
        node_names=node_names,
        max_tokens=llm.max_tokens,
        prompt_size=llm.prompt_size,
        response_size_per_node=250,  # a guess... TODO: smarter
        max_batch_size=max_batch_size,
        send_background_context=background,
        send_node_context=context,
        remove_docstrings=remove_docstrings
    )
    promises = []
    node_names_list = []
    for batch in batches:
        node_names = batch.node_names
        code = batch.code
        promises.append((llm.run(code=code, nodes=node_names)))
        node_names_list.append(node_names)
    # Can i yield here so batches can be logged?
    results = await asyncio.gather(*promises)
    docstring_dict = {}
    for node_names, result in zip(node_names_list, results):
        docstring_dict.update(extract_block(result, node_names))
    modified_tree = add_docstrings_to_tree(tree, docstring_dict, force=force or update)
    if not save and extract_specific_nodes:
        extracted_nodes = extract_nodes_from_tree(modified_tree, node_names)
        modified_tree = nodes_to_tree(extracted_nodes)
    if pretty:
        return format_str(modified_tree.code, mode=FileMode())
    return modified_tree.code
