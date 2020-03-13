from .plantask import *
from . import websocket_client 
global globalqueuesssss
globalqueuesssss = Queue()
# websocketbojc=websocketbojclie()
# websocketbojc.start()
class websocketbojclie():
    websocketbojclient=None
    def websocket_client_recv(self):
        while True:
            try:
                result=self.websocketbojclient.recv()
            except:
                time.sleep(1)
            else:
                print(result)
    def send(self,data):
        try:
            self.websocketbojclient.send(data)
        except:
            self.websocketbojclient=None
            self.start(data)
            return False
        else:
            return True
    def start(self,data):
        if not self.websocketbojclient:
            self.websocketbojclient=websocket_client.create_connection("ws://127.0.0.1:"+str(config.websoeket['port'])+"/websocket")
            self.websocketbojclient.send(json_encode({"authkey":config.websoeket['authkey'],"nickname":"系统"})) #发送签权消息
            result =  self.websocketbojclient.recv()
            print("Received '%s'" % result)
            t=threading.Thread(target=self.websocket_client_recv)
            t.daemon=True
            t.start()
        return self.send(data)
   

def send_websocket(types="sent_all",data="",clientid=""):
    """发送websocket消息

    types sent_all给所有人发送 sent_client给定客户端发送

    data 要发送的内容

    clientid 指定客户端id
    """
    websocketbojc=websocketbojclie()
    key={
        "types":types,"data":data,"clientid":clientid
    }
    # # print(key) 
    # intappwebsocketsclientqueue.put(key)
    return websocketbojc.start(json_encode(key))