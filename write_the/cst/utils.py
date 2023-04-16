import libcst as cst


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
