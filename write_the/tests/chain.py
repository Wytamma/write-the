from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI


tests_template = """
Generate pytest unit tests for the code below, covering all possible scenarios and edge cases. 
Use fixtures and parametrize when appropriate. 
Import the code from {path} and adjust any relative imports. 
Return only the test code.

Code:
```python
{code}
```
"""
docs_prompt = PromptTemplate(input_variables=["code", "path"], template=tests_template)

def run(code, path, temperature=0, max_tokens=-1, gpt_4=False) -> str:
    """
    Generates unit tests for a given code snippet using the pytest framework.
    Args:
      code (str): The code snippet to generate tests for.
      path (str): The path to the code snippet.
      temperature (float, optional): The temperature parameter for the OpenAI model. Defaults to 0.
      max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 2000.
      gpt_4 (bool, optional): Whether to use the GPT-4 model. Defaults to False.
    Returns:
      str: The generated unit tests.
    Notes:
      The tests should cover all possible scenarios, including edge cases.
      The code should be imported from `path` and any relative imports should be fixed.
    Examples:
      >>> run(code="def add(a, b): return a + b", path="my_code.py")
      import my_code
      @pytest.mark.parametrize("a, b, expected", [
          (1, 2, 3),
          (2, 3, 5),
          (3, 4, 7)
      ])
      def test_add(a, b, expected):
          assert my_code.add(a, b) == expected
    """
    model_name = "gpt-4" if gpt_4 else "text-davinci-003"
    llm = OpenAI(temperature=temperature, max_tokens=max_tokens, model_name=model_name)
    docs_chain = LLMChain(llm=llm, prompt=docs_prompt)
    return docs_chain.predict(code=code, path=path)
