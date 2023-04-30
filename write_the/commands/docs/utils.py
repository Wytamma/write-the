import libcst as cst
import re

from write_the.cst import nodes_to_tree
from write_the.cst.function_and_class_collector import get_node_names
from write_the.cst.node_extractor import extract_nodes_from_tree
from write_the.cst.node_remover import remove_nodes_from_tree


def pad_with_newline_if_needed(s):
    if not s.startswith("\n"):
        s = "\n" + s
    if not s.endswith("\n"):
        s = s + "\n"
    return s


def extract_block(text, class_function_names):
    results = {}
    for name in class_function_names:
        pattern = rf"({name}:[\s\S]*?)(?=(\n\w|\Z))"
        match = re.search(pattern, text)
        if match:
            block = match.group(1).lstrip(f"{name}:")
            results[name] = pad_with_newline_if_needed(block)
    return results


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
    if not context:
        if extract_specific_nodes:
            extracted_nodes = extract_nodes_from_tree(tree, nodes)
            processed_tree = nodes_to_tree(extracted_nodes)
        else:
            all_nodes = get_node_names(tree, True)
            nodes_to_remove = [n for n in all_nodes if n not in nodes]
            processed_tree = remove_nodes_from_tree(tree, nodes_to_remove)
        code = processed_tree.code
    else:
        code = tree.code

    return code
