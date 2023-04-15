from pathlib import Path
import ast
from black import format_str, FileMode
from .docstring import DocstringAdder, get_node_names, remove_docstrings, process_tree
from .chain import run

def write_the_docs(filename: Path, nodes=[], force=False, inplace=False, context=True) -> str:   
    with open(filename, "r") as file:
        source_code = file.read()
    source_code = format_str(source_code, mode=FileMode())
    tree = ast.parse(source_code)
    extract_specific_nodes = False
    if nodes:
        extract_specific_nodes = True
    else:
        nodes = get_node_names(tree, force)
    
    processed_tree = remove_docstrings(tree, nodes) # giving nodes is equal to force 

    if not context:
        if extract_specific_nodes:
            processed_tree = process_tree(processed_tree, nodes, False)
        else:
            # remove any nodes that aren't in the nodes list
            all_nodes = get_node_names(tree, False)
            nodes_to_remove = [n for n in all_nodes if n not in nodes]
            processed_tree = process_tree(processed_tree, nodes_to_remove, True)
        
    code = ast.unparse(processed_tree)
    result = run(code=code, nodes=nodes)

    docstring_dict = {}
    for line in result.split("\n\n"):
        node_name, docsting = line.split(':', 1)
        docstring_dict[node_name] = docsting + "\n\n"
    
    modified_tree = DocstringAdder(docstring_dict, force).visit(tree)
    if not inplace and extract_specific_nodes:
        modified_tree = process_tree(tree, nodes, False)
    modified_tree = ast.fix_missing_locations(modified_tree)
    modified_code = ast.unparse(modified_tree)
    return format_str(modified_code, mode=FileMode())
