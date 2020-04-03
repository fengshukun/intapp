#!/usr/bin/env python3.6intapp
import sys,asyncio,websockets
sys.path.append("../../")
from app.linuxweb.common import *
class kwebsocket():
    "websocket服务端"
    clientlists=[] #所有客户端绑定的对象
    lists=[] #所有客户端
    clientuser=[] #所有客户端绑定的用户
    authkey=config.websoeket['authkey']
    def returnjson(self,data='',code=0,msg='成功'):
        res={
            "code":code,
            "msg":msg,
            "time":times(),
            "data":data
        }
        return json_encode(res)
    async def sent_all(self,clientid,text):
        "给所有人发送消息，不包括自己"
        for l in self.clientlists:
            try:
                if clientid not in l['clientid']:
                    await l['socket'].send(text)
            except:pass
    async def sent_client(self,clientid,text):
        "给所指定客户端发送消息"
        xb=self.lists.index(clientid)
        websockets=self.clientlists[xb]['socket']
        try:
            await websockets.send(text)
        except:pass
    async def main(self,websocket, path):
        "服务器端主逻辑"
        auth={"authkey":""}
        try:
            recv_text = await websocket.recv() #接收客户端的消息
            auth=json_decode(recv_text)
        except:
            try:
                await websocket.send(self.returnjson(code=1,msg="签权错误"))
            except:
                print("接收错误",traceback.format_exc())
        else:
            if is_index(auth,"authkey") and self.authkey==auth['authkey']:
                clientid=md5(randoms(8))
                authdata={
                    "clientuser":self.clientuser
                }
                uid=''
                icon=''
                nickname=''
                try:
                    uid=auth['uid']
                except:pass
                try:
                    icon=auth['icon']
                except:pass
                try:
                    nickname=auth['nickname']
                except:pass
                await websocket.send(self.returnjson(authdata,code=0,msg="签权成功"))
                userinfo={"clientid":clientid,"uid":uid,"icon":icon,"nickname":nickname}
                self.clientlists.append({"clientid":clientid,"socket":websocket})
                self.clientuser.append(userinfo)
                self.lists.append(clientid)
                await self.sent_all(clientid,self.returnjson({"userinfo":userinfo})) #发送给其他所有人
                while True:
                    try:
                        recv_text = await websocket.recv() #接收客户端的消息
                        # print(recv_text)
                    except Exception as e:#客户端关闭链接后
                        # if '1001' in str(e):
                        # print("关闭连接",traceback.format_exc())
                        xb=self.lists.index(clientid)
                        del self.lists[xb]
                        del self.clientlists[xb]
                        del self.clientuser[xb]
                        break
                    else:
                        try:
                            res=json_decode(recv_text)
                            if isinstance(res,dict):
                                # res={"types":"sent_client","data":"","clientid":""}
                                # res={"types":"sent_all","data":""}
                                # res={"types":"get_clientlist"}
                                if is_index(res,"types"):
                                    if res['types']=='sent_client': #给指定用户发送
                                        if is_index(res,"clientid"):
                                            await self.sent_client(res['clientid'],self.returnjson(res['data']))
                                        else:
                                            await self.sent_client(clientid,self.returnjson(code=1,msg="你需要指定clientid"))
                                    elif res['types']=='sent_all': #给所有用户发送
                                        await self.sent_all(clientid,self.returnjson(res['data']))
                                    elif res['types']=='get_clientlist': #获取在线用户
                                        await websocket.send(self.returnjson(self.clientuser))
                                    else:
                                        await self.sent_client(clientid,self.returnjson(code=1,msg="无法匹配types"))
                                else:
                                    await self.sent_client(clientid,self.returnjson(code=1,msg="发送发送的数据格式错误或不完整"))
                            else:
                                await self.sent_client(clientid,self.returnjson(code=1,msg="必须发送json格式的文本")) #给当前用户发送消息
                        except:
                            # print("解析错误",traceback.format_exc())
                            await self.sent_client(clientid,self.returnjson(clientid,code=1,msg="解析错误")) #给当前用户发送消息
            else:
                await websocket.send(self.returnjson(code=1,msg="签权失败"))
    def start(self):
        "启动websoeket服务"
        start_server = websockets.serve(self.main, config.websoeket['ip'], config.websoeket['port'])
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
kwebsocket=kwebsocket()
kwebsocket.start()