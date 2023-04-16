from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0, max_tokens=2000)
docs_template = "\nWrite Google style docstrings for the following code, using the multi-line format with a description and examples. The first lines describe the code. Include parameter type definitions where possible, and specify any exceptions raised and side effects of the function. For functions with multiple return values or ambiguous behaviour, provide clear guidelines for documenting the behaviour. Please refer to the Google style guide for more information. Any notes should be include in the `Notes:` section of the docstring. Only return the docstring its self. Return each docstring on a single line with the name of the function/class as the key and the docstring as the value. Separate each result by a newline. If the function is a method return the name in the format Class.method. The Class docstrings should contain Description and Attributes. Each result should be separated by multiple newlines. \n---\nEXAMPLE\n---\n\ndef add(a, b): \n    return a + b \nHere are formatted docstrings for only add:\nadd:\n  Sums 2 numbers.\n  Args:\n    a (int): The first number to add.\n    b (int): The second number to add.\n  Returns:\n    int: The sum of `a` and `b`.\n  Examples:\n    >>> add(1, 2)\n    3\n\n\n---\nCODE\n---\n{code}\nHere are formatted docstrings for only {nodes}:\n"
docs_prompt = PromptTemplate(input_variables=["code", "nodes"], template=docs_template)
docs_chain = LLMChain(llm=llm, prompt=docs_prompt)


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
    nodes = ",".join(nodes)
    return docs_chain.predict(code=code, nodes=nodes)
