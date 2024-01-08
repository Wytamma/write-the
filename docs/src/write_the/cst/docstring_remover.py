import libcst as cst
from .utils import remove_docstring


class DocstringRemover(cst.CSTTransformer):
    def __init__(self, nodes):
        """
        Initializes the DocstringRemover object.
        Args:
          nodes (list): A list of nodes to remove docstrings from.
        """
        self.nodes = nodes
        self.current_class = None

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
        name = (
            f"{self.current_class}.{original_node.name.value}"
            if self.current_class
            else original_node.name.value
        )
        if name in self.nodes:
            return remove_docstring(updated_node)
        return updated_node

    def visit_ClassDef(self, original_node: cst.ClassDef) -> None:
        self.current_class = original_node.name.value

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
        self.current_class = None
        if original_node.name.value in self.nodes:
            return remove_docstring(updated_node)
        return updated_node


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
