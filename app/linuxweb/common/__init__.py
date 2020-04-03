# -*- coding: utf-8 -*-
from app.common import *
#下面的方法在当前模块中有效
def check_login():
    if '127.0.0.1' not in globals.HEADER.HTTP_HOST and '192.168' not in globals.HEADER.HTTP_HOST:
        config.ssh['url']='https://'+globals.HEADER.HTTP_HOST.split(':')[0]+':4433'
    else:
        config.ssh['url']='http://'+globals.HEADER.HTTP_HOST.split(':')[0]+':39101'
    appkeyusername=request.args.get('appkeyusername')
    appkeypassword=request.args.get('appkeypassword')
    if appkeyusername and appkeypassword:
        G.userinfo=sqlite('admin').where("username = '"+str(appkeyusername)+"' and password = '"+md5('kcw'+str(appkeypassword))+"'").find()
        # return returnjson(appkeypassword,-1,msg=appkeyusername)
    else:
        G.userinfo=get_session("userinfo")
    if not G.userinfo:
        return returnjson({},-1,'签权失败')
def before_request():
    return check_login()
    # print('linuxweb模块在请求前执行，我是要在配置文件配置后才能生效哦！',G.userinfo)
def after_request():
    pass
    # print('linuxweb模块在请求后执行，我是要在配置文件配置后才能生效哦！')
    
def set_session(name,value,expire=None):
    "设置session"
    return session.set("applinuxweb"+str(name),value,expire)
def get_session(name):
    "获取session"
    return session.get("applinuxweb"+str(name))
def del_session(name):
    "删除session"
    return session.rm("applinuxweb"+str(name))
def tpl(path,**context):
    intapp=sqlite('conf').where('type','intapp').select()
    return Template("/linuxweb/tpl"+str(path),intapp=intapp,config=config,static=config.static,**context)
def get_json_list(lists,count,pagenow,pagesize):
    data={
        'count':count,
        'pagenow':pagenow,
        'pagesize':pagesize,
        'pagecount':math.ceil(count/pagesize),
        'list':lists
    }
    return data