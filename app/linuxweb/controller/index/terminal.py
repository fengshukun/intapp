from app.linuxweb.common import *
import traceback
def get(id=''):
    "列表"
    if id:
        return returnjson(sqlite('terminal').find(id))
    where=None
    kw=request.args.get('kw')
    pagenow=request.args.get('pagenow')
    pagesize=request.args.get('pagesize')
    if kw:
        where=[("title","like","%"+str(kw))]
    if not pagenow:
        pagenow=1
    else:
        pagenow=int(pagenow)
    if not pagesize:
        pagesize=10
    else:
        pagesize=int(pagesize)
    lists=sqlite("terminal").where(where).page(pagenow,pagesize).select()
    count=sqlite('terminal').where(where).count()
    data=get_json_list(lists,count,pagenow,pagesize)
    return returnjson(data)
def add():
    "添加内容"
    try:
        data=request.get_json()
        data.update(addtime=times(),updtime=times())
        # print(data)
        sqlite('terminal').insert(data)
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()
def delete():
    "批量删除"
    try:
        id=request.get_json()
        sqlite('terminal').where('id','in',id).delete()
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
        data.pop('addtime')
        # data.pop('password')
    except:pass
    else:
        sqlite('terminal').where("id",id).update(data)
    return returnjson()
def setdefs(id=''):
    if id:
        sqlite('terminal').update({"defaults":0})
        sqlite('terminal').where("id",id).update({"defaults":1})
        return returnjson()
    else:
        return returnjson(code=1,msg="失败")