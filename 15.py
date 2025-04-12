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

def get_session_history(user_id: str, conversation_id: str) -> BaseChatMessageHistory:
  if (user_id, conversation_id) not in store:
    store[user_id, conversation_id] = ChatMessageHistory()
  return store[user_id, conversation_id]

with_message_history = RunnableWithMessageHistory(
  runnable,
  get_session_history,
  input_messages_key="input",
  history_messages_key="history",
  history_factory_config=[
    ConfigurableFieldSpec(
      id="user_id",
      annotation=str,
      name="User ID",
      description="用户唯一标识符。",
      default="",
      is_shared=True,
    ),
    ConfigurableFieldSpec(
      id="conversation_id",
      annotation=str,
      name="Conversation ID",
      description="对话唯一标识符。",
      default="",
      is_shared=True,
    )
  ]
)
print("====part1")
response = with_message_history.invoke(
  {"ability": "math", "input": "余弦是什么意思？"},
  config={"configurable": {"user_id": "abc", "conversation_id": "123"}, "callbacks": [InputPrinterCallback()]}
)
print(response)
print("====part2")
response = with_message_history.invoke(
  {"ability": "math", "input": "什么？"},
  config={"configurable": {"user_id": "abc", "conversation_id": "123"}, "callbacks": [InputPrinterCallback()]}
)
print(response)
print("====part3")
response = with_message_history.invoke(
  {"ability": "math", "input": "什么？"},
  config={"configurable": {"user_id": "def", "conversation_id": "456"}, "callbacks": [InputPrinterCallback()]}
)
print(response)
