#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.agents import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from langchain.agents import AgentExecutor
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate

# 这例子没跑出来，似乎是大模型本身的问题，但是该例子还挺有意思的，还是得关注下

class InputPrinterCallback(BaseCallbackHandler):
  def __init__(self):
    self.printed = False
  def on_llm_start(self, serialized, prompts, **kwargs):
    if not self.printed:
      print("\n===== 最终发给大模型的提问 =====")
      for prompt in prompts:
        print(prompt)
      print("="*32)
      self.printed = True

  def on_llm_end(self, response, **kwargs):
    print("\n===== 大模型回答完毕 =====")

#  工具1 search
search = TavilySearchResults(max_results=2, tavily_api_key=os.getenv("TAVILY_API_KEY"))

# 工具2 猫
loader = WebBaseLoader(
    "https://baike.baidu.com/item/%E7%8C%AB/22261"
)

docs = loader.load()

documents = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
).split_documents(docs)

embeddings = OllamaEmbeddings(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_EMBEDDING_MODEL"))

vector = FAISS.from_documents(
    documents,
    embeddings
)

retriever = vector.as_retriever()

print(retriever.invoke("猫的特征")[0])

print("-"*80)

retriever_tool = create_retriever_tool(
    retriever,
    "cat_search",
    "搜索猫百科"
)

tools = [search, retriever_tool]

model = OllamaLLM(
    base_url=os.getenv("OLLAMA_HOST"),
    model=os.getenv("OLLAMA_MODEL"),
    temperature=0.5,
    timeout=300.0,
    top_p=0.9,
    repeat_penalty=1.1
)

# prompt = hub.pull("hwchase17/react")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format to answer the question. Don't use any other format or use none format.

All of your answers should begin with `Question:`/`Thought:`/`Action:`/`Action Input:`/`Observation:`/`Thought:`/`Final Answer:`. The following contents should as the format.

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""),
        ("user", "{input}"),
    ]
)

agent = create_react_agent(
    model,
    tools,
    prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

print(agent_executor.invoke({"input": "猫的特征?今天上海天气怎么样？"}, config={"callbacks": [InputPrinterCallback()]}))