#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import tempfile
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma # 向量数据库
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_ollama import OllamaLLM
from langchain_community.llms import OpenAI
from langchain_core.callbacks import BaseCallbackHandler

# print("===========")
# print(os.getenv("OPENAI_KEY"))

# exit()

# 这例子也没跑通，服了


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

# 启动方式为`streamlit run 32.py`
# 上传32.txt试试

st.set_page_config(page_title="文档问答", layout="wide")
st.title("文档问答")
uploaded_files = st.sidebar.file_uploader("上传文件", type=["txt"], accept_multiple_files=True)
if not uploaded_files:
  st.info("请上传一个或多个txt文件。")
  st.stop()

@st.cache_resource(ttl="1h") #
def configure_retriever(uploaded_files):
  docs=[]
  temp_dir = tempfile.TemporaryDirectory("langchain_code")
  for file in uploaded_files:
    temp_filepath = os.path.join(temp_dir.name, file.name)
    with open(temp_filepath, "wb") as f:
      f.write(file.getvalue())
    loader = TextLoader(temp_filepath, encoding="utf-8")
    docs.extend(loader.load())

  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
  splits = text_splitter.split_documents(docs)
  embeddings = OllamaEmbeddings(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_EMBEDDING_MODEL"))
  vetordb=Chroma.from_documents(splits, embeddings)
  retriever = vetordb.as_retriever()
  return retriever

retriever = configure_retriever(uploaded_files)

if "messages" not in st.session_state or st.sidebar.button("清除聊天记录"):
  st.session_state["messages"] = [{"role": "assistant", "content": "你好！我是文档问答助手"}]

for msg in st.session_state.messages:
  st.chat_message(msg["role"]).write(msg["content"])

from langchain.tools.retriever import create_retriever_tool

tool = create_retriever_tool(
  retriever,
  "文档检索",
  "用于检索用户提出的问题，并基于检索到的文档内容进行回复。"
)

tools=[tool]

msgs= StreamlitChatMessageHistory()

memory = ConversationBufferMemory(
  chat_memory=msgs,
  return_messages=True,
  memory_key="chat_history",
  output_key="output"
)

# 指令模板

instructions = """你是一个设计用于查询文档来回答问题的代理。
你可以使用文档检索工具，并给予检索内容来回答问题。
你可能不查询文档就知道答案，但是你仍然应该查询文档来获得答案。
如果你从文档中找不到任何信息用于回答问题，则只需返回“抱歉，这个问题我还不知道答案。”作为答案。"""

base_prompt_template="""{instructions}

Answer the following questions as best you can. You have access to the following tools:
TOOLS:
------

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: {input}
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New Question: {input}
{agent_scratchpad}"""

base_prompt = PromptTemplate.from_template(base_prompt_template)
prompt = base_prompt.partial(instructions=instructions)
# llm = OllamaLLM(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))
llm = OpenAI(base_url=os.getenv("OPENAI_HOST"), openai_api_key=os.getenv("OPENAI_KEY"), model="gpt-3.5-turbo")


agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, max_iterations=3, tools=tools, memory=memory, verbose=True, handle_parsing_errors="没有从知识库检索到相似内容")

user_query = st.chat_input(placeholder="请开始提问吧")

if user_query:
  # 添加用户消息到session_state
  st.session_state.messages.append({"role": "user", "content": user_query})
  # 显示用户消息
  st.chat_message("user").write(user_query)

  with st.chat_message("assistant"):
    # 创建Streamlit回调处理器
    st_cb = StreamlitCallbackHandler(st.container())
    # agent执行过程日志回调显示在Streamlit Container（如思考、选择工具、执行查询、观察结果等）
    config = {"callbacks": [st_cb, InputPrinterCallback()]}
    # 执行agent并获取响应
    response = agent_executor.invoke({"input": user_query}, config=config)
    # 添加助手消息到session_state
    st.session_state.messages.append({"role": "assistant", "content": response["output"]})