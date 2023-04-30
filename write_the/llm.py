from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
import tiktoken


class LLM:
    def __init__(self, prompt: PromptTemplate, temperature=0, gpt_4=False):
        self.prompt = prompt
        self.prompt_size = self.number_of_tokens(prompt.template)
        self.temperature = temperature
        self.gpt_4 = gpt_4
        self.model_name = "gpt-4" if self.gpt_4 else "text-davinci-003"
        self.max_tokens = 4097 * 2 if self.gpt_4 else 4097

    async def run(self, code, **kwargs):
        llm = OpenAI(
            temperature=self.temperature, max_tokens=-1, model_name=self.model_name
        )
        chain = LLMChain(llm=llm, prompt=self.prompt)
        return await chain.apredict(code=code, **kwargs)

    def number_of_tokens(self, text):
        encoding = tiktoken.encoding_for_model("gpt-4")
        return len(encoding.encode(text))
