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

model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))

temp_chat_history = ChatMessageHistory()
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
      MessagesPlaceholder(variable_name="history"),
      (
        "human",
        "请总结一下我们的聊天记录，用200字以内的中文回答。"
      )
    ] 
  )
  summarization_chain=summarization_prompt|model
  summary_message=summarization_chain.invoke(stored_messages, config={"configurable": {"callbacks": [InputPrinterCallback()]}})
  temp_chat_history.clear()
  temp_chat_history.add_ai_message(summary_message)
  return True

chain_with_trimming = (
  RunnablePassthrough.assign(message_summerized = summarize_messages)
  | chain_with_message_history
)
