from flask import Flask, request, make_response
import asyncio
import requests

app = Flask(__name__)

@app.route("/yes", methods=['GET'])
def hello():
    # return make_response("Hello, World!",200)
    return "Hello, World!"

@app.route("/async")
async def hello_async():
    # task = asyncio.create_task(otr())
    # ret = await task
    # print(ret)
    print("A")
    for i in range(500000):
        print(i)
    # return ret

    await asyncio.sleep(1)
    print("B1")
    return make_response("okyies", 200)
    # await asyncio.sleep(1)
    # return "Hello, Async World!"

# @app.route("/async")
def otr():
    print("1")
    print("2")
    # print("dsaa",{220: "oky"})
    # response = requests.get('http://127.0.0.1:5000/async')
    # return int(220)
    # response = 200
    # response.status_code = 200
    return {220:'ok'}
    # return make_response("ok", 220)

async def sync_otr():
    return await asyncio.to_thread(otr)



@app.route("/async123")
async def mainw():
    # status_code, _ = await asyncio.gather(
    #      sync_otr(),hello_async()
    # )
    # print(f"Got HTTP response with status {status_code}.")
    t1 = asyncio.create_task(hello_async())
    # t2 = asyncio.create_task(sync_otr())
    # t3 = asyncio.create_task(otr1('Ankit'))
    # t4 = asyncio.create_task(otr1('Ankit123'))
    # print("await t1",await t1)

    t2 = await sync_otr()
    print(t2)
    await t1
    # await t2
    # t1 = await hello_async()
    # t2 = await otr()
    # if '{200' in await hello_async() or '{200' in otr():
        # print("its there")
    # print("here",t1)

    # await t3
    # await t4
    # var =await asyncio.gather(hello_async(),otr())
    # print("var",var)
    # vart = t1
    # return vart
    return make_response("var",200)


async def otr1(name):
    print("1", name)
    await asyncio.sleep(0.01)
    print("2", name)
    return await {220: "oky"}
if __name__ == "__main__":
    app.run()
