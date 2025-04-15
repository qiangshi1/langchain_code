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
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables import RunnablePassthrough

# 记录遗忘

class InputPrinterCallback(BaseCallbackHandler):
  def __init__(self):
    self.printed = False
  def on_llm_start(self, serialized, prompts, **kwargs):
    if not self.printed:
      print("\n===== 最终发给大模型的提问 =====")
      for prompt in prompts:
        print(prompts)
      print("="*32)
      self.printed = True

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "你是一个乐于助人的助手，尽力回答所有问题，提供的聊天历史包括您与交谈的用户的事实。"
    ),
    MessagesPlaceholder(variable_name="history"),
    (
      "human",
      "{input}"
    )
  ]
)
model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))
chain = prompt | model

temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message("我叫Jack，你好")
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我今天心情挺开心")
temp_chat_history.add_ai_message("你今天心情怎么样？")
temp_chat_history.add_user_message("我下午在打篮球")
temp_chat_history.add_ai_message("你下午在做什么？")

def trim_messages(chain_input):
  thre=2 # 把它改成5试试
  stored_messages=temp_chat_history.messages
  if len(stored_messages)<=thre: #
    return False
  temp_chat_history.clear()
  for message in stored_messages[-thre:]:
    temp_chat_history.add_message(message)
  return True

with_message_history = RunnableWithMessageHistory(
  chain,
  lambda session_id: temp_chat_history,
  input_messages_key="input",
  history_messages_key="history",
)

chain_with_trimming = (
  RunnablePassthrough.assign(messages_trimmed = trim_messages)
  | with_message_history
)

response = chain_with_trimming.invoke(
  {"input": "我叫什么名字？"},
  {"configurable": {"session_id": "unused"}, "callbacks": [InputPrinterCallback()]}
)
print(response)
print(temp_chat_history.messages)
