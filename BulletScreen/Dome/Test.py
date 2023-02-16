import asyncio
import json
import sys

import websockets


async def test():
    try:
        async with websockets.connect("ws://localhost:8080/ws/s/") as websocket:
            await websocket.send(json.dumps({'command': sys.argv[1].strip()}))
            print("\n [弹幕获取中... ]\n\n")
            while True:
                msg = await websocket.recv()
                print(msg.encode('utf-8').decode("unicode_escape"))
    except ConnectionRefusedError as __:
        print("\n连接服务器错误,检查是否启动服务器!(运行目录下单run.bat,不要关掉窗口)\n")
    except Exception as e:
        print(e.args)

if len(sys.argv) > 1:
    asyncio.run(test())
else:
    print("\n最少需要一个参数\n")
    quit()



