from pathlib import Path
import ast
from black import format_str, FileMode
from .docstring import DocstringAdder, get_node_names, remove_docstrings, process_tree
from .chain import run


def write_the_docs(
    filename: Path, nodes=[], force=False, inplace=False, context=True
) -> str:
    '''
    Writes docstrings to a given file.
    Args:
      filename (Path): The path to the file to write the docstrings to.
      nodes (list): A list of nodes to write docstrings for.
      force (bool): If True, overwrite existing docstrings.
      inplace (bool): If True, write docstrings to the same file.
      context (bool): If True, write docstrings for all nodes in the file.
    Returns:
      str: The modified source code with the docstrings added.
    Notes:
      If `nodes` is empty, docstrings will be written for all nodes in the file.
      If `context` is False, docstrings will only be written for the nodes in `nodes`.
    Examples:
      >>> write_the_docs('example.py', nodes=['add', 'subtract'], force=True, inplace=True, context=False)
      'def add(a, b):
          """Adds two numbers.
          Args:
              a (int): The first number to add.
              b (int): The second number to add.
          Returns:
              int: The sum of `a` and `b`.
          """
          return a + b
      def subtract(a, b):
          """Subtracts two numbers.
          Args:
              a (int): The first number to subtract.
              b (int): The second number to subtract.
          Returns:
              int: The difference of `a` and `b`.
          """
          return a - b'
    '''
    with open(filename, "r") as file:
        source_code = file.read()
    source_code = format_str(source_code, mode=FileMode())
    tree = ast.parse(source_code)
    extract_specific_nodes = False
    if nodes:
        extract_specific_nodes = True
    else:
        nodes = get_node_names(tree, force)
    processed_tree = remove_docstrings(tree, nodes)
    if not context:
        if extract_specific_nodes:
            processed_tree = process_tree(processed_tree, nodes, False)
        else:
            all_nodes = get_node_names(tree, False)
            nodes_to_remove = [n for n in all_nodes if n not in nodes]
            processed_tree = process_tree(processed_tree, nodes_to_remove, True)
    code = ast.unparse(processed_tree)
    result = run(code=code, nodes=nodes)
    docstring_dict = {}
    for line in result.split("\n\n"):
        (node_name, docsting) = line.split(":", 1)
        docstring_dict[node_name] = docsting + "\n\n"
    modified_tree = DocstringAdder(docstring_dict, force).visit(tree)
    if not inplace and extract_specific_nodes:
        modified_tree = process_tree(tree, nodes, False)
    modified_tree = ast.fix_missing_locations(modified_tree)
    modified_code = ast.unparse(modified_tree)
    return format_str(modified_code, mode=FileMode())
