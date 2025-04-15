#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.llms import Ollama
from langchain_core.callbacks import BaseCallbackHandler
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# 导入一些社区官方工具
# Community tools
# Wikipedia
# 这例子跑失败了，似乎是版本问题
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
tool = WikipediaQueryRun(api_wrapper=api_wrapper)
print(tool.invoke({"query": "langchain"}))

print(f"Name:{tool.name}")
print(f"Description:{tool.description}")
print(f"Args:{tool.args}")
print(f"returns directly?: {tool.return_direct}")