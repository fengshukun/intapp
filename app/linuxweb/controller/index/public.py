from app.linuxweb.common import *
import traceback,subprocess
# def error(err,data):
#     print("错误")
#     return err
def before_request():
    pass
def login(username='',sign='',timestamp='',random=''):
    "登录"
    if (times()-int(timestamp))>86400 or times()-int(timestamp)<-86400:
        return returnjson(code=-2,msg='时间戳错误')
    inifo=sqlite('admin').where([('username','eq',username),'or',('phone','eq',username)]).find()
    if not inifo:
        return returnjson(code=-3,msg='用户名错误')
    if inifo['id']>100:
        return returnjson(code=-4,msg='您不是管理员账号')
    usign=md5(str(inifo['username'])+str(inifo['password'])+str(timestamp)+str(random))
    if usign!=sign:
        return returnjson(code=-5,msg='密码错误')
    set_session("userinfo",inifo)
    sqlite('admin').where('id',inifo['id']).update({'logintime':times()})
    return returnjson(msg='登录成功')
def outlogin():
    "退出登录"
    del_session("userinfo")
    return returnjson(msg='成功退出')
def request_tree():
    "获取request收藏夹节点"
    where=[]
    if request.args.get('kw'):
        where.append(('title','like',request.args.get('kw')))
    data=list_to_tree(sqlite('request',config.doc).where(where).field('id,pid,icon,title,describes,opens,types').select(),'id','pid','level')
    return returnjson(data)
def request_treetext(id):
    data=sqlite('request',config.doc).find(id)
    data['contents']=json_decode(data['contents'])
    return returnjson(data)
def request_curls():
    data=request.get_json()
    if data['body']['paramtype'] == 'x-www-form-urlencoded':
        param={}
        for params in data['body']['form_param']:
            param[params['key']]=params['value']
    elif data['body']['paramtype']=='raw':
        param=(re.sub("[ \r\n\t\b]","",data['body']['raw_param']))
    header={}
    for headers in data['header']:
        header[headers['key']]=headers['value']
    http=Http()
    http.set_header=header
    if data['Method']=='GET':
        URL=data['URL']
        if data['URL'] not in '?' and data['body']['paramtype']=='x-www-form-urlencoded':
            URL+='?'
            for params in data['body']['form_param']:
                URL+=params['key']+"="+params['value']+"&"
            URL=URL[:-1]
        http.openurl(URL)
    else:
        http.openurl(data['URL'],data['Method'],param)
    data={
        'header':http.get_header,
        'status':http.get_status_code,
        'body':http.get_text
    }
    del http
    return returnjson(data)
def gitpull():
    "执行git"
    path=request.args.get('path')
    branch=request.args.get('branch') #强制更新指定分支
    title=request.args.get('title')
    if not title:
        title="执行命令 git pull 命令"
    shell='cd '+path+' && sudo /usr/bin/git reset --hard'
    if branch:
        shell+=' origin/'+branch
    shell+=' && sudo /usr/bin/git clean -f && sudo /usr/bin/git pull'
    add_queue(target=PUBLICOther.gitpull,args=(path,shell),title=title,describes="执行命令："+shell)
    return returnjson("命令已添加到任务队列中")
class PUBLICOther():
    def gitpull(path,shell):
        pi=subprocess.Popen(shell,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        strs=pi.stdout.read().decode()
        f=open(path+"/gitpull.log","w",encoding='utf-8')
        f.write("\n时间:%s\n%s\n%s\n" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),shell,strs))
        f.close()
        # if 'error: Your local changes to the following files would be overwritten by merge' in strs:
        #     ttt=''
        #     try:
        #         ars=strs.split("\n")
        #         dels=False
        #         for s in ars:
        #             if 'Please commit your changes or stash them before you merge' in s:
        #                 break
        #             elif 'error: Your local changes to the following files would be overwritten by merge' in s:
        #                 dels=True
        #             if dels and 'error: Your local changes to the following files would be overwritten by merge' not in s:
        #                 s=str(s)
        #                 s=s.strip()
        #                 s=s.replace(' ','')
        #                 ttt+="rm -rf "+path+"/"+s+"\n"
        #                 os.system("rm -rf "+path+"/"+str(s))
        #         pi=subprocess.Popen(shell,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        #         strs=pi.stdout.read().decode()
        #     except:
        #         strs=traceback.format_exc()
            # f=open(path+"/gitpull.log","a",encoding='utf-8') 
            # f.write("\n删除文件后重试\n%s\n时间:%s\n%s\n%s\n" % (ttt,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),shell,strs))
            # f.close()
        if 'lready' in strs and 'up' in strs and 'to' in strs and 'date' in strs:
            send_websocket(data={"nickname":"系统","icon":"http://img.kwebapp.cn/icon/git.png","text":"git pull执行成功，返回结果是：“已经是最新的”","code":1})
        elif 'error:' in strs:
            send_websocket(data={"nickname":"系统","icon":"http://img.kwebapp.cn/icon/git.png","text":"git pull执行遇到错误","code":2})
        elif 'Updating' in strs: 
            send_websocket(data={"nickname":"系统","icon":"http://img.kwebapp.cn/icon/git.png","text":"git pull执行成功，已下载新文件于目录：<br>"+path,"code":1})
        else:
            send_websocket(data={"nickname":"系统","icon":"http://img.kwebapp.cn/icon/git.png","text":strs,"code":3})

# def test():
#     a=int(time.time())
#     ChiHuang("11.jpg")
#     print(int(time.time())-a)
#     ChiHuang("11.jpg")
#     print(int(time.time())-a)
#     ChiHuang("11.jpg")
#     print(int(time.time())-a)
#     ChiHuang("11.jpg")
#     print(int(time.time())-a)
#     ChiHuang("11.jpg")
#     print(int(time.time())-a)
#     return returnjson(int(time.time())-a)