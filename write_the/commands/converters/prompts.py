from langchain.prompts import PromptTemplate


converters_template = """
Convert the following to the desired output.
Example:
```python
def add(a, b):
    return a + b
```
```javascript
function add(p1, p2) {{
  return p1 + p2;
}}
```
Code:
```{input_format}
{code}
```
```{output_format}
"""
write_converters_for_file_prompt = PromptTemplate(
    input_variables=["code", "input_format", "output_format"], 
    template=converters_template
)
