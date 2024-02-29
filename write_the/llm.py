from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import tiktoken
from .models import models

class LLM:
    """
    A class for running a Language Model Chain.
    """
    def __init__(self, prompt: PromptTemplate, temperature=0, model_name="gpt-3.5-turbo-instruct"):
        """
        Initializes the LLM class.
        Args:
            prompt (PromptTemplate): The prompt template to use.
            temperature (int): The temperature to use for the model.
            name (str): The name of the model to use.
        Side Effects:
            Sets the class attributes.
        """
        self.prompt = prompt
        self.prompt_size = self.number_of_tokens(prompt.template)
        self.temperature = temperature
        self.model_name = model_name
        self.max_tokens = int(models[model_name]["context_window"])

    async def run(self, code, **kwargs):
        """
        Runs the Language Model Chain.
        Args:
            code (str): The code to use for the chain.
            **kwargs (dict): Additional keyword arguments.
        Returns:
            str: The generated text.
        """
        if "-instruct" in self.model_name:
            llm = OpenAI(
                temperature=self.temperature, max_tokens=-1, model_name=self.model_name
            )
        else:
            llm = ChatOpenAI(
                temperature=self.temperature, model_name=self.model_name
            )
        chain = LLMChain(llm=llm, prompt=self.prompt)
        return await chain.apredict(code=code, **kwargs)

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
