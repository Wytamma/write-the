import libcst as cst
from .utils import has_docstring


class FunctionAndClassCollector(cst.CSTVisitor):
    def __init__(self, force):
        """
        Initializes the FunctionAndClassCollector.
        Args:
          force (bool): Whether to force the collection of functions and classes even if they have docstrings.
        """
        self.functions = []
        self.classes = []
        self.force = force
        self.current_class = None

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        """
        Visits a FunctionDef node and adds it to the list of functions if it does not have a docstring or if `force` is `True`.
        Args:
          node (cst.FunctionDef): The FunctionDef node to visit.
        """
        name = (
            f"{self.current_class}.{node.name.value}"
            if self.current_class
            else node.name.value
        )
        if not has_docstring(node) or self.force:
            self.functions.append(name)

    def visit_ClassDef(self, node: cst.ClassDef) -> None:
        """
        Visits a ClassDef node and adds it to the list of classes if it does not have a docstring or if `force` is `True`.
        Args:
          node (cst.ClassDef): The ClassDef node to visit.
        """
        self.current_class = node.name.value
        if not has_docstring(node) or self.force:
            self.classes.append(node.name.value)
        # self.visit_ClassDef(node)  # Call the superclass method to continue the visit

    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        self.current_class = None


def get_node_names(tree, force):
    """
    Gets the names of functions and classes from a CST tree.
    Args:
      tree (cst.CSTNode): The CST tree to traverse.
      force (bool): Whether to force the collection of functions and classes even if they have docstrings.
    Returns:
      list[str]: A list of function and class names.
    """
    collector = FunctionAndClassCollector(force)
    tree.visit(collector)
    return collector.classes + collector.functions
