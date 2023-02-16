##  弹幕 **开箱即用,不需要再安装python环境**
`运行项目目录下的run.bat运行django开发服务器,test.bat是一个使用示例`
## 引用了 <https://github.com/wbt5/real-url/>
## 连接到服务器后,向服务器发送{"command":直播间url}数据,即可不断地从服务器接收到直播间的实时弹幕.
<br> 

**python**调用示例
```python

async def test():
    # 连接服务器(先启动服务器:python manage.py runserver 8080)
    async with websockets.connect("ws://localhost:8080/ws/s/") as websocket:
        # 向服务器发送数据(要监听的直播间url)
        await websocket.send(json.dumps({'command': 'https://www.douyu.com/85894'}))
        # 接收服务器返回的弹幕数据
        while True:
            msg = await websocket.recv()
            print(msg)

asyncio.run(test())



```

<br>

c#调用示例
```csharp
public async void WebSocket()
    {
        try
        {       
            if (Socket != null && Socket.State.Equals(WebSocketState.Open))
            {
                Debug.Log("不要重复连接");
                return;
            }
            Socket = new ClientWebSocket();
            ct = new CancellationToken();
            //连接服务器
            await Socket.ConnectAsync(new Uri(ServerUrl), ct);
            Debug.Log("获取弹幕中...............");
            //向服务器发送要获取弹幕的直播间url
            GetBulletScreen(LiveRoomUrl);
            //获取服务器返回的弹幕数据
            while (true)
            {
                var result = new byte[10240];
                await Socket.ReceiveAsync(new ArraySegment<byte>(result), ct);
                string msg = Encoding.UTF8.GetString(result, 0, result.Length);
                unityEvent?.Invoke(msg);
            }
        }
        catch (Exception e)
        {
            Debug.Log("连接失败!!");
        }
    }

```
<br>

##### [对我有用,资助他](https://qq292.github.io://qq292.github.io/)








