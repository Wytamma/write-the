from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

class LLM:
    def __init__(self, prompt: PromptTemplate, temperature=0, max_tokens=-1, gpt_4=False):
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.gpt_4 = gpt_4
        self.model_name = "gpt-4" if self.gpt_4 else "text-davinci-003"

    async def run(self, code, **kwargs):
        llm = OpenAI(
            temperature=self.temperature, 
            max_tokens=self.max_tokens, 
            model_name=self.model_name
        )
        chain = LLMChain(llm=llm, prompt=self.prompt)
        return await chain.apredict(code=code, **kwargs)