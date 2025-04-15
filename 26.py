#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama
from langchain_core.tools import StructuredTool, ToolException
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

# StructedTool，工具出错怎么办？做agent开发捕获异常要使用的

def get_weather(city: str) -> int:
  """获取给定城市的天气。"""
  raise ToolException(f'错误：没有名为{city}的城市。')

get_weather_tool = StructuredTool.from_function(
  func=get_weather,
  handle_tool_error=True # 出错时，返回错误信息，若果设置False会抛异常
)
response = get_weather_tool.invoke({"city": "北京"})
print(response)

# 另一种写法
get_weather_tool2 = StructuredTool.from_function(
  func=get_weather,
  handle_tool_error="没有这个城市" # 出错时，返回错误信息，若果设置False会抛异常
)
response2 = get_weather_tool2.invoke({"city": "北京"})
print(response2)

# 另一种写法
def _handle_error(error: ToolException)->str:
  return f"工具执行期间发生以下错误：`{error.args[0]}`"

get_weather_tool3 = StructuredTool.from_function(
  func=get_weather,
  handle_tool_error=_handle_error # 出错时，返回错误信息，若果设置False会抛异常
)

response3 = get_weather_tool3.invoke({"city": "北京"})
print(response3)
