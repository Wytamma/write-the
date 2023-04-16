from pathlib import Path
import libcst as cst
from black import format_str, FileMode

from write_the.cst import nodes_to_tree
from write_the.cst.docstring_adder import DocstringAdder
from write_the.cst.docstring_remover import remove_docstrings
from write_the.cst.function_and_class_collector import get_node_names
from write_the.cst.node_extractor import extract_nodes_from_tree
from write_the.cst.node_remover import remove_nodes_from_tree
from .chain import run


def write_the_docs(
    filename: Path, nodes=[], force=False, inplace=False, context=True
) -> str:
    """
    Generates docstrings for a given file.
    Args:
      filename (Path): The path to the file to generate docstrings for.
      nodes (list): A list of nodes to generate docstrings for.
      force (bool): Whether to overwrite existing docstrings.
      inplace (bool): Whether to generate docstrings in the same file.
      context (bool): Whether to send context with the code (can improve docstings).
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
    with open(filename, "r") as file:
        source_code = file.read()

    source_code = format_str(source_code, mode=FileMode())
    tree = cst.parse_module(source_code)
    extract_specific_nodes = False

    if nodes:
        extract_specific_nodes = True
        force = True
    else:
        nodes = get_node_names(tree, force)
    if not nodes:
        return source_code
    remove_docstrings_tree = remove_docstrings(tree, nodes)
    if not context:
        if extract_specific_nodes:
            extracted_nodes = extract_nodes_from_tree(remove_docstrings_tree, nodes)
            processed_tree = nodes_to_tree(extracted_nodes)
        else:
            all_nodes = get_node_names(tree, False)
            nodes_to_remove = [n for n in all_nodes if n not in nodes]
            processed_tree = remove_nodes_from_tree(
                remove_docstrings_tree, nodes_to_remove
            )
        code = processed_tree.code
    else:
        code = remove_docstrings_tree.code
    result = run(code=code, nodes=nodes)
    docstring_dict = {}
    for line in result.split("\n\n"):
        (node_name, docsting) = line.split(":", 1)
        docstring_dict[node_name] = docsting + "\n\n"
    modified_tree = remove_docstrings_tree.visit(DocstringAdder(docstring_dict, force))

    if not inplace and extract_specific_nodes:
        extracted_nodes = extract_nodes_from_tree(tree, nodes)
        modified_tree = nodes_to_tree(extracted_nodes)

    modified_code = modified_tree.code
    return format_str(modified_code, mode=FileMode())
