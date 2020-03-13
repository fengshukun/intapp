from app.linuxweb.common import *
def intapp():
    data=request.get_json()
    if data:
        for k in data:
            sqlite('conf').where('id',k['id']).update({'value':k['value']})
        return returnjson()
    else:
        ar=sqlite('conf').where('type','intapp').select()
        return returnjson(ar)
def start(id=0):
    if id:
        sqlite('start_command').where('id',id).delete()
    else:
        data=request.get_json()
        data['addtime']=times()
        data['status']=0
        sqlite('start_command').insert(data)
    return returnjson()
def get_start():
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
    lists=sqlite('start_command').page(pagenow,pagesize).select()
    count=sqlite('start_command').count()
    data=get_json_list(lists,count,pagenow,pagesize)
    return returnjson(data)

def get_swap():
    ar=sqlite('conf').where("type = 'system' and title='swap内存'").find()
    return returnjson(ar)
def set_swap(size=1024,types='init'):
    sqlite('start_command').where('title','swap内存启动').delete()
    if types=='init':
        '初始化swap内存'
        os.system("swapoff /root/swapfile && rm -f /root/swapfile") #关闭
        os.system("dd if=/dev/zero of=/root/swapfile bs=1M count="+str(size)+" && mkswap /root/swapfile && swapon /root/swapfile") #启用
        sqlite('conf').where("type = 'system' and title='swap内存'").update({'value':size})
    elif types=='start':
        os.system("dd if=/dev/zero of=/root/swapfile bs=1M count="+str(size)+" && mkswap /root/swapfile && swapon /root/swapfile") #启用
        sqlite('conf').where("type = 'system' and title='swap内存'").update({'value':size})
    else:
        os.system("swapoff /root/swapfile && rm -f /root/swapfile") #关闭
    sqlite('start_command').insert({'title':'swap内存启动','describes':'系统创建,请务删除','status':0,'command':'swapon /root/swapfile','addtime':times()})
    return returnjson()

def firewallstatus(k='1'):
    "防火墙开关"
    k=int(k)
    sqlite('start_command').where('title','启动防火墙').delete()
    if k:
        os.system("systemctl start firewalld.service")  #启动防火墙
        file_set_content('firewallstatus','1')
        sqlite('start_command').insert({'title':'启动防火墙','describes':'系统创建,请务删除','status':0,'command':'systemctl start firewalld.service','addtime':times()})
    else:
        os.system("systemctl stop firewalld.service")  #关闭防火墙
        file_set_content('firewallstatus','0')
    return returnjson()
def firewall(id=0):
    "添加/删除 放行的防火墙"
    data=request.get_json()
    if id: #删除 放行的防火墙端口
        os.system("firewall-cmd --zone=public --remove-port="+str(data['port'])+"/tcp --permanent && systemctl restart firewalld.service")
        #firewall-cmd --zone=public --remove-port=80/tcp --permanent && systemctl restart firewalld.service  删除
        sqlite('firewall').where('id',id).delete()
    else: #添加 放行的防火墙端口
        os.system("firewall-cmd --zone=public --add-port="+str(data['port'])+"/tcp --permanent && firewall-cmd --reload")
        #firewall-cmd --zone=public --add-port=80/tcp --permanent && firewall-cmd --reload  增加
        sqlite('firewall').insert({'port':data['port'],'describes':data['describes'],'addtime':times()})
    return returnjson()
def get_firewall():
    "获取防火墙列表"
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
    lists=sqlite('firewall').page(pagenow,pagesize).select()
    count=sqlite('firewall').count()
    data=get_json_list(lists,count,pagenow,pagesize)
    data['firewallstatus']=file_get_content('firewallstatus')
    return returnjson(data)