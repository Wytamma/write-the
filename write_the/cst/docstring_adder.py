import libcst as cst
from .utils import has_docstring


class DocstringAdder(cst.CSTTransformer):
    def __init__(self, docstrings, force):
        self.docstrings = docstrings
        self.current_class = None
        self.force = force

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        """
        Adds a docstring to a function definition.
        Args:
          original_node (cst.FunctionDef): The original CST node.
          updated_node (cst.FunctionDef): The updated CST node.
        Returns:
          cst.FunctionDef: The updated CST node with a docstring added.
        """
        return self.add_docstring(updated_node)

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.ClassDef:
        """
        Adds a docstring to a class definition.
        Args:
          original_node (cst.ClassDef): The original CST node.
          updated_node (cst.ClassDef): The updated CST node.
        Returns:
          cst.ClassDef: The updated CST node with a docstring added.
        """
        self.current_class = original_node.name.value
        updated_node = self.add_docstring(updated_node)
        self.current_class = None
        return updated_node

    def add_docstring(self, node):
        """
        Adds a docstring to a CST node.
        Args:
          node (cst.CSTNode): The CST node to add a docstring to.
        Returns:
          cst.CSTNode: The updated CST node with a docstring added.
        """
        key = (
            f"{self.current_class}.{node.name.value}"
            if self.current_class
            else node.name.value
        )
        docstring = self.docstrings.get(key, None)

        if docstring and (not has_docstring(node) or self.force):
            new_docstring = cst.parse_statement(f'"""{docstring}"""')
            body = node.body.with_changes(body=[new_docstring] + list(node.body.body))
            return node.with_changes(body=body)
        return node
