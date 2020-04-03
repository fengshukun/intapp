# -*- coding: utf-8 -*- 
from app.linuxweb.common import *
from kcweb import web
import app as application

#生产环境运行入口
app=web(__name__,application)

#这里是初始化数据 请务修改
e37f0136aa3ffaf149b351f6a4c948e9=threading.Thread(target=messagequeue)
e37f0136aa3ffaf149b351f6a4c948e9.daemon=True
e37f0136aa3ffaf149b351f6a4c948e9.start()
if get_sysinfo()['uname'][0]=='Linux':
    config.ssh['url']='http://'+get_local_ip()+':39101'
    config.app['appmode']='produc'
    try:
        e37f0136aa3ffaf149b351f6a4c948e9splan=plan()
        e37f0136aa3ffaf149b351f6a4c948e9s=sqlite("interval").select()
        for e37f0136aa3ffaf149b351f6a4c948e9ss in e37f0136aa3ffaf149b351f6a4c948e9s:
            e37f0136aa3ffaf149b351f6a4c948e9splan.plantask(e37f0136aa3ffaf149b351f6a4c948e9ss) #添加计划任务
    except:pass
    ea2b2676c28c0db26d39331a336c6b92=sqlite('start_command').field('id,command,status').select()
    for ea2b2676c28c0db26d39331a336c6b92s in ea2b2676c28c0db26d39331a336c6b92:
        print(ea2b2676c28c0db26d39331a336c6b92s['command'])
        os.system(ea2b2676c28c0db26d39331a336c6b92s['command'])
        if not ea2b2676c28c0db26d39331a336c6b92s['status']: 
            sqlite('start_command').where('id',ea2b2676c28c0db26d39331a336c6b92s['id']).update({'status':1})
#初始化结束

#调试运行入口
if __name__ == "__main__":
    app.run("server",host="0.0.0.0",port="9501",name="python")