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

chain = ( llm ) # 对比看下
chain = ( llm | JsonOutputParser() )

async def async_stream():
  async for chunk in chain.astream(
    "以JSON格式输出法国、西班牙和日本的国家及其人口列表。"
    '使用一个带有"countries"外部键的字典，其中包含国家列表。'
    "每个国家都应该有键`name`和`population`"
  ):
    print(chunk, flush=True)

asyncio.run(async_stream())