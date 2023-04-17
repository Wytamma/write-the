from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI


tests_template = """
Please generate unit tests for the following code using the pytest framework. 
Include fixtures and parametrize function where appropriate, and only return test code. 
The tests should cover all possible scenarios, including edge cases. 
Include imports where required. Do not provide explanations or additional information. 
Remember to import the code from `{path}` and fix any relative imports. 
Please generate pytest test functions for the following code:
```python
{code}
```
"""
docs_prompt = PromptTemplate(input_variables=["code", "path"], template=tests_template)

def run(code, path, temperature=0, max_tokens=2000, gpt_4=False) -> str:
    model_name = "gpt-4" if gpt_4 else "text-davinci-003"
    llm = OpenAI(temperature=temperature, max_tokens=max_tokens, model_name=model_name)
    docs_chain = LLMChain(llm=llm, prompt=docs_prompt)
    return docs_chain.predict(code=code, path=path)
