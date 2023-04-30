import pytest
import libcst as cst
from write_the.cst.docstring_adder import DocstringAdder
from write_the.cst.utils import has_docstring, get_docstring


@pytest.fixture
def docstrings():
    return {
        "function_name": "This is a docstring for a function.",
        "ClassName.method_name": "This is a docstring for a method.",
    }


@pytest.fixture
def force():
    return False


@pytest.fixture
def function_def_node():
    return cst.FunctionDef(
        name=cst.Name("function_name"),
        params=cst.Parameters(),
        body=cst.IndentedBlock(body=[cst.SimpleStatementLine(body=[cst.Pass()])]),
    )


@pytest.fixture
def class_def_node():
    return cst.ClassDef(
        name=cst.Name("ClassName"),
        body=cst.IndentedBlock(body=[cst.SimpleStatementLine(body=[cst.Pass()])]),
    )


@pytest.fixture
def method_def_node():
    method_def = cst.FunctionDef(
        name=cst.Name("method_name"),
        params=cst.Parameters(params=[cst.Param(name=cst.Name("cls"))]),
        body=cst.IndentedBlock(body=[cst.SimpleStatementLine(body=[cst.Pass()])]),
    )
    return cst.ClassDef(
        name=cst.Name("ClassName"),
        body=cst.IndentedBlock(body=[cst.SimpleStatementLine(body=[method_def])]),
    )


def test_leave_function_def_with_docstring(docstrings, force, function_def_node):
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.leave_FunctionDef(
        function_def_node, function_def_node
    )
    assert has_docstring(updated_node)


def test_leave_function_def_without_docstring(docstrings, force, function_def_node):
    docstrings.pop("function_name")
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.leave_FunctionDef(
        function_def_node, function_def_node
    )
    assert not has_docstring(updated_node)


def test_leave_class_def_with_docstring(docstrings, force, class_def_node):
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.leave_ClassDef(class_def_node, class_def_node)
    assert has_docstring(updated_node) is False


def test_leave_class_def_without_docstring(docstrings, force, class_def_node):
    docstrings.pop("ClassName.method_name")
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.leave_ClassDef(class_def_node, class_def_node)
    assert not has_docstring(updated_node)


def test_leave_method_def_without_docstring(
    docstrings, force, class_def_node, method_def_node
):
    docstrings.pop("ClassName.method_name")
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.leave_ClassDef(class_def_node, class_def_node)
    updated_node = docstring_adder.leave_FunctionDef(method_def_node, method_def_node)
    assert not has_docstring(updated_node)


def test_add_docstring_with_docstring(docstrings, force, function_def_node):
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.add_docstring(function_def_node)
    assert has_docstring(updated_node)


def test_add_docstring_without_docstring(docstrings, force, function_def_node):
    docstrings.pop("function_name")
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.add_docstring(function_def_node)
    assert not has_docstring(updated_node)


def test_add_docstring_with_force(docstrings, function_def_node):
    force = True
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.add_docstring(function_def_node)
    assert has_docstring(updated_node)


def test_add_docstring_escape_newline(docstrings, function_def_node):
    force = True
    docstrings["function_name"] = """\\ntest\ntest\\\\n\\n"""
    docstring_adder = DocstringAdder(docstrings, force)
    updated_node = docstring_adder.add_docstring(function_def_node)
    assert has_docstring(updated_node)
    assert (
        get_docstring(updated_node).strip('"""').strip()
        == """\\\\ntest\n    test\\\\n\\\\n"""
    )
