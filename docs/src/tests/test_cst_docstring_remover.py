import pytest
import libcst as cst
from write_the.cst.docstring_remover import DocstringRemover, remove_docstrings
from write_the.cst.utils import get_docstring


@pytest.fixture
def tree():
    return cst.parse_module(
        """
def foo():
    '''This is a docstring.'''
    pass

def bar():
    '''This is another docstring.'''
    pass

class Foo:
    '''This is a class docstring.'''
    pass

class Bar:
    '''This is another class docstring.'''
    pass
"""
    )


@pytest.fixture
def nodes():
    return ["foo", "Bar"]


def test_leave_FunctionDef(tree, nodes):
    remover = DocstringRemover(nodes)
    updated_tree = tree.visit(remover)
    assert get_docstring(updated_tree.body[0]) is None
    assert get_docstring(updated_tree.body[1]) == "'''This is another docstring.'''"


def test_leave_ClassDef(tree, nodes):
    remover = DocstringRemover(nodes)
    updated_tree = tree.visit(remover)
    assert get_docstring(updated_tree.body[2]) == "'''This is a class docstring.'''"
    assert get_docstring(updated_tree.body[3]) is None


def test_remove_docstrings(tree, nodes):
    updated_tree = remove_docstrings(tree, nodes)
    assert get_docstring(updated_tree.body[0]) is None
    assert get_docstring(updated_tree.body[1]) == "'''This is another docstring.'''"
    assert get_docstring(updated_tree.body[2]) == "'''This is a class docstring.'''"
    assert get_docstring(updated_tree.body[3]) is None
