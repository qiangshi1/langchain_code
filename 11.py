#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from pprint import pprint
from langchain_community.llms import Ollama

from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.callbacks import StdOutCallbackHandler

llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

# async def async_stream():
#   events=[]
#   async for event in llm.astream_events("hello", version="v2"):
#     events.append(event)
#   pprint(events)

# asyncio.run(async_stream()) # 打印所有callback？

handler = StdOutCallbackHandler()
prompt = PromptTemplate.from_template("1 + {number} = ")

chain = prompt | llm

ret = chain.invoke({"number": 1})
print(ret)

print("=============================")
# callbacks会在chain执行的某些步骤时执行，如果传入StdOutCallbackHandler，就会添加一些打印
ret = chain.invoke({"number": 2}, config={"callbacks": [handler]})
print(ret)
