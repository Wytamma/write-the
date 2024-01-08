import pytest
import libcst as cst
from write_the.cst.function_and_class_collector import (
    FunctionAndClassCollector,
    get_node_names,
)


@pytest.fixture
def tree():
    return cst.parse_module("def foo(): pass\nclass Bar: pass")


@pytest.fixture
def force():
    return False


def test_visit_FunctionDef_with_no_docstring(tree):
    collector = FunctionAndClassCollector(force=False)
    tree.visit(collector)
    assert collector.functions == ["foo"]


def test_visit_FunctionDef_with_docstring(tree):
    collector = FunctionAndClassCollector(force=True)
    tree.visit(collector)
    assert collector.functions == ["foo"]


def test_visit_ClassDef_with_no_docstring(tree):
    collector = FunctionAndClassCollector(force=False)
    tree.visit(collector)
    assert collector.classes == ["Bar"]


def test_visit_ClassDef_with_docstring(tree):
    collector = FunctionAndClassCollector(force=True)
    tree.visit(collector)
    assert collector.classes == ["Bar"]


def test_get_node_names(tree, force):
    assert get_node_names(tree, force) == ["Bar", "foo"]


def test_get_node_names_with_force_true(tree, force):
    assert get_node_names(tree, True) == ["Bar", "foo"]
