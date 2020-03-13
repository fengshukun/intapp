# -*- coding: utf-8 -*-
from .intappwebsocketsclient import *
G=globals.G
g_local_ip=''
def get_local_ip():
    "获取内网ip"
    global g_local_ip
    if g_local_ip:
        return g_local_ip
    try:
        socket_objs = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
        ip_from_ip_port = [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in socket_objs][0][1]
        ip_from_host_name = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1]
        g_local_ip = [l for l in (ip_from_ip_port, ip_from_host_name) if l][0]
    except (Exception) as e:
        print("get_local_ip found exception : %s" % e)
    return g_local_ip if("" != g_local_ip and None != g_local_ip) else socket.gethostbyname(socket.gethostname())
    
global globalqueue
globalqueue = Queue()
def messagequeue():
    while True:
        if not globalqueue.empty():
            # print("执行队列")
            value=globalqueue.get()
            if value['args']:
                try:
                    sqlite('task').where("key = '"+value['task']['key']+"' and code!=4").update({"code":3,"res":"正在执行"})
                    value['target'](*value['args'])
                except:
                    sqlite('task').where("key = '"+value['task']['key']+"' and code!=4").update({"code":1,"res":"失败"})
            else:
                try:
                    value['target']()
                except:
                    sqlite('task').where("key = '"+value['task']['key']+"' and code!=4").update({"code":1,"res":"失败"})
            sqlite('task').where("key = '"+value['task']['key']+"' and code!=4").update({"code":4,"res":"执行完成"})
        else:
            time.sleep(1)
def add_queue(target,args=None,title="默认任务",describes=""):
    """添加队列
    
    target 方法名  必须

    args 方法参数 非必须  如

    title 任务名称

    descs 任务描述

    msg 任务执行结果
    使用方式如：add_queue(target=aa,args=(1,))
    """
    ttt=times()
    task={"title":title,"describes":describes,"code":2,"key":md5(str(ttt)+str(random.randint(100000,999999))),"res":"","addtime":ttt}
    sqlite('task').insert(task)
    key={"target":target,"args":args,"task":task}
    globalqueue.put(key)
def get_process_id(name):
    try:
        child = subprocess.Popen(['pgrep', '-f', name],stdout=subprocess.PIPE, shell=False)
        response = child.communicate()[0]
        return [int(pid) for pid in response.split()]
    except:
        return []
def is_url(url):
    "判断url合法性"
    if re.match(r'^https?:/{2}\w.+$', url):
        return True
    else:
        return False
def returnjson(data=[],code=0,msg="成功",status='200 ok'):
    """在浏览器输出包装过的json

        参数 data 结果 默认[]

        参数 code body状态码 默认0

        参数 msg body状态描述 默认 成功

        参数 status http状态码 默认 200

        返回 json字符串结果集 
        """
    res={
        "code":code,
        "msg":msg,
        "time":times(),
        "data":data
    }
    return json_encode(res),status,{"Content-Type":"application/json; charset=utf-8"}
def file_get_content(k):
    "获取文件内容"
    if os.path.isfile(k):
        f=open(k,'r',encoding="utf-8")
        con=f.read()
        f.close()
    else:
        con=''
    return con
def file_set_content(k,data):
    f=open(k,'w',encoding="utf-8")
    f.write(data)
    f.close()
    return True
def randoms(lens=6,types=1):
    """生成随机字符串
    
    lens 长度

    types 1数字 2字母 3字母加数字
    """
    strs="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,!@#$%^&*()_+=-;',./:<>?"
    if types==1:
        strs="0123456789"
    elif types==2:
        strs="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    elif types==3:
        strs="0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    k=''
    i=0
    while i < lens:
        k+=random.choice(strs)
        i+=1
    return k