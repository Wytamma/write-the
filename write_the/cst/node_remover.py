import libcst as cst


class NodeRemover(cst.CSTTransformer):
    def __init__(self, nodes):
        """
        Initializes a NodeRemover instance.
        Args:
          nodes (list): A list of nodes to remove.
        """
        self.nodes = nodes

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.RemovalSentinel:
        """
        Removes a FunctionDef node from the tree if it is in the list of nodes.
        Args:
          original_node (cst.FunctionDef): The original FunctionDef node.
          updated_node (cst.FunctionDef): The updated FunctionDef node.
        Returns:
          cst.RemovalSentinel: A sentinel indicating whether the node should be removed.
        """
        if original_node.name.value in self.nodes:
            return cst.RemoveFromParent()
        return updated_node

    def leave_ClassDef(
        self, original_node: cst.ClassDef, updated_node: cst.ClassDef
    ) -> cst.RemovalSentinel:
        """
        Removes a ClassDef node from the tree if it is in the list of nodes.
        Args:
          original_node (cst.ClassDef): The original ClassDef node.
          updated_node (cst.ClassDef): The updated ClassDef node.
        Returns:
          cst.RemovalSentinel: A sentinel indicating whether the node should be removed.
        """
        if original_node.name.value in self.nodes:
            return cst.RemoveFromParent()
        return updated_node


def remove_nodes_from_tree(tree, nodes):
    """
    Removes nodes from a CST tree.
    Args:
      tree (cst.CSTNode): The CST tree to remove nodes from.
      nodes (list): A list of nodes to remove.
    Returns:
      cst.CSTNode: The updated CST tree.
    """
    remover = NodeRemover(nodes)
    tree = tree.visit(remover)
    return tree
