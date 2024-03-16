---
title: Docstrings
---

# Automatically Generate Docstrings for yor Python Code With AI

The primary use case for `write-the` is to add docstrings to your Python code. You can do this using the `write-the docs` command.

```bash
write-the docs [OPTIONS] [PATH_TO_SOURCE_CODE]
```

By default the `write-the docs` command will add docstrings to all the `nodes` in the source code that are not already documented. You can run the docs command on an entire directory or a single file. 

```bash
❯ write-the docs src/
✅ src/multiply.py
def multiply(a, b):
    """
    Multiplies 2 numbers.

    Args:
      a (int or float): The first number to multiply.
      b (int or float): The second number to multiply.

    Returns:
      int or float: The product of a and b.

    Examples:
      >>> multiply(2, 3)
      6
      >>> multiply(1.5, 4)
      6.0
    """
    return a * b
```

The ✅ indicates that the docstrings were created. If there is an error (❌) adding the docstrings, the error message will be printed to the console. Any nodes that already have docstrings will be skipped (⏭️).

## Save 

By default the docstrings will be printed to the console, you can use the `--save` flag to write the docstrings to the source code.

```bash
❯ write-the docs --save src/
⏭️ src/multiply_docstring.py - No nodes found, skipping file...
✅ src/multiply.py
✅ src/calculate.py
```

## Generate docs for specific nodes

A node is a function, class or class.method block. You can use the `--node` (`-n`) flag to specify which nodes to document (this will overwrite existing docstrings). 

```bash
write-the docs src/ -n function_name -n class_name -n class.method_name
```

## Force and Update

You can also use the `--force` flag to overwrite all existing docstrings in the specified folder or file.

```bash
write-the docs --force src/some_file.py
```

You can use the `--update` flag to update existing docstrings. For example the command that was used to update the docstrings in the `write-the` codebase in [this commit](https://github.com/Wytamma/write-the/commit/862928a4467b9afd30443fc2332384c88c780d24) was:

```bash
write-the docs --update --save src/
```
