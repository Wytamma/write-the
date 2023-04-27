import libcst as cst
from black import format_str, FileMode

from write_the.cst import nodes_to_tree
from write_the.cst.docstring_adder import add_docstrings_to_tree
from write_the.cst.docstring_remover import remove_docstrings
from write_the.cst.function_and_class_collector import get_node_names
from write_the.cst.node_extractor import extract_nodes_from_tree
from write_the.commands.docs.utils import extract_block, process_nodes
from write_the.llm import LLM
from .prompts import write_docstings_for_nodes_prompt


async def write_the_docs(
    tree: cst.Module,
    nodes=[],
    force=False,
    save=False,
    context=True,
    pretty=False,
    batch=False,
) -> str:
    """
    Generates docstrings for a given tree of nodes.
    Args:
      tree (cst.Module): The tree of nodes to write docs for.
      nodes (list): The list of nodes to write docs for.
      force (bool): Whether to force writing of docs.
      save (bool): Whether to save the docs.
      context (bool): Whether to include context nodes.
      pretty (bool): Whether to format the code.
      batch (bool): Whether to run in batch mode.
    Returns:
      str: The source code with the generated docstrings.
    Notes:
      If `nodes` is provided, `force` is set to `True` and `context` is set to `False`.
    Examples:
      >>> write_the_docs("example.py")
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
    if nodes:
        extract_specific_nodes = True
        force = True
    else:
        nodes = get_node_names(tree, force)
    if not nodes:
        return tree.code
    tree_without_docstrings = remove_docstrings(tree, nodes)
    code = process_nodes(tree_without_docstrings, nodes, context, extract_specific_nodes)
    llm = LLM(write_docstings_for_nodes_prompt)
    result = await llm.run(code=code, nodes=nodes)
    docstring_dict = extract_block(result, nodes)
    modified_tree = add_docstrings_to_tree(tree, docstring_dict, force=force)
    if not save and extract_specific_nodes:
        extracted_nodes = extract_nodes_from_tree(modified_tree, nodes)
        modified_tree = nodes_to_tree(extracted_nodes)
    if pretty:
        return format_str(modified_tree.code, mode=FileMode())
    return modified_tree.code
