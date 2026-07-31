import os

import tiktoken
import typer
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain_openrouter import ChatOpenRouter

from .models import models

def _get_api_key(model_name) -> str:
    """Check env vars and prompt if missing."""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        api_key = typer.prompt("API key not set. Enter API key: ")
    return api_key

class LLM:
    """
    A class for running a Language Model Chain.
    """
    def __init__(self, prompt: PromptTemplate, temperature=0, model_name="gpt-3.5-turbo-instruct"):
        """
        Initializes the LLM class.

        Args:
          prompt (PromptTemplate): The prompt template to use.
          temperature (int, optional): The temperature to use for the model. Defaults to 0.
          model_name (str, optional): The name of the model to use. Defaults to "gpt-3.5-turbo-instruct".

        Side Effects:
          Sets the class attributes.

        Raises:
          KeyError: If the model_name is not found in the models dictionary.
        """
        self.prompt = prompt
        self.prompt_size = self.number_of_tokens(prompt.template)
        self.temperature = temperature
        self.model_name = model_name
        self.api_key = _get_api_key(model_name)

        try:
            self.max_tokens = int(models[model_name]["context_window"])
        except KeyError:
            self.max_tokens = 4096
            if model_name.startswith('gpt-4'):
                self.max_tokens = 8192
            elif model_name.startswith('gpt-3'):
                self.max_tokens = 4096

    async def run(self, code, **kwargs):
        """
        Runs the Language Model Chain asynchronously.

        Args:
          code (str): The code to use for the chain.
          **kwargs (dict): Additional keyword arguments.

        Returns:
          str: The generated text.
        """
        # openAI API
        if self.model_name in models:
          if "-instruct" in self.model_name:
              llm = OpenAI(
                  temperature=self.temperature, max_tokens=-1, model_name=self.model_name, api_key=self.api_key
              )
          else:
              llm = ChatOpenAI(
                  temperature=self.temperature, model_name=self.model_name, api_key=self.api_key
              )
        # openrouter API
        else:
          llm = ChatOpenRouter(temperature=self.temperature, model_name=self.model_name, api_key=self.api_key)

        # LCEL: compose prompt → llm → output parser instead of LLMChain
        chain = self.prompt | llm | StrOutputParser()
        return await chain.ainvoke({"code": code, **kwargs})

    def number_of_tokens(self, text):
        """
        Counts the number of tokens in a given text.

        Args:
          text (str): The text to count tokens for.

        Returns:
          int: The number of tokens in the text.
        """
        encoding = tiktoken.encoding_for_model("gpt-4")
        return len(encoding.encode(text))
