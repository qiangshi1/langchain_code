#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.llms import Ollama

from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

llm = Ollama(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_MODEL"))
embeddings = OllamaEmbeddings(base_url=os.getenv("OLLAMA_HOST"), model=os.getenv("OLLAMA_EMBEDDING_MODEL"))

examples = [
  {
    "question": "谁活得更长，穆罕默德·阿里还是艾伦·图灵？",
    "answer":
      """
      是否需要后续问题：是的。
      后续问题：穆罕默德·阿里去世时多大年纪？
      中间答案：穆罕默德·阿里去世时74岁。
      后续问题：艾伦·图灵去世时多大年纪？
      中间答案：艾伦·图灵去世时41岁。
      所以最终答案是：穆罕默德·阿里
      """,
  },
  {
    "question": "克雷格斯列表的创始人是什么时候出生的？",
    "answer":
      """
      是否需要后续问题：是的。
      后续问题：克雷格斯列表的创始人是谁？
      中间答案：克雷格斯列表的创始人是克雷格·纽马克。
      后续问题：克雷格·纽马克是什么时候出生的？
      中间答案：克雷格·纽马克于1952年12月6日出生。
      所以最终答案是：1952年12月6日
      """,
  },
  {
    "question": "乔治·华盛顿的外祖父是谁？",
    "answer":
      """
      是否需要后续问题：是的。
      后续问题：乔治·华盛顿的母亲是谁？
      中间答案：乔治·华盛顿的母亲是玛丽·波尔·华盛顿。
      后续问题：玛丽·波尔·华盛顿的父亲是谁？
      中间答案：玛丽·波尔·华盛顿的父亲是约瑟夫·波尔。
      所以最终答案是：约瑟夫·波尔
      """,
  },
  {
    "question": "《大白鲨》和《皇家赌场》的导演都来自同一个国家吗？",
    "answer":
      """
      是否需要后续问题：是的。
      后续问题：《大白鲨》的导演是谁？
      中间答案：《大白鲨》的导演是史蒂文·斯皮尔伯格。
      后续问题：史蒂文·斯皮尔伯格来自哪个国家？
      中间答案：美国。
      后续问题：《皇家赌场》的导演是谁？
      中间答案：《皇家赌场》的导演是马丁·坎贝尔。
      后续问题：马丁·坎贝尔来自哪个国家？
      中间答案：新西兰。
      所以最终答案是：不是
      """,
  },
]

example_selector = SemanticSimilarityExampleSelector.from_examples(
  # 这是可供选择的示例列表。
  examples,
  # 这是用于生成嵌入的嵌入类，该嵌入用于衡量语义相似性。
  embeddings,
  # 这是用于存储嵌入和执行相似性搜索的VectorStore类。
  Chroma,
  # 这是要生成的示例数。
  k=2
)

question = "乔治·华盛顿的父亲是谁？"
selected_examples = example_selector.select_examples({"question": question})
print(f"最相似的示例：{question}")
print('----')
for example in selected_examples:
  for k, v in example.items():
    print(f"{k}: {v}")

print('====')
example_prompt = PromptTemplate(
  input_variables=["question", "answer"],
  template="问题: {question}\n{answer}",
)

prompt = FewShotPromptTemplate(
  example_selector=example_selector,
  example_prompt=example_prompt,
  suffix="问题：{input}",
  input_variables=["input"],
)

print(prompt.format(input=question))