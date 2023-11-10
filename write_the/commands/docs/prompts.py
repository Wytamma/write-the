from langchain.prompts import PromptTemplate


docs_template = """
Provide Google style docstrings for the given code. 
Include description, parameter types, exceptions, side effects, notes, and examples. 
Return only the docstrings, with function/class names as keys. 
Use the Class.method format for methods.

Example:
def add(a, b):
  return a + b
Formatted docstrings for add:
add:
  Sums 2 numbers.

  Args:
    a (int): The first number to add.
    b (int): The second number to add.

  Returns:
    int: The sum of a and b.

  Examples:
    >>> add(1, 2)
    3

Code:
{code}
Formatted docstrings for {nodes}:
"""
write_docstings_for_nodes_prompt = PromptTemplate(
    input_variables=["code", "nodes"], template=docs_template
)
