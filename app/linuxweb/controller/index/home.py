# -*- coding: utf-8 -*-
from app.linuxweb.common import *
import base64,psutil
def index():
    # send_websocket(data={"nickname": "kcw-linux控制板", "icon": "", "text": "输入内容..."})
    send_websocket(data={"nickname":"系统","icon":"http://img.kwebapp.cn/icon/git.png","text":"git pull执行成功，返回结果是：“已经是最新的”","code":1})
    # file_set_content("/etc/letsencrypt/live/test5.kwebapp.cn/bind","fewagfewa\nwadqDQ\n")
    # sqlite('').execute('DROP TABLE task')
    # sqlite('terminal').insert({"icon":'',"title":"我的的测试服务器","describes":"测试服务器","defaults":1,"host":"212.129.149.238",
    # "port":"22","user":"root","password":"Sk7485866","bgcolor":"#4D4D4D","addtime":times(),"updtime":times()})
    return returnjson({"desc":"我是在view目录项目新建的一个接口版本","name":"/api/index/index"})
def sendwebsocket(types="sent_all",clientid=""):
    "发送websocket异步消息"
    data=request.get_json() #{"nickname": "kcw-linux控制板", "icon": "http://127.0.0.1:9501/images/icon/linux.gif", "text": "输入内容..."}
    if send_websocket(data=data,types=types,clientid=clientid):
        return returnjson()
    else:
        returnjson(code=1,msg="发送失败")
def home():
    sysinfo=get_sysinfo()
    rundate=times()-int(sysinfo['start_time'])
    if rundate < 60:
        rundate=str(rundate)+"秒"
    elif rundate < 60*60:
        rundate=str(int(rundate/60))+"分钟"+str(int(rundate%60))+"秒"
    elif rundate < 60*60*24:
        m=int(rundate%(60*60))
        if m < 60:
            rundate=str(int(rundate/(60*60)))+"小时"+str(m)+"秒"
        elif m <60*60:
            rundate=str(int(rundate/(60*60)))+"小时"+str(int(m/60))+"分"+str(int(m%60))+"秒"
    else:
        m=int(rundate%(60*60*24))
        if m < 60:
            rundate=str(int(rundate/(60*60*24)))+"天"+str(m)+"秒"
        elif m < 60*60:
            rundate=str(int(rundate/(60*60*24)))+"天"+str(int(m/60))+"分"+str(int(m%60))+"秒"
        elif m < 60*60*24:
            xs=int(m/3600)
            mm=int(m%3600)
            if mm < 60:
                rundate=str(int(rundate/(60*60*24)))+"天"+str(xs)+"小时"+str(mm)+"秒"
            else:
                rundate=str(int(rundate/(60*60*24)))+"天"+str(xs)+"小时"+str(int(mm/60))+"分"+str(int(mm%60))+"秒"
    sysinfo['rundate']=rundate
    return returnjson(sysinfo)
# def net():#网络信息
#     return returnjson(psutil.net_connections())
def disk():#磁盘分区和使用情况
    partition=[]
    disk_usage=psutil.disk_usage('/')
    # print(disk_usage)
    partition.append({
        'name':'/','type':'','count':disk_usage[0],'used':disk_usage[1],'free':disk_usage[2],'userate':disk_usage[3]
    })
    partitions=psutil.disk_partitions()
    for v in partitions:
        disk_usage=psutil.disk_usage(v[0])
        if disk_usage[0]:
            partition.append({
                'name':v[0],'type':v[2],'count':disk_usage[0],'used':disk_usage[1],'free':disk_usage[2],'userate':disk_usage[3]
            })
    return returnjson({
        'partitions':partition, #磁盘分区和使用情况
        'io':psutil.disk_io_counters()
    })
def cpume():#cpu和内存信息
    # time.sleep(59)
    info={}
    info['cpu']={
        'count':psutil.cpu_count(),
        'time':psutil.cpu_times().user,
        'use':psutil.cpu_percent() #cpu使用率
    }
    physics=psutil.virtual_memory() #物理内存
    swap=psutil.swap_memory()  #交换内存
    # print(swap)
    info['memory']={
        'physics':{               #物理内存
            'count':physics.total,   #'内存大小'
            'available':physics.available,#可用
            'used':physics.used,   #已用
            'userate':physics.percent   #使用率
        },
        'swap':{
            'count':swap.total,
            'available':swap.free,
            'used':swap.used,   #已用
            'userate':swap.percent
        },
    }
    net=psutil.net_io_counters()
    info['net']={
        'bytes_sent':net.bytes_sent,
        'bytes_recv':net.bytes_recv,
        'packets_sent':net.packets_sent,
        'packets_recv':net.packets_recv
    }
    return returnjson(info)
def shell():
    data=request.get_json()
    os.system(data['shell'])
    return returnjson()
def process():
    "进程列表"
    lists=[]
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            lists.append(pinfo)
    return returnjson(lists)
def menu():
    "菜单列表"
    ar=sqlite('terminal').where("defaults",1).find()
    if not ar:
        ar=config.ssh
    password=(base64.b64encode(ar['password'].encode('utf-8')).decode('utf-8'))
    # print(config.ssh['url'])
    data={
        #默认终端信息
        'terminal':{
            'title':ar['user']+" "+ar['host']+":"+ar['port'],
            'url':config.ssh['url']+'?hostname='+ar['host']+'&port='+ar['port']+'&username='+ar['user']+'&password='+password+'#bgcolor='+ar['bgcolor']
        },
        'userinfo':G.userinfo,
        'header':[
            {'title':'收藏夹','icon':config.static['img']+'/icon/favorites.png','url':'','level':[
                {'title':'智连代理','icon':config.static['img']+'/icon/other.png','url':'http://www.zhilianhttp.com/Users/index.html','level':''},
                {'title':'云打码平台','icon':config.static['img']+'/icon/other.png','url':'http://www.yundama.com/','level':''},
                {'title':'字体图标库','icon':config.static['img']+'/icon/spark.png','url':'http://www.fontawesome.com.cn/faicons/','level':''},
            ]},
            {'title':'文档','icon':config.static['img']+'/icon/doc.png','url':'/index/index/doc/list','level':''},
            {'title':'request','icon':config.static['img']+'/icon/request.png','url':'/index/index/index/request','level':''}
        ],
        'leftlist':[ #左侧菜单列表
            {'title':'首页','icon':config.static['img']+'/icon/home.png','url':'/index/index/index/home','level':''},
            {'title':'应用','icon':config.static['img']+'/icon/app.png','url':'','level':[
                {'title':'网站','icon':config.static['img']+'/icon/web.png','url':'/app/index/web','level':''},
            ]},
            {'title':'管理员','icon':config.static['img']+'/icon/admin.png','url':'/index/index/index/admin','level':''},
            {'title':'软件管理','icon':config.static['img']+'/icon/software.png','url':'/software/index','level':''},
            {'title':'任务队列','icon':config.static['img']+'/icon/task.png','url':'/software/index/index/task/1','level':''},
            {'title':'web终端','icon':config.static['img']+'/icon/terminal.png','url':'/index/index/index/terminal','level':''},
            {'title':'计划任务','icon':config.static['img']+'/icon/plan.png','url':'/index/index/index/plan','level':''},
            # {'title':'系统进程','icon':config.static['img']+'/icon/process.png','url':'/index/index/index/process','level':''},
            {'title':'系统设置','icon':config.static['img']+'/icon/setup.png','url':'/index/index/index/setup','level':''},
            # {'title':'收藏夹','icon':config.static['img']+'/icon/favorites.png','url':'','level':[
            #     {'title':'字体图标库','icon':config.static['img']+'/icon/spark.png','url':'http://www.fontawesome.com.cn/faicons/','level':''},
            #     {'title':'百度翻译','icon':config.static['img']+'/icon/spark.png','url':'https://fanyi.baidu.com/?aldtype=16047#auto/zh','level':''},
            #     {'title':'Vue.js 教程','icon':config.static['img']+'/icon/vue.png','url':'https://www.runoob.com/vue2/vue-class-style.html','level':''},
            # ]},
        ]
    }
    if sqlite('software',config.software).where([('title','like',"%kodexplorer%"),'and',('status','gt',3),'and',('platform','eq',get_sysinfo()['uname'][0])]).count():
        a=sqlite('app_web',config.sqliteweb).where('title','eq',"kodexplorer").find()
        if a:
            ttt1=a['domain'].split("\n")
            data['header'].insert(0,{'title':'资源管理器','icon':config.static['img']+'/icon/kodexplorer.png','url':'http://'+ttt1[0]+":"+a['port'],'level':''})
    if sqlite('software',config.software).where([('title','like',"%phpmyadmin%"),'and',('status','gt',3),'and',('platform','eq',get_sysinfo()['uname'][0])]).count():
        a=sqlite('app_web',config.sqliteweb).where('title','eq',"phpmyadmin").find()
        if a:
            ttt1=a['domain'].split("\n")
            data['header'].insert(0,{'title':'mysql数据库管理','icon':config.static['img']+'/icon/phpmyadmin.png','url':'http://'+ttt1[0]+":"+a['port'],'level':''})
    data['websocket']={
        "host":globals.HEADER.HTTP_HOST.split(":")[0],
        "port":config.websoeket['port'],
        "authkey":config.websoeket['authkey'],
    }
    return returnjson(data)
def getinfo():
    "获取系统信息"
    data=get_sysinfo()
    paths=os.path.abspath('.')
    paths=paths.replace("\\", "/")
    data['path']=paths
    data['configpath']=config.path
    return returnjson(data)
def select(table):
    "通用查询select"
    data=request.get_json()
    try:
        where=data['where']
    except:
        where=None
    try:
        field=data['field']
    except:
        field='*'
    return returnjson(sqlite(table).where(where).field(field).select())
def selectpage(table):
    "通用查询select"
    data=request.get_json()
    try:
        where=data['where']
    except:
        where=None
    try:
        field=data['field']
    except:
        field='*'
    pagenow=request.args.get('pagenow')
    pagesize=request.args.get('pagesize')
    if not pagenow:
        pagenow=1
    else:
        pagenow=int(pagenow)
    if not pagesize:
        pagesize=10
    else:
        pagesize=int(pagesize)
    lists=sqlite(table).field(field).where(where).page(pagenow,pagesize).select()
    count=sqlite(table).where(where).count()
    data=get_json_list(lists,count,pagenow,pagesize)
    return returnjson(data)
def add(table):
    "添加内容"
    try:
        data=request.get_json()
        try:
            data.update(updtime=times(),addtime=times())
        except:pass
        sqlite(table).insert(data)
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()
def delete(table):
    "批量删除"
    try:
        id=request.get_json()
        sqlite(table).where('id','in',id).delete()
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()
def put(id=0):
    "更新内容"
    data=request.get_json()
    if not id:
        id=data['id']
    try:
        data.pop('updtime')
    except:pass
    else:
        sqlite(table).where("id",id).update(data)
    return returnjson()