#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位人工智能助手，你的名字是{name}。"),
        ("human", "你好"),
        ("ai", "我很好，谢谢"),
        ("human", "{user_input}")
    ]
)

# 下边写法等价于上边写法，下边写法更常用
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=("你是一位人工智能助手，你的名字是{name}。")
        ),
        HumanMessage(
            content=("你好")
        ),
        AIMessage(
            content=("我很好，谢谢")
        ),
        HumanMessage(
            content=("{user_input}")
        )
    ]
)

messages = chat_template.format_messages(name="Bob", user_input="你的名字是什么？")

print(messages)
# [SystemMessage(content='你是一位人工智能助手，你的名字是Bob。'), HumanMessage(content='你好'), AIMessage(content='我很好，谢谢'), HumanMessage(content='你的名字是什么？')]
