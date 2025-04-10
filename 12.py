#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama

from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

async def task1():
  async for chunk in llm.astream("日本在哪里？"):
    print(chunk, end="|", flush=True)

async def task2():
  async for chunk in llm.astream("1+1=?"):
    print(chunk, end="|", flush=True)

async def main():
  # ---------------
  # # 同步调用（不好）
  # await task1()
  # await task2()

  # 异步调用（好）
  await asyncio.gather(task1(), task2())

asyncio.run(main())