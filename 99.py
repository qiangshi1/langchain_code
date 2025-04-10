#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# asyncio
import asyncio
import time

async def say_after(delay, what):
  await asyncio.sleep(delay)
  print(what)

# print("====part 1")

# # async声明一个协程函数main()
# async def main():
#   # await相当于一个标记，告诉程序这里有一个阻塞操作，可以将协程挂起并等待
#   await asyncio.sleep(1)
#   print('hello')

# asyncio.run(main())

# print("====part 2")

# async def main():
#   print(f"started at {time.strftime('%X')}")
#   await say_after(1, 'hello')
#   await say_after(2, 'world')
#   print(f"finished at {time.strftime('%X')}")

# asyncio.run(main())

# print("====part 3")

# async def main():
#   task1 = asyncio.create_task(
#     say_after(1, 'hello'))

#   task2 = asyncio.create_task(
#     say_after(2, 'world'))

#   print(f"started at {time.strftime('%X')}")

#   # Wait until both tasks are completed (should take
#   # around 2 seconds.)
#   await task1
#   await task2

#   print(f"finished at {time.strftime('%X')}")

# asyncio.run(main())


# print("====part 4")

# async def main():
#   async with asyncio.TaskGroup() as tg:
#     task1 = tg.create_task(
#       say_after(1, 'hello'))

#     task2 = tg.create_task(
#       say_after(2, 'world'))

#     print(f"started at {time.strftime('%X')}")

#   # The await is implicit when the context manager exits.

#   print(f"finished at {time.strftime('%X')}")


# asyncio.run(main())

# print("====part 5")

# async def nested():
#   return 42

# async def main():
#   # Nothing happens if we just call "nested()".
#   # A coroutine object is created but not awaited,
#   # so it *won't run at all*.
#   nested()

#   # Let's do it differently now and await it:
#   print(await nested())  # will print "42".

# asyncio.run(main())


# print("====part 6")
# async def nested():
#     return 42

# async def main():
#     # Schedule nested() to run soon concurrently
#     # with "main()".
#     task = asyncio.create_task(nested())

#     # "task" can now be used to cancel "nested()", or
#     # can simply be awaited to wait until it is complete:
#     await task

# asyncio.run(main())

# print("====part 7")
import asyncio

# 模拟一个异步事件生成器
async def event_generator(num_events):
  for i in range(num_events):
    # 模拟异步操作，比如等待 I/O 或其他耗时任务
    yield f"Event #{i}"
    await asyncio.sleep(1)

# 异步处理事件
async def process_events():
  async for event in event_generator(5):  # 生成 5 个事件
    print(f"Processing: {event}")

# 主程序
async def main():
  await process_events()

# 运行事件循环
asyncio.run(main())
