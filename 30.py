#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=2, tavily_api_key=os.getenv("TAVILY_API_KEY"))

print(search.invoke("今天天气怎么样？"))