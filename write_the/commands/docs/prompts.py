from langchain.prompts import PromptTemplate


docs_template = """
Provide Google style docstrings for the given code. 
Include description, parameter types, exceptions, side effects, notes, and examples. 
Return only the docstrings, with function/class names as yaml keys. 
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
write_docstrings_for_nodes_prompt = PromptTemplate(
    input_variables=["code", "nodes"], template=docs_template
)

update_docs_template = """
Update the Google style docstrings to match the code.
Add, update or remove description, parameter types, exceptions, side effects, notes, examples, etc. if required.
Return only the docstrings, with function/class names as yaml keys.
Use the Class.method format for methods.

Example:
def add(first, second, third=0):
  \"\"\"
  Sums 2 numbers.

  Args:
    a (int): The first number to add.
    b (int): The second number to add.

  Returns:
    int: The sum of a and b.

  Examples:
    >>> add(1, 2)
    3
  \"\"\"
  return first + second + third
Updated docstrings for add:
add:
  Sums up to 3 numbers.

  Args:
    first (int): The first number to add.
    second (int): The second number to add.
    third (int, optional): The third number to add. Defaults to 0.

  Returns:
    int: The sum of first, second, and third.

  Examples:
    >>> add(1, 2)
    3
    >>> add(1, 2, 3)
    6

Code:
{code}
Updated docstrings for {nodes}:
"""

update_docstrings_for_nodes_prompt = PromptTemplate(
    input_variables=["code", "nodes"], template=update_docs_template
)