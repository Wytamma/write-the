import ast


def has_docstring(node):
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
        self.docstrings = docstrings
        self.current_class = None
        self.force = force

    def visit_FunctionDef(self, node):
        self.add_docstring(node)
        return node

    def visit_ClassDef(self, node):
        self.current_class = node.name
        self.add_docstring(node)
        self.generic_visit(node)
        self.current_class = None
        return node

    def add_docstring(self, node):
        key = f"{self.current_class}.{node.name}" if self.current_class else node.name
        docstring = self.docstrings.get(key, None)
        if docstring and (not has_docstring(node) or self.force):
            docstring_node = ast.Expr(value=ast.Constant(value=docstring, kind=None))
            node.body.insert(0, docstring_node)


class FunctionAndClassCollector(ast.NodeVisitor):
    def __init__(self, force):
        self.functions = []
        self.classes = []
        self.current_class = None
        self.force = force

    def visit_FunctionDef(self, node):
        name = f"{self.current_class}.{node.name}" if self.current_class else node.name
        if not has_docstring(node) or self.force:
            self.functions.append(name)

    def visit_ClassDef(self, node):
        self.current_class = node.name
        if not has_docstring(node) or self.force:
            self.classes.append(node.name)
        self.generic_visit(node)
        self.current_class = None


def get_node_names(ast, force):
    collector = FunctionAndClassCollector(force)
    collector.visit(ast)
    return collector.functions + collector.classes


class DocstringRemover(ast.NodeTransformer):
    def __init__(self, nodes):
        self.nodes = nodes

    def visit_FunctionDef(self, node):
        if node.name in self.nodes:
            self.remove_docstring(node)
        return node

    def visit_ClassDef(self, node):
        if node.name in self.nodes:
            self.remove_docstring(node)
        self.generic_visit(node)
        return node

    def remove_docstring(self, node):
        if not node.body:
            return
        first_stmt = node.body[0]
        if isinstance(first_stmt, ast.Expr) and isinstance(
            first_stmt.value, ast.Constant
        ):
            node.body.pop(0)

class NodeExtractor(ast.NodeVisitor):
    def __init__(self, nodes):
        self.nodes = nodes
        self.extracted_nodes = []

    def visit_FunctionDef(self, node):
        if node.name in self.nodes:
            self.extracted_nodes.append(node)
        self.generic_visit(node)  # Visit child nodes (e.g., nested functions)

    def visit_ClassDef(self, node):
        if node.name in self.nodes:
            self.extracted_nodes.append(node)
        self.generic_visit(node)  # Visit child nodes (e.g., methods)

def extract_nodes_from_tree(tree, nodes):
    extractor = NodeExtractor(nodes)
    extractor.visit(tree)
    return extractor.extracted_nodes

class NodeRemover(ast.NodeTransformer):
    def __init__(self, nodes):
        self.nodes = nodes

    def visit_FunctionDef(self, node):
        if node.name in self.nodes:
            return None  # Remove the node
        return node  # Keep the node

    def visit_ClassDef(self, node):
        if node.name in self.nodes:
            return None  # Remove the node
        self.generic_visit(node)  # Visit child nodes (e.g., methods)
        return node

def remove_nodes_from_tree(tree, nodes):
    remover = NodeRemover(nodes)
    tree = remover.visit(tree)
    return tree

def nodes_to_tree(nodes):
    module_node = ast.Module(body=[], type_ignores=[])
    module_node.body.extend(nodes)
    ast.fix_missing_locations(module_node)
    return module_node

def process_tree(tree, nodes, remove_nodes):
    if remove_nodes:
        return remove_nodes_from_tree(tree, nodes)
    else:
        extracted_nodes = extract_nodes_from_tree(tree, nodes)
        return nodes_to_tree(extracted_nodes)


def remove_docstrings(tree, nodes):
    remover = DocstringRemover(nodes)
    tree = remover.visit(tree)
    return tree
