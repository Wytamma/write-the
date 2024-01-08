import libcst as cst
from .utils import has_docstring, remove_docstring
import textwrap
import re


class DocstringAdder(cst.CSTTransformer):
    def __init__(self, docstrings, force, indent="    "):
        self.docstrings = docstrings
        self.force = force
        self.indent = indent
        self.current_class = None

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

    def visit_ClassDef(self, original_node: cst.ClassDef) -> None:
        self.current_class = original_node.name.value

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
        self.current_class = None
        updated_node = self.add_docstring(updated_node)
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
        docstring: str = self.docstrings.get(key, None)
        if docstring and (self.force or not has_docstring(node)):
            if self.force and has_docstring(node):
                # Remove existing docstring
                node = remove_docstring(node)
            escaped_docstring = re.sub(r"(?<!\\)\\n", "\\\\\\\\n", docstring)
            dedented_docstring = textwrap.dedent(escaped_docstring)
            indent = self.indent
            if self.current_class:
                indent = indent * 2
            indented_docstring = textwrap.indent(dedented_docstring, indent)
            new_docstring = cst.parse_statement(f'"""{indented_docstring}{indent}"""')
            body = node.body.with_changes(body=(new_docstring, *node.body.body))
            return node.with_changes(body=body)

        return node


def add_docstrings_to_tree(tree, docstring_dict, force=False):
    return tree.visit(DocstringAdder(docstring_dict, force=force, indent=tree.config_for_parsing.default_indent))
