import asyncio
import json
import re
import threading
import websockets
from UI import App, Frame1
import pyautogui as pa




com = re.compile(r"[^A-J0-9]*?([A-Z].*?[1-9][0-9]?)[^A-J0-9]*?([A-Z].*?[1-9][0-9]?)")


def get_command(sting):
    result = com.match(sting.upper())
    if result:
        for r in result.groups():
            widget = Frame1.data_position.get(r)
            if widget:
                x = widget.winfo_rootx() + widget.winfo_width() / 2
                y = widget.winfo_rooty() + widget.winfo_height() / 2
                pa.click(x, y, 1)


def main(loop, url):
    asyncio.set_event_loop(loop)

    async def work():
        websocket = await websockets.connect("ws://localhost:8080/ws/s/")
        await websocket.send(json.dumps({'command': url}))
        while True:
            msg = await websocket.recv()
            danmu = [*json.loads(msg).values()][0]
            print(danmu)
            get_command(danmu)

    future = asyncio.gather(work())
    loop.run_until_complete(future)

s = 'https://live.bilibili.com/734?popular_rank=1&visit_id=2wz6k8zwtt80https://live.bilibili.com/734?popular_rank=1&visit_id=2wz6k8zwtt80'
com=re.compile(f'(https?://.*?/\d+).*?(https?://.*?/\d+)')
g = com.match(s)
v = g.groups()
c = len(v)
a = v[0].__eq__(v[1])
# 要抓取弹幕的直播间地址
url = 'https://live.bilibili.com/734'
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    threading.Thread(target=main, args=(loop, url)).start()
    app = App()
    app.run()

# https://www.douyu.com/85894
# https://live.bilibili.com/734
# 'https://live.bilibili.com/27084791'