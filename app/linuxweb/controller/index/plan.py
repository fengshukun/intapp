
# -*- coding: utf-8 -*-
from app.linuxweb.common import *
def get(id=0):
    "获取列表"
    if id:
        return returnjson(sqlite("interval").find(id))
    where=None
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
    lists=sqlite("interval").page(pagenow,pagesize).select()
    count=sqlite("interval").where(where).count()
    data=get_json_list(lists,count,pagenow,pagesize)
    return returnjson(data)
def add():
    "添加任务"
    if sqlite("interval").count() >=500:
        return returnjson(code=1,msg="您已超过系统预设最大限制")
    data=request.get_json()
    data['addtime']=times()
    if data['oss']==True:
        data['oss']=1
    else:
        data['oss']=0
    data['iden']=md5(str(times()))
    if not data['name'] or not data['value']:
        return returnjson(code=1,msg="参数不全")
    plans=plan()
    plans.plantask(data)
    sqlite("interval").insert(data)
    return returnjson()
def delpl():
    "删除计划"
    id=request.get_json()
    sqlite("interval").where('id','in',id).delete()
    return returnjson(msg="任务已删除，重启控制板后生效")
def log(iden):
    "任务日志"
    p=plan()
    return returnjson(p.log(iden))