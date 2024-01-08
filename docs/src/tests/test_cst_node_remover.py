import pytest
import libcst as cst
from write_the.cst.node_remover import NodeRemover, remove_nodes_from_tree


@pytest.fixture
def tree():
    return cst.parse_module(
        """
def foo():
    pass

def bar():
    pass

class Foo:
    pass

class Bar:
    pass
"""
    )


@pytest.fixture
def nodes():
    return ["foo", "Bar"]


def test_node_remover_init(nodes):
    remover = NodeRemover(nodes)
    assert remover.nodes == nodes


def test_remove_nodes_from_tree(tree, nodes):
    updated_tree = remove_nodes_from_tree(tree, nodes)
    assert len(updated_tree.body) == 2
    assert isinstance(updated_tree.body[0], cst.FunctionDef)
    assert isinstance(updated_tree.body[1], cst.ClassDef)
    assert updated_tree.body[0].name.value == "bar"
    assert updated_tree.body[1].name.value == "Foo"
