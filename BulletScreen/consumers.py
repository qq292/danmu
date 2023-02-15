import json
import queue
import re
import threading
from pprint import pprint

from asgiref.sync import async_to_sync, sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer
import asyncio
from BulletScreen.real_url.danmu import danmaku
from channels.layers import get_channel_layer
from concurrent.futures import ThreadPoolExecutor

loop = ThreadPoolExecutor(max_workers=20)


def Work(ep, ul):
    asyncio.set_event_loop(ep)

    async def printer(q):
        try:
            while True:
                # print(f'线程: {len(threading.enumerate())}')
                if BulletScreenConsumer.isStop:
                    BulletScreenConsumer.dmc.stop()
                    BulletScreenConsumer.data.queue.clear()
                    raise ValueError('_')
                m = await q.get()
                if m['msg_type'] == 'danmaku':
                    BulletScreenConsumer.data.put(json.dumps({m["name"]: m['content']}))

        except ValueError:
            BulletScreenConsumer.event_loop.shutdown_asyncgens()
            BulletScreenConsumer.workThread = loop.submit(Work, BulletScreenConsumer.event_loop,
                                                          BulletScreenConsumer.url)

        except Exception as e:
            print(e.args)

    async def work():
        BulletScreenConsumer.isStop = False
        q = asyncio.Queue()
        BulletScreenConsumer.dmc = danmaku.DanmakuClient(ul, q)
        asyncio.create_task((printer(q)))
        await BulletScreenConsumer.dmc.start()

    future = asyncio.gather(work())
    ep.run_until_complete(future)


q = queue.Queue()


class BulletScreenConsumer(WebsocketConsumer):
    users = []
    workThread = None
    workThreadSend = None
    dmc = None
    data = q
    isStop = False
    url = ''
    event_loop = None
    com = re.compile(f'(https?://.*?/\d+).*?(https?://.*?/\d+)')

    def connect(self):
        BulletScreenConsumer.users.append(self)
        self.accept()

    def disconnect(self, close_code):
        self.close()
        BulletScreenConsumer.users.remove(self)
        raise StopConsumer()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'command' in text_data_json:
            _url = text_data_json['command']
            result = BulletScreenConsumer.com.match(_url + BulletScreenConsumer.url)
            if result:
                g = result.groups()
                if g[0].__eq__(g[1]):
                    print('self.channel_name:  ' + self.channel_name)
                    return

            BulletScreenConsumer.url = _url
            if BulletScreenConsumer.workThread:
                BulletScreenConsumer.isStop = True
            else:
                BulletScreenConsumer.event_loop = asyncio.new_event_loop()
                BulletScreenConsumer.workThread = loop.submit(Work, BulletScreenConsumer.event_loop,
                                                              BulletScreenConsumer.url)

        try:
            if BulletScreenConsumer.workThreadSend is None or BulletScreenConsumer.workThreadSend.done():
                BulletScreenConsumer.workThreadSend = loop.submit(BulletScreenConsumer.sends)
        except Exception as e:
            print(e.args)

    @staticmethod
    def sends():
        while True:
            if BulletScreenConsumer.data:
                data = BulletScreenConsumer.data.get()
                for i in range(len(BulletScreenConsumer.users)):
                    users = BulletScreenConsumer.users[i]
                    users.send(text_data=data)

# url = 'https://live.bilibili.com/734'
# url = 'https://www.douyu.com/85894'
