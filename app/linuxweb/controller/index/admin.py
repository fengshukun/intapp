from app.linuxweb.common import *
table='admin'
def get(id=0):
    "获取列表"
    if id:
        return returnjson(sqlite(table).field('id,icon,username,phone,nickname,name,logintime,addtime').find(id))
    where=None
    kw=request.args.get('kw')
    pagenow=request.args.get('pagenow')
    pagesize=request.args.get('pagesize')
    if kw:
        where=[("username","like","%"+str(kw)),'or',("name","like","%"+str(kw)),'or',("nickname","like","%"+str(kw)),'or',("phone","like","%"+str(kw))]
    if not pagenow:
        pagenow=1
    else:
        pagenow=int(pagenow)
    if not pagesize:
        pagesize=10
    else:
        pagesize=int(pagesize)
    lists=sqlite(table).where(where).page(pagenow,pagesize).select()
    count=sqlite(table).where(where).count()
    data=get_json_list(lists,count,pagenow,pagesize)
    return returnjson(data)
def add():
    "添加内容"
    try:
        data=request.get_json()
        data.update(logintime=times(),addtime=times())
        # print(data)
        sqlite(table).insert(data)
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()
def delete():
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
        data.pop('logintime')
        data.pop('addtime')
        data.pop('password')
    except:pass
    else:
        sqlite(table).where("id",id).update(data)
    return returnjson()


def setpwd():
    "设置管理员登录密码"
    
    data=request.get_json()
    # print(data)
    try:
        sqlite(table).where("id",data['id']).update({'password':data['password']})
    except:
        return returnjson(code=-1,msg="设置失败")
    else:
        return returnjson()