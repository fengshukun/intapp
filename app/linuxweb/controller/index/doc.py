from app.linuxweb.common import *
import urllib,traceback
class modeldoctext(model.model):
    "文档内容"
    # config={'type':'sqlite'}
    config={'type':'sqlite','db':config.doc['db']}
    model.dbtype.conf=config
    table="doctext"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        'doclist_id':model.dbtype.int(LEN=11,DEFAULT=0),        #文档列表id
        'types':model.dbtype.int(LEN=1,DEFAULT=0),              #0目录  1文件
        "pid":model.dbtype.int(LEN=11,DEFAULT=0),               #父级id
        "icon":model.dbtype.varchar(LEN=128,DEFAULT=''),        #图标
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #文档名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #文档描述
        "opens":model.dbtype.int(LEN=1,DEFAULT=1),              #是否展开节点
        "contents":model.dbtype.text(NULL=True),                #文档内容
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }
def before_request():
    pass

def get():
    field='id,pid,icon,title,describes,addtime,updtime,defaults'
    kw=request.args.get('kw')
    pagenow=request.args.get('pagenow')
    pagesize=request.args.get('pagesize')
    where=[("pid","eq",0)]
    if kw:
        where.append('and')
        where.append(("title","like",str(kw)+"%"))
        where.append('or')
        where.append(("describes","like",str(kw)+"%"))
    if not pagenow:
        pagenow=1
    else:
        pagenow=int(pagenow)
    if not pagesize:
        pagesize=20
    else:
        pagesize=int(pagesize)
    lists=list_to_tree(sqlite('doclist',config.doc).where(where).field(field).page(pagenow,pagesize).select(),'id','pid','level')
    count=sqlite('doclist',config.doc).where(where).count()
    data=get_json_list(lists,count,pagenow,pagesize)
    return returnjson(data)
def edition(id=0):
    "获取项目版本  项目列表id"
    try:
        data=sqlite('doclist',config.doc).where('pid',id).select()
        if not data:
            if sqlite('doclist',config.doc).where('id',id).count():
                sqlite('doclist',config.doc).insert({'pid':id,'icon':'','title':'v1','describes':'系统创建的默认版本','defaults':1,'addtime':times(),'updtime':times()})
                data=sqlite('doclist',config.doc).where('pid',id).select()
                for k in data:
                    doctext=modeldoctext()
                    doctext.table="doctext"+str(k['id'])
                    doctext.create_table()
            else:
                return returnjson(code=1,msg="id错误")
    except:
        print(traceback.print_exc())
        return returnjson(code=1,msg="失败")
    return returnjson(data)
def editionadd():
    "创建版本"
    a=check_login()
    if a :
        return a
    data=request.get_json()
    id=data['id'] #起点版本id
    y=sqlite('doclist',config.doc).where('id',id).find()
    if y:
        if sqlite('doclist',config.doc).where([('pid','eq',y['pid']),'and',('title','eq',data['title'])]).count():
            return returnjson(code=1,msg="不能创建系相同本号")
        mytimes=times()
        sqlite('doclist',config.doc).insert({'pid':y['pid'],'icon':y['icon'],'title':data['title'],'describes':data['describes'],'defaults':0,'addtime':mytimes,'updtime':mytimes}) #创建版本
        doclist_id=sqlite('doclist',config.doc).where([('pid','eq',y['pid']),'and',('title','eq',data['title']),'and',('addtime','eq',mytimes)]).field('id').find()['id']
        doctext=modeldoctext()
        doctext.table="doctext"+str(doclist_id)
        doctext.create_table()
        ar=sqlite('doctext'+str(id),config.doc).where(doclist_id,id).select()
        for k in ar:
            sqlite('doctext'+str(doclist_id),config.doc).insert({
                'doclist_id':doclist_id,
                'types':k['types'],
                'pid':k['pid'],
                'icon':k['icon'],
                'title':k['title'],
                'describes':k['describes'],
                'opens':k['opens'],
                'contents':k['contents'],
                'addtime':k['addtime'],
                'updtime':k['updtime']
            })
    return returnjson()
def editiondel(id):
    "删除版本"
    a=check_login()
    if a :
        return a
    sqlite("",config.doc).execute("DROP TABLE doctext"+str(id))  ##删除版本节点表
    sqlite('doclist',config.doc).where('id',id).delete()
    return returnjson()
def editiondef(project_id,id):
    "设置该版本为默认"
    a=check_login()
    if a :
        return a
    sqlite('doclist',config.doc).where('pid',project_id).update({'defaults':0})
    sqlite('doclist',config.doc).where('id',id).update({'defaults':1})
    return returnjson()
def tree(id,kw=''):
    "获取文档节点   版本id"
    where=[('doclist_id','eq',id)]
    if kw:
        where.append('and')
        where.append(('title','like',kw+"%"))
        # where.append('and') 
        # where.append(('types','eq',1))
    data=list_to_tree(sqlite('doctext'+str(id),config.doc).where(where).field('id,pid,icon,title,describes,opens,types').select(),'id','pid','level')
    return returnjson(data)
def treetext(doclist_id,id):
    "获取节点文本 版本doclist_id 节点id"
    return returnjson(sqlite('doctext'+doclist_id,config.doc).find(id))
def treeadd(doclist_id,pid=0):
    "添加节点  项目列表版本doclist_id,节点pid"
    a=check_login()
    if a :
        return a
    if not sqlite('doclist',config.doc).where('id',doclist_id).count():
        return returnjson(code=1,msg="doclist_id错误")
    if int(pid) > 0 and not sqlite('doctext'+doclist_id,config.doc).where('id',pid).count():
        return returnjson(code=1,msg="pid错误"+str(pid))
    data=request.get_json()
    data['pid']=pid
    data['doclist_id']=doclist_id
    data['addtime']=times()
    data['updtime']=times()
    sqlite('doctext'+doclist_id,config.doc).insert(data)
    return returnjson()
def treedel(doclist_id,id):
    "删除节点"
    a=check_login()
    if a :
        return a
    def getSubNode(id,arr=[]):
        a=sqlite("doctext"+doclist_id,config.doc).where('pid',id).field('id').select()
        for k in a:
            arr.append(k['id'])
            getSubNode(k['id'],arr)
        return arr
    arrid=getSubNode(id)
    if arrid:
        sqlite("doctext"+doclist_id,config.doc).where('pid','in',arrid).delete()
    sqlite("doctext"+doclist_id,config.doc).where('id',id).delete()
    return returnjson()
def treeupd(doclist_id):
    "编辑节点"
    a=check_login()
    if a :
        return a
    data=request.get_json()
    if 'level' in data:
        del data['level']
    data['updtime']=times()
    # if 'contents' in data:
    #     data['contents']=urllib.parse.unquote(data['contents'])
    sqlite('doctext'+doclist_id,config.doc).where('id',data['id']).update(data)
    return returnjson()
def add():
    "添加项目"
    a=check_login()
    if a :
        return a
    try:
        data=request.get_json()
        data.update(addtime=times(),updtime=times())
        sqlite('doclist',config.doc).insert(data)
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()
def upd(id=0):
    "更新项目内容"
    a=check_login()
    if a :
        return a
    data=request.get_json()
    if not id:
        id=data['id']
    try:
        data.pop('addtime')
        data.pop('level')
        data['updtime']=times()
    except:pass
    else:
        data.update(updtime=times())
        sqlite('doclist',config.doc).where("id",id).update(data)
    return returnjson()
def delete(id=0):
    "批量删除项目"
    a=check_login()
    if a :
        return a
    try:
        if not id:
            id=request.get_json()
        def getSubNode(id,arr=[]):
            a=sqlite("doclist",config.doc).where('pid','in',id).field('id').select()
            for k in a:
                arr.append(k['id'])
            return arr
        arrid1=getSubNode(id) #全部版本
        if arrid1:
            for kk in arrid1:
                sqlite('',config.doc).execute("DROP TABLE doctext"+str(kk))  ##删除版本节点表
        if arrid1:
            sqlite('doclist',config.doc).where('id','in',arrid1) #删除所有版本
        sqlite('doclist',config.doc).where('id','in',id).delete() #删除当前项目
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()