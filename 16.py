#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import asyncio
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.runnables import ConfigurableFieldSpec

# 先启动一个redis服务器：
# redis-server
# 可以使用vscode redis插件检查消息是否已存储

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "You're an assistant who's good at {ability}. Rspond in 20 words or fewer"
    ),
    MessagesPlaceholder(variable_name="history"),
    (
      "human",
      "{input}"
    )
  ]
)
model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))
runnable = prompt | model

store = {} # 用来存储会话记录

REDIS_URL=base_url=os.getenv("REDIS_URL")

def get_session_history(session_id: str) -> RedisChatMessageHistory:
  return RedisChatMessageHistory(session_id, url=REDIS_URL)

with_message_history = RunnableWithMessageHistory(
  runnable,
  get_session_history,
  input_messages_key="input",
  history_messages_key="history",
)
print("====part1")
response = with_message_history.invoke(
  {"ability": "math", "input": "余弦是什么意思？"},
  config={"configurable": {"session_id": "abc123"}}
)
print(response)
print("====part2")
response = with_message_history.invoke(
  {"ability": "math", "input": "什么？"},
  config={"configurable": {"session_id": "abc123"}}
)
print(response)
print("====part3")
response = with_message_history.invoke(
  {"ability": "math", "input": "什么？"},
  config={"configurable": {"session_id": "def234"}}
)
print(response)

