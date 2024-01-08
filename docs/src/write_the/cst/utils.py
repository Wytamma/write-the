import libcst as cst
from typing import Optional


def has_docstring(node: cst.CSTNode) -> bool:
    """
    Checks if a CSTNode has a docstring.
    Args:
      node (cst.CSTNode): The node to check.
    Returns:
      bool: Whether or not the node has a docstring.
    Notes:
      Only checks for docstrings on FunctionDef and ClassDef nodes.
    """
    if isinstance(node, cst.FunctionDef) or isinstance(node, cst.ClassDef):
        body = node.body.body
        if body and isinstance(body[0], cst.SimpleStatementLine):
            stmt = body[0].body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                return True
    return False


def remove_docstring(node):
    """
    Removes the docstring from a node.
    Args:
      node (cst.CSTNode): The node to remove the docstring from.
    Returns:
      cst.CSTNode: The node with the docstring removed.
    """
    if not node.body.body:
        return node
    first_stmt = node.body.body[0]
    if isinstance(first_stmt, cst.SimpleStatementLine):
        stmt = first_stmt.body[0]
        if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
            new_body = node.body.with_changes(body=node.body.body[1:])
            return node.with_changes(body=new_body)
    return node


def get_docstring(node: cst.CSTNode) -> Optional[str]:
    """
    Retrieves the docstring of a CSTNode if it has one.
    Args:
        node (cst.CSTNode): The node to check.
    Returns:
        Optional[str]: The docstring of the node if it exists, None otherwise.
    Notes:
        Only retrieves docstrings for FunctionDef and ClassDef nodes.
    """
    if has_docstring(node):
        body = node.body.body
        stmt = body[0].body[0]
        return stmt.value.value
    return None


def nodes_to_tree(nodes):
    """
    Converts a list of CSTNodes into a CSTModule.
    Args:
      nodes (list[cst.CSTNode]): The list of nodes to convert.
    Returns:
      cst.Module: The CSTModule containing the given nodes.
    """
    module = cst.Module(body=nodes)
    return module


def get_code_from_node(node: cst.CSTNode):
    return cst.Module(body=[node]).code
