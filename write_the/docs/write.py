import libcst as cst
from black import format_str, FileMode

from write_the.cst import nodes_to_tree
from write_the.cst.docstring_adder import DocstringAdder
from write_the.cst.docstring_remover import remove_docstrings
from write_the.cst.function_and_class_collector import get_node_names
from write_the.cst.node_extractor import extract_nodes_from_tree
from write_the.cst.node_remover import remove_nodes_from_tree
from write_the.docs.chain import run


def process_nodes(tree: cst.Module, nodes, context, extract_specific_nodes) -> str:
    """
    Processes a tree of nodes.
    Args:
      tree (cst.Module): The tree of nodes to process.
      nodes (list): The list of nodes to process.
      context (bool): Whether to include context nodes.
      extract_specific_nodes (bool): Whether to extract specific nodes.
    Returns:
      str: The processed tree as a string.
    Examples:
      >>> process_nodes(tree, nodes, context, extract_specific_nodes)
      "Processed tree as a string"
    """
    tree_without_docstrings = remove_docstrings(tree, nodes)
    if not context:
        if extract_specific_nodes:
            extracted_nodes = extract_nodes_from_tree(tree_without_docstrings, nodes)
            processed_tree = nodes_to_tree(extracted_nodes)
        else:
            all_nodes = get_node_names(tree, False)
            nodes_to_remove = [n for n in all_nodes if n not in nodes]
            processed_tree = remove_nodes_from_tree(
                tree_without_docstrings, nodes_to_remove
            )
        code = processed_tree.code
    else:
        code = tree_without_docstrings.code

    return code


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

    code = process_nodes(tree, nodes, context, extract_specific_nodes)
    result = await run(code=code, nodes=nodes)
    docstring_dict = {}
    for line in result.split("\n\n"):
        line = line.strip()
        if not line:
            continue
        (node_name, docsting) = line.split(":", 1)
        docstring_dict[node_name] = docsting + "\n"
    modified_tree = tree.visit(DocstringAdder(docstring_dict, force))
    if not save and extract_specific_nodes:
        extracted_nodes = extract_nodes_from_tree(modified_tree, nodes)
        modified_tree = nodes_to_tree(extracted_nodes)
    if pretty:
        return format_str(modified_tree.code, mode=FileMode())
    return modified_tree.code
