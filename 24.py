#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama
from langchain_core.tools import tool
from langchain_core.callbacks import BaseCallbackHandler
from pydantic import BaseModel, Field

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

model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

# @tool
@tool # 把一个函数变成一个langchain工具
def multiply(a: int, b: int) -> int:
  """Multiply two integers."""
  return a * b

print(multiply.name)
print(multiply.description)
print(multiply.args)

# @tool支持异步
@tool
async def amultiply(a: int, b: int) -> int:
  """Multiply two integers."""
  return a * b

print(amultiply.name)
print(amultiply.description)
print(amultiply.args)

# 字段拓展
# @tool 增加description
class CalculatorInput(BaseModel):
  a: int = Field(description="第一个整数")
  b: int = Field(description="第二个整数")
@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
def multiply2(a: int, b: int) -> int:
  """Multiply two integers."""
  return a * b

print(multiply2.name)
print(multiply2.description)
print(multiply2.args)

# StructedTool，类似于@tool

