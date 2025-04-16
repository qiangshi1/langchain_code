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
from langchain.agents import create_tool_calling_agent
from langchain.agents import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools.retriever import create_retriever_tool

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

retriever=vector.as_retriever()

print(retriever.invoke("猫的特征")[0])

retriever_tool=create_retriever_tool(
    retriever,
    "wikipedia_search",
    "搜索维基百科"
)

tools = [search, retriever_tool]

model = OllamaLLM(
    base_url=os.getenv("OLLAMA_HOST"),
    model=os.getenv("OLLAMA_MODEL"),
    temperature=0.7,
    timeout=300.0,
    top_p=0.9,
    repeat_penalty=1.1
)

from langchain import hub
# prompt = hub.pull("hwchase17/openai-functions-agent") # 标准提示词模板 https://smith.langchain.com/hub/hwchase17/openai-functions-agent
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(
    model,
    tools,
    prompt
)

from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

print(agent_executor.invoke({"input": "猫的特征?今天上海天气怎么样？"}))