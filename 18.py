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
from langchain.callbacks import StdOutCallbackHandler

# 总结历史聊天记录

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

def remove_think(message:str):
  # 移除<think>标签内容
  if "<think>" in message and "</think>" in message:
    start = message.find("<think>")
    end = message.find("</think>") + len("</think>")
    message = message[:start] + message[end:]
  return message

prompt = ChatPromptTemplate.from_messages(
  [
    (
      "system",
      "你是一个乐于助人的助手，尽力回答所有问题，提供的聊天历史包括您与交谈的用户的事实。"
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    (
      "user",
      "{input}"
    )
  ]
)

class ChatMessageHistoryWithoutThink(ChatMessageHistory):
  def add_ai_message(self, message: str) -> None:
    message_without_think = remove_think(message)
    super().add_ai_message(message_without_think)

temp_chat_history = ChatMessageHistory()

model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))
chain = prompt | model
chain_with_message_history = RunnableWithMessageHistory(
  chain,
  lambda session_id: temp_chat_history,
  input_messages_key="input",
  history_messages_key="chat_history"
)

temp_chat_history = ChatMessageHistoryWithoutThink() # 希望把AI答复的think从历史消息中移除，但是没搞出来
temp_chat_history.add_user_message("我叫Jack，你好")
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我今天心情挺开心")
temp_chat_history.add_ai_message("你今天心情怎么样？")
temp_chat_history.add_user_message("我下午在打篮球")
temp_chat_history.add_ai_message("你下午在做什么？")

def summarize_messages(chain_input):
  stored_messages=temp_chat_history.messages
  if len(stored_messages) == 0:
    return False
  summarization_prompt = ChatPromptTemplate.from_messages(
    [
      MessagesPlaceholder(variable_name="chat_history"),
      (
        "user",
        "将上述聊天消息浓缩成一条摘要消息。尽可能地包含多个细节，比如要包含名字。"
      )
    ]
  )
  summarization_chain=summarization_prompt|model
  summary_message=summarization_chain.invoke(stored_messages, config={"callbacks": [InputPrinterCallback()]})
  temp_chat_history.clear()
  summary_message_without_think=remove_think(summary_message)
  temp_chat_history.add_ai_message(summary_message_without_think)
  print("xxxx")
  print(temp_chat_history)
  print("yyyy")
  return True

chain_with_summarization = (
  RunnablePassthrough.assign(message_summerized = summarize_messages) |
  chain_with_message_history
)

response = chain_with_summarization.invoke(
  {"input": "名字，下午在干嘛，心情"},
  config={"configurable": {"session_id": "unused"}, "callbacks": [InputPrinterCallback()]}
)

print(response)
print("zzzz")
print(temp_chat_history.messages)