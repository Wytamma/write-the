import libcst as cst


class DocstringRemover(cst.CSTTransformer):
    def __init__(self, nodes):
        """
        Initializes the DocstringRemover object.
        Args:
          nodes (list): A list of nodes to remove docstrings from.
        """
        self.nodes = nodes

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        """
        Removes the docstring from a FunctionDef node if it is in the list of nodes.
        Args:
          original_node (cst.FunctionDef): The original FunctionDef node.
          updated_node (cst.FunctionDef): The updated FunctionDef node.
        Returns:
          cst.FunctionDef: The updated FunctionDef node with the docstring removed if it is in the list of nodes.
        """
        if original_node.name.value in self.nodes:
            return self.remove_docstring(updated_node)
        return updated_node

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        """
        Removes the docstring from a ClassDef node if it is in the list of nodes.
        Args:
          original_node (cst.ClassDef): The original ClassDef node.
          updated_node (cst.ClassDef): The updated ClassDef node.
        Returns:
          cst.ClassDef: The updated ClassDef node with the docstring removed if it is in the list of nodes.
        """
        if original_node.name.value in self.nodes:
            return self.remove_docstring(updated_node)
        return updated_node

    def remove_docstring(self, node):
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


def remove_docstrings(tree, nodes):
    """
    Removes the docstrings from a tree of nodes.
    Args:
      tree (cst.CSTNode): The tree of nodes to remove the docstrings from.
      nodes (list): A list of nodes to remove docstrings from.
    Returns:
      cst.CSTNode: The tree of nodes with the docstrings removed.
    """
    remover = DocstringRemover(nodes)
    tree = tree.visit(remover)
    return tree
