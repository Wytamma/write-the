from langchain.prompts import PromptTemplate


converters_template = """
Convert the following to the desired output.

```python
def add(a, b):
    return a + b
```
```typescript
function add(a: number, b: number): number {{
  return a + b;
}}
```

```{input_format}
{code}
```
```{output_format}
"""
write_converters_for_file_prompt = PromptTemplate(
    input_variables=["code", "input_format", "output_format"], 
    template=converters_template
)
