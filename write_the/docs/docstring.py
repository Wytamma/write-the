import ast


def has_docstring(node):
    """
    Checks if a node has a docstring.
    Args:
      node (ast.AST): The node to check.
    Returns:
      bool: True if the node has a docstring, False otherwise.
    """
    if not node.body:
        return False
    first_stmt = node.body[0]
    if not isinstance(first_stmt, ast.Expr):
        return False
    if not isinstance(first_stmt.value, ast.Constant):
        return False
    if first_stmt.value.kind not in (None, "u"):
        return False
    return True


class DocstringAdder(ast.NodeTransformer):
    def __init__(self, docstrings, force):
        """
        Initializes a DocstringAdder object.
        Args:
          docstrings (dict): A dictionary of docstrings to add.
          force (bool): Whether to force adding docstrings.
        Attributes:
          docstrings (dict): A dictionary of docstrings to add.
          current_class (str): The current class name.
          force (bool): Whether to force adding docstrings.
        """
        self.docstrings = docstrings
        self.current_class = None
        self.force = force

    def visit_FunctionDef(self, node):
        """
        Visits a function definition node and adds a docstring if necessary.
        Args:
          node (ast.FunctionDef): The node to visit.
        Returns:
          ast.FunctionDef: The visited node.
        """
        self.add_docstring(node)
        return node

    def visit_ClassDef(self, node):
        """
        Visits a class definition node and adds a docstring if necessary.
        Args:
          node (ast.ClassDef): The node to visit.
        Returns:
          ast.ClassDef: The visited node.
        """
        self.current_class = node.name
        self.add_docstring(node)
        self.generic_visit(node)
        self.current_class = None
        return node

    def add_docstring(self, node):
        """
        Adds a docstring to a node if necessary.
        Args:
          node (ast.AST): The node to add a docstring to.
        """
        key = f"{self.current_class}.{node.name}" if self.current_class else node.name
        docstring = self.docstrings.get(key, None)
        if docstring and (not has_docstring(node) or self.force):
            docstring_node = ast.Expr(value=ast.Constant(value=docstring, kind=None))
            node.body.insert(0, docstring_node)


class FunctionAndClassCollector(ast.NodeVisitor):
    def __init__(self, force):
        """
        Initializes a FunctionAndClassCollector object.
        Args:
          force (bool): Whether to force adding docstrings.
        Attributes:
          functions (list): A list of function names.
          classes (list): A list of class names.
          current_class (str): The current class name.
          force (bool): Whether to force adding docstrings.
        """
        self.functions = []
        self.classes = []
        self.current_class = None
        self.force = force

    def visit_FunctionDef(self, node):
        """
        Visits a function definition node and adds the name to the list of functions if necessary.
        Args:
          node (ast.FunctionDef): The node to visit.
        """
        name = f"{self.current_class}.{node.name}" if self.current_class else node.name
        if not has_docstring(node) or self.force:
            self.functions.append(name)

    def visit_ClassDef(self, node):
        """
        Visits a class definition node and adds the name to the list of classes if necessary.
        Args:
          node (ast.ClassDef): The node to visit.
        """
        self.current_class = node.name
        if not has_docstring(node) or self.force:
            self.classes.append(node.name)
        self.generic_visit(node)
        self.current_class = None


def get_node_names(ast, force):
    """
    Gets the names of nodes that need docstrings.
    Args:
      ast (ast.AST): The AST to search.
      force (bool): Whether to force adding docstrings.
    Returns:
      list: A list of node names.
    """
    collector = FunctionAndClassCollector(force)
    collector.visit(ast)
    return collector.functions + collector.classes


class DocstringRemover(ast.NodeTransformer):
    def __init__(self, nodes):
        """
        Initializes a DocstringRemover object.
        Args:
          nodes (list): A list of node names.
        Attributes:
          nodes (list): A list of node names.
        """
        self.nodes = nodes

    def visit_FunctionDef(self, node):
        """
        Visits a function definition node and removes the docstring if necessary.
        Args:
          node (ast.FunctionDef): The node to visit.
        Returns:
          ast.FunctionDef: The visited node.
        """
        if node.name in self.nodes:
            self.remove_docstring(node)
        return node

    def visit_ClassDef(self, node):
        """
        Visits a class definition node and removes the docstring if necessary.
        Args:
          node (ast.ClassDef): The node to visit.
        Returns:
          ast.ClassDef: The visited node.
        """
        if node.name in self.nodes:
            self.remove_docstring(node)
        self.generic_visit(node)
        return node

    def remove_docstring(self, node):
        """
        Removes a docstring from a node if necessary.
        Args:
          node (ast.AST): The node to remove a docstring from.
        """
        if not node.body:
            return
        first_stmt = node.body[0]
        if isinstance(first_stmt, ast.Expr) and isinstance(
            first_stmt.value, ast.Constant
        ):
            node.body.pop(0)


class NodeExtractor(ast.NodeVisitor):
    def __init__(self, nodes):
        """
        Initializes a NodeExtractor object.
        Args:
          nodes (list): A list of node names.
        Attributes:
          nodes (list): A list of node names.
          extracted_nodes (list): A list of extracted nodes.
        """
        self.nodes = nodes
        self.extracted_nodes = []

    def visit_FunctionDef(self, node):
        """
        Visits a function definition node and adds it to the list of extracted nodes if necessary.
        Args:
          node (ast.FunctionDef): The node to visit.
        """
        if node.name in self.nodes:
            self.extracted_nodes.append(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """
        Visits a class definition node and adds it to the list of extracted nodes if necessary.
        Args:
          node (ast.ClassDef): The node to visit.
        """
        if node.name in self.nodes:
            self.extracted_nodes.append(node)
        self.generic_visit(node)


def extract_nodes_from_tree(tree, nodes):
    """
    Extracts nodes from an AST.
    Args:
      tree (ast.AST): The AST to search.
      nodes (list): A list of node names.
    Returns:
      list: A list of extracted nodes.
    """
    extractor = NodeExtractor(nodes)
    extractor.visit(tree)
    return extractor.extracted_nodes


class NodeRemover(ast.NodeTransformer):
    def __init__(self, nodes):
        """
        Initializes a NodeRemover object.
        Args:
          nodes (list): A list of node names.
        Attributes:
          nodes (list): A list of node names.
        """
        self.nodes = nodes

    def visit_FunctionDef(self, node):
        """
        Visits a function definition node and removes it if necessary.
        Args:
          node (ast.FunctionDef): The node to visit.
        Returns:
          ast.FunctionDef: The visited node, or None if the node was removed.
        """
        if node.name in self.nodes:
            return None
        return node

    def visit_ClassDef(self, node):
        """
        Visits a class definition node and removes it if necessary.
        Args:
          node (ast.ClassDef): The node to visit.
        Returns:
          ast.ClassDef: The visited node, or None if the node was removed.
        """
        if node.name in self.nodes:
            return None
        self.generic_visit(node)
        return node


def remove_nodes_from_tree(tree, nodes):
    """
    Removes nodes from an AST.
    Args:
      tree (ast.AST): The AST to search.
      nodes (list): A list of node names.
    Returns:
      ast.AST: The modified AST.
    """
    remover = NodeRemover(nodes)
    tree = remover.visit(tree)
    return tree


def nodes_to_tree(nodes):
    """
    Converts a list of nodes to an AST.
    Args:
      nodes (list): A list of nodes.
    Returns:
      ast.AST: The generated AST.
    """
    module_node = ast.Module(body=[], type_ignores=[])
    module_node.body.extend(nodes)
    ast.fix_missing_locations(module_node)
    return module_node


def process_tree(tree, nodes, remove_nodes):
    """
    Processes an AST.
    Args:
      tree (ast.AST): The AST to process.
      nodes (list): A list of node names.
      remove_nodes (bool): Whether to remove nodes or extract them.
    Returns:
      ast.AST: The processed AST.
    """
    if remove_nodes:
        return remove_nodes_from_tree(tree, nodes)
    else:
        extracted_nodes = extract_nodes_from_tree(tree, nodes)
        return nodes_to_tree(extracted_nodes)


def remove_docstrings(tree, nodes):
    """
    Removes docstrings from an AST.
    Args:
      tree (ast.AST): The AST to process.
      nodes (list): A list of node names.
    Returns:
      ast.AST: The processed AST.
    """
    remover = DocstringRemover(nodes)
    tree = remover.visit(tree)
    return tree
