from langchain.prompts import PromptTemplate


converters_template = """
Covert the following text in {input_format} format to an equivalent {output_format} format
Return only the converted output in a code block formatted as a "plaintext" file.

Code:
```plaintext
{code}
```
"""
write_converters_for_file_prompt = PromptTemplate(
    input_variables=["code", "input_format", "output_format"], template=converters_template
)
