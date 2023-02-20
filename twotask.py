from flask import Flask

import asyncio

app = Flask(__name__)

async def task_1():
    # await asyncio.sleep(1)
    for i in range(100000):
        print(i)
    # await asyncio.sleep(1)
    return "Task 1 completed"

async def task_2():
    #
    for i in range(1000):
        print("hii")
    # await asyncio.sleep(2)
    return "Task 2 completed"

@app.route('/async')
async def index():
    results = await asyncio.gather(task_1(), task_2())
    for t in results:
        print("yesss", t)
    return f"Results: {results}"

if __name__ == '__main__':
    app.run()
