var p = null

function initWebpack(url) {//初始化websocket
    if ('WebSocket' in window) {
        planWebsocket = new WebSocket(url); // 通信地址
        p = planWebsocket
        planWebsocket.onopen = function (event) {
            console.log('建立连接');

        }

        planWebsocket.onmessage = function (event) {
            console.log('收到消息:' + unescape(eval("'" + event.data.toString() + "'")))
            let data = JSON.parse(event.data);
            if (data.command == "getplans") {
                var planData = data.data;//返回的数据
                console.log(planData);
            } else if (data.command == "getscenes") {
                // 其他命令
            }
        }

        planWebsocket.onclose = function (event) {
            console.log('连接关闭');
        }

        planWebsocket.onerror = function () {
            alert('websocket通信发生错误！');
        }
    } else {
        alert('该浏览器不支持websocket!');
    }
}

function send(url) {
    let sendData = {
                "command": url
            }
            p.send(JSON.stringify(sendData)); // 发送获取数据的接口
}