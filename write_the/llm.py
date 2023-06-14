from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import tiktoken


class LLM:
    """
    A class for running a Language Model Chain.
    """
    def __init__(self, prompt: PromptTemplate, temperature=0, gpt_4=False):
        """
        Initializes the LLM class.
        Args:
            prompt (PromptTemplate): The prompt template to use.
            temperature (int): The temperature to use for the model.
            gpt_4 (bool): Whether to use GPT-4 or Text-Davinci-003.
        Side Effects:
            Sets the class attributes.
        """
        self.prompt = prompt
        self.prompt_size = self.number_of_tokens(prompt.template)
        self.temperature = temperature
        self.gpt_4 = gpt_4
        self.model_name = "gpt-4" if self.gpt_4 else "text-davinci-003"
        self.max_tokens = 4097 * 2 if self.gpt_4 else 4097

    async def run(self, code, **kwargs):
        """
        Runs the Language Model Chain.
        Args:
            code (str): The code to use for the chain.
            **kwargs (dict): Additional keyword arguments.
        Returns:
            str: The generated text.
        """
        llm = OpenAI(
            temperature=self.temperature, max_tokens=-1, model_name=self.model_name
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
