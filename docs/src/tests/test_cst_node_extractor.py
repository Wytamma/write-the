import pytest
import libcst as cst
from write_the.cst.node_extractor import NodeExtractor, extract_nodes_from_tree


@pytest.fixture
def tree():
    return cst.parse_module(
        """
def foo():
    pass

class Bar:
    pass
"""
    )


@pytest.fixture
def nodes():
    return ["foo", "Bar"]


def test_extract_nodes_from_tree(tree, nodes):
    extracted_nodes = extract_nodes_from_tree(tree, nodes)
    assert len(extracted_nodes) == 2
    assert isinstance(extracted_nodes[0], cst.FunctionDef)
    assert isinstance(extracted_nodes[1], cst.ClassDef)


def test_extract_nodes_from_tree_empty_nodes(tree):
    extracted_nodes = extract_nodes_from_tree(tree, [])
    assert len(extracted_nodes) == 0


def test_visit_FunctionDef(tree, nodes):
    extractor = NodeExtractor(nodes)
    tree.visit(extractor)
    assert len(extractor.extracted_nodes) == 2
    assert isinstance(extractor.extracted_nodes[0], cst.FunctionDef)


def test_visit_ClassDef(tree, nodes):
    extractor = NodeExtractor(nodes)
    tree.visit(extractor)
    assert len(extractor.extracted_nodes) == 2
    assert isinstance(extractor.extracted_nodes[1], cst.ClassDef)


def test_visit_FunctionDef_invalid_node(tree):
    extractor = NodeExtractor(["foo"])
    tree.visit(extractor)
    assert len(extractor.extracted_nodes) == 1


def test_visit_ClassDef_invalid_node(tree):
    extractor = NodeExtractor(["Bar"])
    tree.visit(extractor)
    assert len(extractor.extracted_nodes) == 1
