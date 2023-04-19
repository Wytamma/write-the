from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI


docs_template = """
Provide Google style docstrings for the given code. 
Include description, parameter types, exceptions, side effects, and examples. 
For detailed instructions, refer to the Google style guide. 
Return only the docstrings, with function/class names as keys. 
Use the Class.method format for methods. Separate results by newlines.

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

def run(code, nodes: list) -> str:
    """
    Generates docstrings for a given code and list of nodes.
    Args:
      code (str): The code to generate docstrings for.
      nodes (list): A list of nodes to generate docstrings for.
    Returns:
      str: The generated docstrings.
    Examples:
      >>> run('from langchain.prompts import PromptTemplate', ['PromptTemplate'])
      'PromptTemplate:
        A class for generating prompts.
        Attributes:
          input_variables (list): A list of input variables for the prompt.
          template (str): The template for the prompt.'
    """
    llm = OpenAI(temperature=0, max_tokens=-1)
    docs_prompt = PromptTemplate(input_variables=["code", "nodes"], template=docs_template)
    docs_chain = LLMChain(llm=llm, prompt=docs_prompt)
    nodes = ",".join(nodes)
    return docs_chain.predict(code=code, nodes=nodes)
