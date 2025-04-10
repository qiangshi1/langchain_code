#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=("你是一位人工智能助手，你的名字是{name}。")
        ),
        MessagesPlaceholder("msgs")
    ]
)

result = prompt_template.invoke({"msgs": [HumanMessage(content="你好"), AIMessage(content="我很好，谢谢"), HumanMessage(content="你的名字是什么？")]})

print(result)
# [SystemMessage(content='你是一位人工智能助手，你的名字是Bob。'), HumanMessage(content='你好'), AIMessage(content='我很好，谢谢'), HumanMessage(content='你的名字是什么？')]
