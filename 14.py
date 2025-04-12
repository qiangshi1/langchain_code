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

def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = ChatMessageHistory()
  return store[session_id]

with_message_history = RunnableWithMessageHistory(
  runnable,
  get_session_history,
  input_messages_key="input",
  history_messages_key="history",
)
print("====part1")
response = with_message_history.invoke(
  {"ability": "math", "input": "余弦是什么意思？"},
  config={"configurable": {"session_id": "abc123"}, "callbacks": [InputPrinterCallback()]}
)
print(response)
print("====part2")
response = with_message_history.invoke(
  {"ability": "math", "input": "什么？"},
  config={"configurable": {"session_id": "abc123"}, "callbacks": [InputPrinterCallback()]}
)
print(response)
print("====part3")
response = with_message_history.invoke(
  {"ability": "math", "input": "什么？"},
  config={"configurable": {"session_id": "def234"}, "callbacks": [InputPrinterCallback()]}
)
print(response)
