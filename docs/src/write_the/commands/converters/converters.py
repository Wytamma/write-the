from pathlib import Path
from .prompts import write_converters_for_file_prompt
from write_the.llm import LLM


async def write_the_converters(filename: Path, input_format: str, output_format: str, gpt_4: bool = False) -> str:
    """
    Formats and runs the tests for a given file.
    Args:
      filename (Path): The path to the file to be tested.
      input_format (str): The input format of the file.
      output_format (str): The format to convert the file to.
      gpt_4 (bool, optional): Whether to use GPT-4 for testing. Defaults to False.
    Returns:
      str: The converted output.
    Examples:
      >>> write_the_converters(Path(".travis.yml"), input_format="Travis CI", output_format="Github Actions", gpt_4=True)
      "The converted output"
    """
    with open(filename, "r") as file:
        source_text = file.read()

    llm = LLM(write_converters_for_file_prompt, gpt_4=gpt_4)
    result = await llm.run(code=source_text, input_format=input_format, output_format=output_format)

    formatted_text = (
        result.strip().rstrip('```')
    )
    return formatted_text.strip()
