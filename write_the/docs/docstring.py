import libcst as cst


class DocstringAdder(cst.CSTTransformer):
    def __init__(self, docstrings, force):
        self.docstrings = docstrings
        self.current_class = None
        self.force = force

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        return self.add_docstring(updated_node)

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        self.current_class = original_node.name.value
        updated_node = self.add_docstring(updated_node)
        self.current_class = None
        return updated_node

    def add_docstring(self, node):
        key = f"{self.current_class}.{node.name.value}" if self.current_class else node.name.value
        docstring = self.docstrings.get(key, None)

        if docstring and (not has_docstring(node) or self.force):
            new_docstring = cst.parse_statement(f'"""{docstring}"""')
            body = node.body.with_changes(body=[new_docstring] + list(node.body.body))
            return node.with_changes(body=body)
        return node


class FunctionAndClassCollector(cst.CSTVisitor):
    def __init__(self, force):
        self.functions = []
        self.classes = []
        self.current_class = None
        self.force = force

    def visit_FunctionDef(self, node: cst.FunctionDef):
        name = f"{self.current_class}.{node.name.value}" if self.current_class else node.name.value
        if not has_docstring(node) or self.force:
            self.functions.append(name)

    def visit_ClassDef(self, node: cst.ClassDef):
        self.current_class = node.name.value
        if not has_docstring(node) or self.force:
            self.classes.append(node.name.value)
        self.visit(node.body)
        self.current_class = None

def get_node_names(tree, force):
    collector = FunctionAndClassCollector(force)
    tree.visit(collector)
    return collector.functions + collector.classes

class DocstringRemover(cst.CSTTransformer):
    def __init__(self, nodes):
        self.nodes = nodes

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.FunctionDef:
        if original_node.name.value in self.nodes:
            return self.remove_docstring(updated_node)
        return updated_node

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.ClassDef:
        if original_node.name.value in self.nodes:
            return self.remove_docstring(updated_node)
        return updated_node

    def remove_docstring(self, node):
        if not node.body.body:
            return node
        first_stmt = node.body.body[0]
        if isinstance(first_stmt, cst.SimpleStatementLine):
            stmt = first_stmt.body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                new_body = node.body.with_changes(body=node.body.body[1:])
                return node.with_changes(body=new_body)
        return node

class NodeExtractor(cst.CSTVisitor):
    def __init__(self, nodes):
        self.nodes = nodes
        self.extracted_nodes = []

    def visit_FunctionDef(self, node: cst.FunctionDef):
        if node.name.value in self.nodes:
            self.extracted_nodes.append(node)

    def visit_ClassDef(self, node: cst.ClassDef):
        if node.name.value in self.nodes:
            self.extracted_nodes.append(node)

def extract_nodes_from_tree(tree, nodes):
    extractor = NodeExtractor(nodes)
    tree.visit(extractor)
    return extractor.extracted_nodes

class NodeRemover(cst.CSTTransformer):
    def __init__(self, nodes):
        self.nodes = nodes

    def leave_FunctionDef(self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef) -> cst.RemovalSentinel:
        if original_node.name.value in self.nodes:
            return cst.RemoveFromParent()
        return updated_node

    def leave_ClassDef(self, original_node: cst.ClassDef, updated_node: cst.ClassDef) -> cst.RemovalSentinel:
        if original_node.name.value in self.nodes:
            return cst.RemoveFromParent()
        return updated_node


def has_docstring(node: cst.CSTNode) -> bool:
    if isinstance(node, cst.FunctionDef) or isinstance(node, cst.ClassDef):
        body = node.body.body
        if body and isinstance(body[0], cst.SimpleStatementLine):
            stmt = body[0].body[0]
            if isinstance(stmt, cst.Expr) and isinstance(stmt.value, cst.SimpleString):
                return True
    return False

def remove_nodes_from_tree(tree, nodes):
    remover = NodeRemover(nodes)
    tree = tree.visit(remover)
    return tree


def nodes_to_tree(nodes):
    module = cst.Module(body=nodes)
    return module


def process_tree(tree, nodes, remove_nodes):
    if remove_nodes:
        return remove_nodes_from_tree(tree, nodes)
    else:
        extracted_nodes = extract_nodes_from_tree(tree, nodes)
        return nodes_to_tree(extracted_nodes)


def remove_docstrings(tree, nodes):
    remover = DocstringRemover(nodes)
    tree = tree.visit(remover)
    return tree
