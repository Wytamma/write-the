from typing import Optional
import libcst as cst


class NodeExtractor(cst.CSTVisitor):
    def __init__(self, nodes):
        self.nodes = nodes
        self.extracted_nodes = []
        self.current_class = None

    def visit_FunctionDef(self, node: cst.FunctionDef):
        """
        Visits a FunctionDef node and adds it to the extracted_nodes list if it is in the nodes list.
        Args:
          node (cst.FunctionDef): The FunctionDef node to visit.
        Side Effects:
          Adds the node to the extracted_nodes list if it is in the nodes list.
        """
        name = (
            f"{self.current_class}.{node.name.value}"
            if self.current_class
            else node.name.value
        )
        if name in self.nodes:
            self.extracted_nodes.append(node)

    def visit_ClassDef(self, node: cst.ClassDef):
        """
        Visits a ClassDef node and adds it to the extracted_nodes list if it is in the nodes list.
        Args:
          node (cst.ClassDef): The ClassDef node to visit.
        Side Effects:
          Adds the node to the extracted_nodes list if it is in the nodes list.
        """
        self.current_class = node.name.value
        if node.name.value in self.nodes:
            self.extracted_nodes.append(node)

    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        self.current_class = None


def extract_nodes_from_tree(tree, nodes):
    """
    Extracts nodes from a CST tree.
    Args:
      tree (cst.CSTNode): The CST tree to extract nodes from.
      nodes (list): A list of nodes to extract.
    Returns:
      list: A list of extracted nodes.
    Examples:
      >>> extract_nodes_from_tree(tree, nodes)
      [cst.FunctionDef, cst.ClassDef]
    """
    extractor = NodeExtractor(nodes)
    tree.visit(extractor)
    return extractor.extracted_nodes


def extract_node_from_tree(tree, node) -> Optional[cst.CSTNode]:
    extractor = NodeExtractor([node])
    tree.visit(extractor)
    if not extractor.extracted_nodes:
        raise ValueError(f"Could not find node: {node}!")
    return extractor.extracted_nodes[0]
