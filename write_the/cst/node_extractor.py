from typing import Optional
import libcst as cst


class NodeExtractor(cst.CSTVisitor):
    def __init__(self, nodes):
        self.nodes = nodes
        self.extracted_nodes = []
        self.current_class = None

    def visit_FunctionDef(self, node: cst.FunctionDef):
        """
        Visits a FunctionDef node and adds it to the extracted_nodes list if its name is in the nodes list.

        Args:
          node (cst.FunctionDef): The FunctionDef node to visit.

        Side Effects:
          Modifies the extracted_nodes list of the NodeExtractor instance, adding the node if its name is in the nodes list.
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
        Visits a ClassDef node and sets the current_class attribute. If the class name is in the nodes list, it also adds the node to the extracted_nodes list.

        Args:
          node (cst.ClassDef): The ClassDef node to visit.

        Side Effects:
          Modifies the current_class attribute of the NodeExtractor instance, setting it to the name of the visited node. If the class name is in the nodes list, it also modifies the extracted_nodes list, adding the node.
        """
        self.current_class = node.name.value
        if node.name.value in self.nodes:
            self.extracted_nodes.append(node)

    def leave_ClassDef(self, node: cst.ClassDef) -> None:
        self.current_class = None


def extract_nodes_from_tree(tree, nodes):
    """
    Extracts specified nodes from a CST tree.

    Args:
      tree (cst.CSTNode): The CST tree to extract nodes from.
      nodes (list of str): A list of node names to extract.

    Returns:
      list of cst.CSTNode: A list of extracted nodes.

    Examples:
      >>> extract_nodes_from_tree(tree, ['FunctionDef', 'ClassDef'])
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
