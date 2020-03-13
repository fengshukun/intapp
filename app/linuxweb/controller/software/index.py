from app.linuxweb.common import *
def index(html='index',id=0):
    "所有html页面"
    try:
        return tpl('/software/index/'+html+'.html',id=id)
    except Exception as e:
        err=traceback.format_exc().split(",")
        return tpl('/error.html',title="页面错误:"+str(e),content=err)
def select():
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
    return returnjson(sqlite('software',config.software).where(where).field(field).select())
def gettitle(title):
    return returnjson(sqlite('software',config.software).where("title='"+title+"' and platform='"+get_sysinfo()['uname'][0]+"' and status >=4").find())
def get(id=''):
    "软件列表"
    if id:
        return returnjson(sqlite('software',config.software).find(id))
    where=[]
    if config.app['appmode']=='produc':
        where=[('platform','eq',get_sysinfo()['uname'][0])]
    kw=request.args.get('kw')
    status=request.args.get('status')
    pagenow=request.args.get('pagenow')
    pagesize=request.args.get('pagesize')
    if kw:
        if len(where):
            where.append('and')
        where.append(("title","like",str(kw)+"%"))
    elif status:
        if len(where):
            where.append('and')
        where.append(("status","egt",status))
    # print(where)
    if not pagenow:
        pagenow=1
    else:
        pagenow=int(pagenow)
    if not pagesize:
        pagesize=10
    else:
        pagesize=int(pagesize)
    lists=sqlite("software",config.software).where(where).order("title desc").page(pagenow,pagesize).select()
    i=0
    for k in lists:
        if (k['status'] == 10) and k['platform']=='Linux':
            if 'nginx' in k['title'] :
                if not get_process_id('nginx'):
                    lists[i]['status']=4
                    sqlite("software",config.software).where('id',k['id']).update({'status':4})
                    print('nginx',get_process_id('nginx'))
            elif 'redis' in k['title']:
                if not get_process_id('redis'):
                    lists[i]['status']=4
                    sqlite("software",config.software).where('id',k['id']).update({'status':4})
                    print('redis',get_process_id('redis'))
            elif 'mysql' in k['title']:
                if not get_process_id('mysql'):
                    lists[i]['status']=4
                    sqlite("software",config.software).where('id',k['id']).update({'status':4})
                    print('mysql',get_process_id('mysql'))
            elif 'php5' in k['title'] or 'php7' in k['title']:
                if not get_process_id(k['title']):
                    lists[i]['status']=4
                    sqlite("software",config.software).where('id',k['id']).update({'status':4})
                    print(k['title'],get_process_id(k['title']))
            elif 'phpims' in k['title']:
                if not get_process_id('phpims'):
                    lists[i]['status']=4
                    sqlite("software",config.software).where('id',k['id']).update({'status':4})
        i+=1
    count=sqlite('software',config.software).where(where).count()
    data=get_json_list(lists,count,pagenow,pagesize)
    data['sysinfo']=get_sysinfo()
    data['kodexplorer']=''
    if sqlite('software',config.software).where([('title','like',"%kodexplorer%"),'and',('status','gt',3),'and',('platform','eq',get_sysinfo()['uname'][0])]).count():
        a=sqlite('app_web').where('title','eq',"kodexplorer").find()
        if a:
            ttt1=a['domain'].split("\n")
            data['kodexplorer']='http://'+ttt1[0]+":"+a['port']
    return returnjson(data)
def add():
    "添加内容"
    try:
        data=request.get_json()
        data.update(updtime=times(),addtime=times())
        # print(data)
        sqlite('software',config.software).insert(data)
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
    except:pass
    else:
        sqlite('software',config.software).where("id",id).update(data)
    return returnjson()
def delete():
    "批量删除"
    try:
        id=request.get_json()
        sqlite('software',config.software).where('id','in',id).delete()
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()
def install(id=''):
    "下载/安装/启动/停止 软件"
    id=int(id)
    ar=sqlite('software',config.software).where('id',id).find()
    if not ar:
        return returnjson(code=1,msg="id错误")
    
    if ar['status']==0:#下载软件
        if 'nginx' in ar['title']:
            ass=sqlite('software',config.software).where([('title','like','nginx%'),'and',('status','gt',0),'and',('platform','eq',get_sysinfo()['uname'][0])]).find()
            if ass:
                sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':''})
                return returnjson(ass,code=1,msg="您已安装其他nginx版本，卸载其他nginx版本后可安装此版本")
        sqlite('software',config.software).where('id',ar['id']).update({'status':1,'msg':''})
        add_queue(target=SOFT.zxdownload,args=(ar,),title="安装"+ar['title'])
        # multiprocessing.Process(target=SOFT.zxdownload,args=(ar,)).start()
    elif ar['status']==2:#安装软件
        add_queue(target=SOFT.zxinstall,args=(ar,),title="安装"+ar['title'])
        # multiprocessing.Process(target=SOFT.zxinstall,args=(ar,)).start()
        sqlite('software',config.software).where('id',ar['id']).update({'status':1,'msg':''})
        
    elif ar['status']==4:#启动软件
        # multiprocessing.Process(target=SOFT.start,args=(ar,)).start()
        sqlite('software',config.software).where('id',ar['id']).update({'status':1,'msg':''})
        SOFT.start(ar)
        # add_queue(target=SOFT.start,args=(ar,))
    elif ar['status']==10:#停止软件 
        # multiprocessing.Process(target=SOFT.stop,args=(ar,)).start()
        sqlite('software',config.software).where('id',ar['id']).update({'status':1,'msg':''})
        SOFT.stop(ar)
        # add_queue(target=SOFT.stop,args=(ar,))
    else:
        return returnjson(code=1,msg="未知状态")
    return returnjson()

def uninstall(id=''):
    "卸载软件和重启软件"
    id=int(id)
    ar=sqlite('software',config.software).where('id',id).find()
    if not ar:
        return returnjson(code=1,msg="id错误")
    sqlite('software',config.software).where('id',ar['id']).update({'status':1,'msg':''})
    if ar['status']==4:
        # add_queue(target=SOFT.uninstall,args=(ar,))
        # multiprocessing.Process(target=SOFT.uninstall,args=(ar,)).start()
        SOFT.uninstall(ar)
        return returnjson()
    if ar['status']==10:
        # multiprocessing.Process(target=SOFT.reboot,args=(ar,)).start()
        # add_queue(target=SOFT.reboot,args=(ar,))
        SOFT.reboot(ar)
        return returnjson()
    return returnjson(code=1,msg="未知状态")



def gitssh():
    'gitssh公钥'
    data=file_get_content("/root/.ssh/id_rsa.pub")
    return returnjson(data)

def task():
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
    lists=sqlite("task").page(pagenow,pagesize).order("id desc").select()
    count=sqlite('task').count()
    data=get_json_list(lists,count,pagenow,pagesize)
    return returnjson(data)