import libcst as cst
from write_the.cst.utils import has_docstring, nodes_to_tree
import pytest


@pytest.fixture
def cst_function_def():
    return cst.FunctionDef(
        name=cst.Name("function_name"),
        params=cst.Parameters(),
        body=cst.IndentedBlock(
            body=[
                cst.SimpleStatementLine(
                    body=[
                        cst.Expr(value=cst.SimpleString('"""This is a docstring."""'))
                    ]
                ),
                cst.SimpleStatementLine(body=[cst.Pass()]),
            ]
        ),
    )


@pytest.fixture
def cst_class_def():
    return cst.ClassDef(
        name=cst.Name("ClassName"),
        body=cst.IndentedBlock(
            body=[
                cst.SimpleStatementLine(
                    body=[
                        cst.Expr(
                            value=cst.SimpleString('"""This is a class docstring."""')
                        )
                    ]
                ),
                cst.SimpleStatementLine(body=[cst.Pass()]),
            ]
        ),
    )


def test_has_docstring_function_def(cst_function_def):
    assert has_docstring(cst_function_def)


def test_has_docstring_class_def(cst_class_def):
    assert has_docstring(cst_class_def)


def test_nodes_to_tree(cst_function_def, cst_class_def):
    tree = nodes_to_tree([cst_function_def, cst_class_def])
    assert isinstance(tree, cst.Module)
    assert len(tree.body) == 2
