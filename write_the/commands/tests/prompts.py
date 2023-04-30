from langchain.prompts import PromptTemplate


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
write_tests_for_file_prompt = PromptTemplate(
    input_variables=["code", "path"], template=tests_template
)
