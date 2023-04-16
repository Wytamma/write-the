from pathlib import Path
import libcst as cst
from black import format_str, FileMode
from .docstring import get_node_names, remove_docstrings, process_tree
from write_the.cst import DocstringAdder
from .chain import run

def write_the_docs(filename: Path, nodes=[], force=False, inplace=False, context=True) -> str:
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

    remove_docstrings_tree = remove_docstrings(tree, nodes)
    if not context:
        if extract_specific_nodes:
            processed_tree = process_tree(remove_docstrings_tree, nodes, False)
        else:
            all_nodes = get_node_names(tree, False)
            nodes_to_remove = [n for n in all_nodes if n not in nodes]
            processed_tree = process_tree(remove_docstrings_tree, nodes_to_remove, True)
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
        modified_tree = process_tree(modified_tree, nodes, False)

    modified_code = modified_tree.code
    return format_str(modified_code, mode=FileMode())

