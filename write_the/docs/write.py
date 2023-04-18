from pathlib import Path
import libcst as cst
from black import format_str, FileMode

from write_the.cst import nodes_to_tree
from write_the.cst.docstring_adder import DocstringAdder
from write_the.cst.docstring_remover import remove_docstrings
from write_the.cst.function_and_class_collector import get_node_names
from write_the.cst.node_extractor import extract_nodes_from_tree
from write_the.cst.node_remover import remove_nodes_from_tree
from write_the.docs.chain import run


def write_the_docs(
    filename: Path, nodes=[], force=False, save=False, context=True, pretty=False
) -> str:
    """
    Generates docstrings for a given file.
    Args:
      filename (Path): The path to the file to generate docstrings for.
      nodes (list): A list of nodes to generate docstrings for.
      force (bool): Whether to overwrite existing docstrings.
      save (bool): Whether to generate docstrings in the same file.
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
    if pretty:
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
    result = run(code=code, nodes=nodes)
    docstring_dict = {}
    for line in result.split("\n\n"):
        line = line.strip()
        if not line:
            continue
        (node_name, docsting) = line.split(":", 1)
        docstring_dict[node_name] = docsting + "\n"
    modified_tree = tree_without_docstrings.visit(DocstringAdder(docstring_dict, force))
    if not save and extract_specific_nodes:
        extracted_nodes = extract_nodes_from_tree(modified_tree, nodes)
        modified_tree = nodes_to_tree(extracted_nodes)
    if pretty:
        
        return format_str(modified_tree.code, mode=FileMode())
    return modified_tree.code
