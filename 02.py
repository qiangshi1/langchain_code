#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnableLambda  # Add this import


llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

llm = Ollama(base_url="http://172.16.12.97:11434", model="deepseek-r1:8b")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个世界级的技术专家."),
        ("user", "{input}"),
    ]
)

output_parser = StrOutputParser()

chain = prompt | llm | output_parser
result = chain.invoke({"input": "帮我写一篇关于AI的技术文章，100个字"})
print(result)