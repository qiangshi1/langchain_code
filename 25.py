#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama
from langchain_core.tools import StructuredTool
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

# StructedTool，类似于@tool

def multiply(a: int, b: int) -> int:
  """Multiply two integers."""
  return a * b

async def amultiply(a: int, b: int) -> int:
  """Multiply two integers."""
  return a * b

async def main():
  calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)
  print(calculator.invoke({"a":2, "b":3}))
  print(await calculator.ainvoke({"a":2, "b":5}))

asyncio.run(main())

class CalculatorInput(BaseModel):
  a: int = Field(description="第一个整数")
  b: int = Field(description="第二个整数")

# 支持字段拓展
async def main2():
  calculator = StructuredTool.from_function(func=multiply, name="calculator", description="multiply numbers", args_schema=CalculatorInput, coroutine=amultiply)
  print(calculator.invoke({"a":2, "b":3}))
  print(await calculator.ainvoke({"a":2, "b":5}))

asyncio.run(main2())


