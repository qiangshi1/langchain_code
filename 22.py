#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import XMLOutputParser
from langchain_core.callbacks import BaseCallbackHandler

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
  # XmlOutputParser

# 格式失败！！！
model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

action_query = "生成周星驰的简化电影作品列表，安按照最新的时间降序"
parser = XMLOutputParser(tags=["movies","actor","film","name","genre"])
prompt = PromptTemplate(
  template="回答用户的查询。\n{format_instructions}\n{query}",
  input_variables=["query"],
  partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | model | parser
output = chain.invoke({"query": action_query}, config={"callbacks": [InputPrinterCallback()]})
print(output)


