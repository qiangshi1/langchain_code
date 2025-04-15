#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.pydantic_v1 import BaseModel
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.llms import Ollama

db = SQLDatabase.from_uri("sqlite:///./data/Chinook.db")
model = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))
toolkit = SQLDatabaseToolkit(db=db, llm=model)
print(toolkit.get_tools())

# 官方工具包s，没跑通

agent_executor = create_sql_agent(
  llm=model,
  toolkit=toolkit,
  verbose=True,
  agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)


