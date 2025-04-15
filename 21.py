#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.pydantic_v1 import BaseModel, Field

class InputPrinterCallback(BaseCallbackHandler):
  def __init__(self):
    self.printed = False
  def on_llm_start(self, serialized, prompts, **kwargs):
    if not self.printed:
      print("\n===== 最终发给大模型的提问 =====")
      for prompt in prompts:
        print(prompts)
      print("="*32)
      self.printed = True


# output parser
  # JsonOutputParser+流式

model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

class Joke(BaseModel): # json格式，约束AI的输出
  setup: str = Field(description="设置笑话的问题")
  punchline: str = Field(description="解决笑话的答案")

joke_query = "告诉我一个笑话。"
parser = JsonOutputParser(pydantic_object=Joke)
prompt = PromptTemplate(
  template="回答用户的查询。\n{format_instructions}\n{query}",
  input_variables=["query"],
  partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | model | parser
# invoke改成stream
for s in chain.stream({"query": joke_query}, config={"callbacks": [InputPrinterCallback()]}):
  print(s)


