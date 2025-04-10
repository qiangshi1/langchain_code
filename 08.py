#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.llms import Ollama

from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

chunks = []


# 流式输出
for chunk in llm.stream("天空是什么颜色？"):
  chunks.append(chunk)
  print(chunk, end="|", flush=True)
