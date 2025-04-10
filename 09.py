#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama

from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

# 异步流式输出
async def async_stream():
  async for chunk in llm.astream("日本在哪里？"):
    print(chunk, end="|", flush=True)

asyncio.run(async_stream())
print("==============")