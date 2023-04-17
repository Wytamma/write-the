from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

llm = OpenAI(temperature=0, max_tokens=2000)
tests_template = """
Please generate unit tests for the following code using the pytest framework. 
Include fixtures where appropriate, and only return test code. 
The tests should cover all possible scenarios, including edge cases. 
Include imports where required. Do not provide explanations or additional information. 
Remember to import the code from {path} and fix any relative imports. 
Please generate pytest test functions for the following code:
```python
{code}
```
"""
docs_prompt = PromptTemplate(input_variables=["code", "path"], template=tests_template)
docs_chain = LLMChain(llm=llm, prompt=docs_prompt)

def run(code, path) -> str:
    return docs_chain.predict(code=code, path=path)
