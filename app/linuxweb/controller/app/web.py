# -*- coding: utf-8 -*-
from app.linuxweb.common import *
def get():
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
    lists=sqlite("app_web").field(field).where(where).page(pagenow,pagesize).select()
    i=0
    for k in lists:
        lists[i]['domain']=k['domain'].split("\n")
        i+=1
    count=sqlite("app_web").where(where).count()
    data=get_json_list(lists,count,pagenow,pagesize)
    data['kodexplorer']=''
    if sqlite('software',config.software).where([('title','like',"%kodexplorer%"),'and',('status','gt',3),'and',('platform','eq',get_sysinfo()['uname'][0])]).count():
        a=sqlite('app_web').where('title','eq',"kodexplorer").find()
        if a:
            ttt1=a['domain'].split("\n")
            data['kodexplorer']='http://'+ttt1[0]+":"+a['port']
    return returnjson(data)
def add_web():
    "添加网站,linux和windows已完成"
    nginx=sqlite('software',config.software).where([('status','egt','4'),'and',('platform','eq',get_sysinfo()['uname'][0]),'and',('title','like','nginx%')]).find()
    if not nginx:
        return returnjson(code=1,msg='安装nginx服务器后才创建网站')
    addtime=times()
    data=request.get_json()
    # print(data['path'])
    ttt1=data['domain'].split("\n")
    where="port="+data['port']+" and (" #[('port','eq',data['port'])]
    for kk in ttt1:
        where=where+"domain like '%"+kk+"%'"+" or "
    where=where[:-4]+")"
    # print(where)
    # exit()
    data['only']=md5(str(addtime)+str(random.randint(100000,999999)))
    ttt=sqlite('app_web').where(where).find()
    # print(ttt)
    # exit()
    if ttt:
        ttt=ttt['domain'].split("\n")
        for k in ttt:
            for kk in ttt1:
                if k==kk:
                    return returnjson(code=1,msg=k+"已被使用")
    ttt=data['domain'].split("\n")
    server_name=''
    for k in ttt:
        server_name=str(server_name)+" "+str(k)
    if '5.6' in data['phpeditionath']:
        phpport=9000
    elif '7.0' in data['phpeditionath']:
        phpport=9610
    elif '7.1' in data['phpeditionath']:
        phpport=9611
    elif '7.2' in data['phpeditionath']:
        phpport=9612
    elif '7.3' in data['phpeditionath']:
        phpport=9613
    elif '7.4' in data['phpeditionath']:
        phpport=9614
    elif data['phpeditionath']=='static':
        phpport='static'
    elif data['phpeditionath']=='vue':
        phpport='vue'
    else:
        return returnjson(code=1,msg='找不到php版本')
    if nginx['platform']=='Linux':
        pass
        paths=nginx['paths']
        filenames=nginx['title']
        servertpl=paths+filenames+'/conf/vhost/webtpl/default'
        balancing=[] #负载均衡列表
        proxy_set_header=[] #自定义转发请求头列表
        text=Templates(servertpl,balancing=balancing,client_max_body_size=20,port=data['port'],
            proxy_set_header=proxy_set_header,ssl=False,
            server_name=server_name,only=data['only'],webpath=data['path'],phpport=phpport,rewrite=paths+filenames+"/conf/vhost/rewrite/"+data['only'])
        f=open(paths+filenames+"/conf/vhost/"+data['only']+'.conf','w',encoding="utf-8")
        f.write(text)
        f.close()
        f=open(paths+filenames+"/conf/vhost/rewrite/"+data['only'],'w',encoding="utf-8")
        f.write('')
        f.close()
        os.system("nginx -s reload")
    elif nginx['platform']=='Windows':
        paths=nginx['paths']
        filenames=nginx['title']
        servertpl=paths+filenames+'/conf/vhost/webtpl/default'
        balancing=[] #负载均衡列表
        proxy_set_header=[] #自定义转发请求头列表
        text=Templates(servertpl,balancing=balancing,client_max_body_size=20,port=data['port'],
            proxy_set_header=proxy_set_header,ssl=False,
            server_name=server_name,only=data['only'],webpath=data['path'],phpport=phpport,rewrite=paths+filenames+"/conf/vhost/rewrite/"+data['only'])
        f=open(paths+filenames+"/conf/vhost/"+data['only']+'.conf','w',encoding="utf-8")
        f.write(text)
        f.close()
        f=open(paths+filenames+"/conf/vhost/rewrite/"+data['only'],'w',encoding="utf-8")
        f.write('')
        f.close()
        os.system("cd "+paths+filenames+" & stop.bat")
        time.sleep(1)
        os.system("cd "+paths+filenames+" & start.bat")
        
    if not os.path.exists(data['path']):
        os.makedirs(data['path'])
        f=open(data['path']+"/index.html",'w',encoding="utf-8")
        f.write('<!DOCTYPE html><html><head><title>网站创建成功</title><meta charset=utf-8></head><body><h1 style="margin-top:100px;text-align:center">恭喜您！网站创建成功</h1></body></html>')
        f.close()
        f=open(data['path']+"/index.php",'w',encoding="utf-8")
        f.write("<?php echo '恭喜您！网站创建成功，您成功运行了php文件'; ?>")
        f.close()
        f=open(data['path']+"/403.html",'w',encoding="utf-8")
        f.write('<!DOCTYPE html><html><head><title>error</title><meta charset=utf-8></head><body><h1 style="margin-top:100px;text-align:center">103 error</h1></body></html>')
        f.close()
        f=open(data['path']+"/404.html",'w',encoding="utf-8")
        f.write('<!DOCTYPE html><html><head><title>404</title><meta charset=utf-8></head><body><h1 style="margin-top:100px;text-align:center">404 Not Found</h1></body></html>')
        f.close()
        f=open(data['path']+"/502.html",'w',encoding="utf-8")
        f.write('<!DOCTYPE html><html><head><title>502</title><meta charset=utf-8></head><body><h1 style="margin-top:100px;text-align:center">502 Not Found</h1></body></html>')
        f.close()
    try:
        try:
            data.update(updtime=addtime,addtime=addtime)
            data['servers']=paths+filenames
        except:pass
        sqlite('app_web').insert(data)
    except:
        return returnjson(code=1,msg="失败")
    else:
        return returnjson()
def del_web(id,path=0):
    #path=1 表示删除网站目录  ,linux和windows已完成
    "删除网站"
    nginx=sqlite('app_web').where('id',id).find()
    filenames=nginx['servers']
    if get_sysinfo()['uname'][0]=='Linux':
        if os.path.isfile(filenames+"/conf/vhost/"+nginx['only']+'.conf'):
            os.remove(filenames+"/conf/vhost/"+nginx['only']+'.conf')
            if os.path.isfile(filenames+"/conf/vhost/rewrite/"+nginx['only']):
                os.remove(filenames+"/conf/vhost/rewrite/"+nginx['only'])
            if os.path.isfile(filenames+"/logs/"+nginx['only']+".access.log"):
                os.remove(filenames+"/logs/"+nginx['only']+".access.log")
            if os.path.isfile(filenames+'/conf/vhost/rewrite/'+nginx['only']+".key"):
                os.remove(filenames+'/conf/vhost/rewrite/'+nginx['only']+".key")
            if os.path.isfile(filenames+'/conf/vhost/rewrite/'+nginx['only']+".pem"):
                os.remove(filenames+'/conf/vhost/rewrite/'+nginx['only']+".pem")
            pi=subprocess.Popen('nginx -s reload',shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            ars=pi.stdout.read().decode()
            ars=ars.split("\n")
            strs=ars[len(ars)-2]
    elif get_sysinfo()['uname'][0]=='Windows':
        if os.path.isfile(filenames+"/conf/vhost/"+nginx['only']+'.conf'):
            os.remove(filenames+"/conf/vhost/"+nginx['only']+'.conf')
            if os.path.isfile(filenames+"/conf/vhost/rewrite/"+nginx['only']):
                os.remove(filenames+"/conf/vhost/rewrite/"+nginx['only'])
            if os.path.isfile(filenames+"/logs/"+nginx['only']+".access.log"):
                os.remove(filenames+"/logs/"+nginx['only']+".access.log")
            os.system("cd "+filenames+" & stop.bat")
            time.sleep(3)
            os.system("cd "+filenames+" & start.bat")
    else:
        return returnjson(code=1,msg="无法匹配系统")
    if path=='1' and os.path.exists(nginx['path']):
        shutil.rmtree(nginx['path'])
    sqlite('app_web').where('id',id).delete()
    
    return returnjson()
def updconf():
    "更新网站配置信息"
    data=request.get_json()
    app_web=sqlite('app_web')
    nginx=app_web.where("id",data['id']).find()
    filenames=nginx['servers']
    servertpl=filenames+'/conf/vhost/webtpl/default'
    if data['filepath']=='base': #更新基本信息、域名信息，负载均衡信息 
        if '5.6' in data['phpeditionath']:
            phpport=9000
        elif '7.0' in data['phpeditionath']:
            phpport=9610
        elif '7.1' in data['phpeditionath']:
            phpport=9611
        elif '7.2' in data['phpeditionath']:
            phpport=9612
        elif '7.3' in data['phpeditionath']:
            phpport=9613
        elif '7.4' in data['phpeditionath']:
            phpport=9614
        elif data['phpeditionath']=='static':
            phpport='static'
        elif data['phpeditionath']=='vue':
            phpport='vue'
        else:
            return returnjson(code=1,msg='找不到php版本')
        
        
        ttt1=data['domain'].split("\n")
        server_name=''
        for k in ttt1:
            server_name=str(server_name)+" "+str(k)
        where="port="+data['port']+" and id != "+data['id']+" and (" #[('port','eq',data['port'])]
        for kk in ttt1:
            where=where+"domain like '%"+kk+"%'"+" or "
        where=where[:-4]+")"
        ttt2=app_web.where(where).find()
        if ttt2:
            ttt2=ttt2['domain'].split("\n")
            for k in ttt2:
                for kk in ttt2:
                    if k==kk:
                     return returnjson(code=1,msg=k+"已在本服务器其他站点使用被使用")
        for k in data['balancing']:
            if k['ip']=='' or k['port']=='':
                return returnjson(code=1,msg="请填写负载均衡ip和端口")
        upddata={
            "phpeditionath":data['phpeditionath'],
            "domain":data['domain'],
            "port":data['port'],
            "path":data['path'],
            "balancing":json_encode(data['balancing']),
            "client_max_body_size":data['client_max_body_size']
        }
        backconf=file_get_content(servertpl)
        text=Templates(servertpl,balancing=data['balancing'],client_max_body_size=data['client_max_body_size'],port=data['port'],
            proxy_set_header=[],ssl=False,
            server_name=server_name,only=nginx['only'],webpath=data['path'],phpport=phpport,rewrite=filenames+"/conf/vhost/rewrite/"+nginx['only'])
        f=open(filenames+"/conf/vhost/"+nginx['only']+'.conf','w',encoding="utf-8")
        f.write(text)
        f.close()
        sqlite("app_web").where("id",data['id']).update(upddata)
        pi=subprocess.Popen('nginx -s reload',shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        ars=pi.stdout.read().decode()
        ars=ars.split("\n")
        strs=ars[len(ars)-2]
        if len(strs) > 1:
            file_set_content(servertpl,backconf)
            return returnjson(code=1,msg=strs)
        # sqlite('app_web').where('id',id).update({'domain':data['text']})
    else: #更新伪静态和当前配置文件
        # f=open(paths+filenames+"/conf/vhost/rewrite/"+nginx['only'],'w',encoding="utf-8")
        backconf=file_get_content(filenames+data['filepath'])
        file_set_content(filenames+data['filepath'],data['text'])
        pi=subprocess.Popen('nginx -s reload',shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        ars=pi.stdout.read().decode()
        ars=ars.split("\n")
        strs=ars[len(ars)-2]
        if len(strs) > 1:
            file_set_content(filenames+data['filepath'],backconf)
            return returnjson(code=1,msg=strs)
    return returnjson()
def ssl(id):
    nginx=sqlite('app_web').where("id",id).find()
    data=request.get_json()
    filenames=nginx['servers']
    key=filenames+'/conf/vhost/rewrite/'+nginx['only']+".key"
    pem=filenames+'/conf/vhost/rewrite/'+nginx['only']+".pem"
    file_set_content(key,data['key'])
    file_set_content(pem,data['pem'])
    ttt=nginx['domain'].split("\n")
    server_name=''
    for k in ttt:
        server_name=str(server_name)+" "+str(k)
    if '5.6' in nginx['phpeditionath']:
        phpport=9000
    elif '7.0' in nginx['phpeditionath']:
        phpport=9610
    elif '7.1' in nginx['phpeditionath']:
        phpport=9611
    elif '7.2' in nginx['phpeditionath']:
        phpport=9612
    elif '7.3' in nginx['phpeditionath']:
        phpport=9613
    elif '7.4' in nginx['phpeditionath']:
        phpport=9614
    elif nginx['phpeditionath']=='static':
        phpport='static'
    elif nginx['phpeditionath']=='vue':
        phpport='vue'
    else:
        return returnjson(code=1,msg='找不到php版本')
    servertpl=filenames+'/conf/vhost/webtpl/default'
    backtext=file_get_content(servertpl)
    text=Templates(servertpl,balancing=json_decode(nginx['balancing']),client_max_body_size=nginx['client_max_body_size'],port=nginx['port'],
            proxy_set_header=[],ssl=443,
            server_name=server_name,only=nginx['only'],webpath=nginx['path'],phpport=phpport,rewrite=filenames+"/conf/vhost/rewrite/"+nginx['only'])
    file_set_content(filenames+"/conf/vhost/"+nginx['only']+'.conf',text)
    pi=subprocess.Popen('nginx -s reload',shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    ars=pi.stdout.read().decode()
    ars=ars.split("\n")
    strs=ars[len(ars)-2]
    if len(strs) > 1:
        file_set_content(servertpl,backtext)
        return returnjson(code=1,msg=strs)
    return returnjson()
def createssl():
    data=request.get_json()
    if len(data['domain'])<1:
        return returnjson(code=1,msg="至少添加一个域名")
    cmd='/intapp/letsencrypt/letsencrypt-auto certonly --standalone --email '+data['email']
    domain=''
    for k in data['domain']:
        if k['domain']:
            cmd+=" -d "+k['domain']
            domain+=k['domain']+"\n"
        else:
            return returnjson(code=1,msg="请输入域名")
    add_queue(target=__createssl,args=(data,),title="创建Let's Encrypt免费证书",describes=cmd)
    return returnjson(code=0,msg="已添加到任务，请稍后到ssl列表夹查看")
def __createssl(data):
    "创建Let's Encrypt免费证书"
    # data=request.get_json()
    if len(data['domain'])<1:
        return returnjson(code=1,msg="至少添加一个域名")
    # cmd='/intapp/letsencrypt/letsencrypt-auto certonly --standalone --email fk1402936534@qq.com -d test1.kwebapp.cn'
    # cmd='/intapp/letsencrypt/letsencrypt-auto certonly --email fk1402936534@qq.com -d *.kwebapp.cn --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory'
    cmd='/intapp/letsencrypt/letsencrypt-auto certonly --standalone --email '+data['email']
    # cmd='/intapp/letsencrypt/letsencrypt-auto certonly --email '++data['email']
    domain=''
    for k in data['domain']:
        if k['domain']:
            cmd+=" -d "+k['domain']
            domain+=k['domain']+"\n"
        else:
            return returnjson(code=1,msg="请输入域名")
    # cmd+=' --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory''
    child = pexpect.spawn(cmd,timeout=180)
    time.sleep(1)
    index = child.expect(["gree","right IP address","ongratulations","appropriate number","Problem binding to port 80", pexpect.EOF, pexpect.TIMEOUT])
    print("index1",index)
    if index == 0 :
        child.sendline("A")
        index = child.expect(["es", pexpect.EOF, pexpect.TIMEOUT])
        print("index2",index)
        if (index == 0):
            child.sendline("Y")
            index = child.expect(["(?i)ongratulations", pexpect.EOF, pexpect.TIMEOUT])
            print("index3",index)
            if index == 0:
                print("成功")
                conf={
                    "data":data,
                    "createtime":times(),
                    "createdate":str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                }
                file_set_content("/etc/letsencrypt/live/"+str(data['domain'][0]['domain'])+"/config.conf",json_encode(conf))
                child.close(force=True)
                return returnjson()
            else:
                print("error1")
                child.close(force=True)
                return returnjson(code=1,msg="申请不成功")
        else:
            return returnjson(code=1,msg="申请失败")
            child.close(force=True)
    elif index == 1: 
        print("contain(s) the right IP address")
        child.close(force=True)
        return returnjson(code=1,msg="域名无法访问访问，检查域名解析或是否备案")
    elif index == 2: 
        print("成功")
        conf={
            "data":data,
            "createtime":times(),
            "createdate":str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        }
        file_set_content("/etc/letsencrypt/live/"+str(data['domain'][0]['domain'])+"/config.conf",json_encode(conf))
        child.close(force=True)
        return returnjson()
    elif index == 3:
        print("该域名已签发，并在有效期内")
        child.close(force=True)
        return returnjson(code=1,msg="7天内最多申请5个")
    elif index == 4:
        child.close(force=True)
        return returnjson(code=1,msg="80端口被占用")
    else:
        print("error")
        child.close(force=True)
    return returnjson(code=1,msg="失败，您可以在终端执行这个命令尝试："+cmd)
    
#续签 ssl
# ./letsencrypt-auto certonly --renew-by-default --email test@kwebapp.cn -d test1.kwebapp.cn -d test2.kwebapp.cn

def webinfo(id):
    "获取网站配置信息"
    nginx=sqlite('app_web').where('id',id).find()
    filenames=nginx['servers']
    pseudo_static_tpl=get_file(filenames+'/conf/vhost/webtpl/rewrite') #伪静态模板
    tpl=[]
    for k in pseudo_static_tpl:
        tpl.append({'name':k['name'],'text':file_get_content(k['path'])})
    key=filenames+'/conf/vhost/rewrite/'+nginx['only']+".key"
    pem=filenames+'/conf/vhost/rewrite/'+nginx['only']+".pem"
    data={
        "baseinfo":nginx,
        "balancing":json_decode(nginx['balancing']),
        "phpeditionath":sqlite("software",config.software).field("id,title").where("title like 'php%' and status >=4 and platform = '"+get_sysinfo()['uname'][0]+"' and title != 'phpmyadmin4.9'").select(),
        "pseudo_static":{
            "text":file_get_content(filenames+'/conf/vhost/rewrite/'+nginx['only']), #伪静态信息
            'tpl':tpl #伪静态模板
        },
        "configinfo":file_get_content(filenames+'/conf/vhost/'+nginx['only']+'.conf'),
        # "access":file_get_content(filenames+'/logs/'+nginx['only']+'.access.log'),
        "accesspath":'/logs/'+nginx['only']+'.access.log',
        'key':file_get_content(key),
        'pem':file_get_content(pem)
    }
    return returnjson(data)
