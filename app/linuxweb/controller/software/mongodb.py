from app.linuxweb.common import *
import base64
WORK_DIR=config.other['mongodbpath']
def get_config(id):
    '获取mongodb页面配置'
    data=json_decode(file_get_content(WORK_DIR+"/config.conf"))
    try:
        key=file_get_content(WORK_DIR+"/key/mongo.key")
    except:
        key=""
    data['key']=key
    data['get_local_ip']=get_local_ip()
    return returnjson(data)
def upd_config(id):
    '修改mongodb页面配置'
    data=request.get_json()
    os.system("mkdir -p "+WORK_DIR+"/key")
    f=open(WORK_DIR+"/key/mongo.key","w")
    f.write(data['key'])
    f.close()
    os.system("chmod 600 "+WORK_DIR+"/key/mongo.key")
    data['key']=''
    file_set_content(WORK_DIR+"/config.conf",json_encode(data))
    return returnjson()

def start_config(types='restart'):
    '启动/停止config服务'
    data=request.get_json()
    data['key']=''
    os.system("mkdir -p "+WORK_DIR+"/conf")
    f=open(WORK_DIR+"/conf/config.conf","w")
    f.write("logappend=true\n"+
            "fork=true\n"+
            "maxConns=5000\n"+
            "replSet=configs\n"+
            "keyFile="+WORK_DIR+"/key/mongo.key\n"+
            "configsvr=true")
    f.close()
    os.system("chmod 777 "+WORK_DIR+"/conf/config.conf")
    # os.system("chmod 600 "+WORK_DIR+"/key/mongo.key")
    i=1
    for k in data['configs']['server']:
        os.system("mkdir -p "+WORK_DIR+"/config"+str(i)+"/data")
        i+=1
    if types=='restart' or types=='stop': #停止服务
        i=1
        for k in data['configs']['server']:
            pid=file_get_content(WORK_DIR+"/config"+str(i)+"/db.pid")
            os.system("kill -9 "+str(pid))
            time.sleep(0.1)
            i+=1
        data['configs']['serverstatus']=0
    if types=='restart' or types=='start': #启动服务
        i=1
        for k in data['configs']['server']:
            startstatus=False
            cmd="mongod --bind_ip "+str(k['ip'])+" --port "+str(k['port'])+" -f "+WORK_DIR+"/conf/config.conf --dbpath "+WORK_DIR+"/config"+str(i)+"/data --logpath "+WORK_DIR+"/config"+str(i)+"/log.log --pidfilepath "+WORK_DIR+"/config"+str(i)+"/db.pid"
            result=os.popen(cmd)
            res = result.read()
            for line in res.splitlines():
                print("line",line)
                if 'process started successfully' in line:
                    startstatus=True
                    break
            if not startstatus:
                return returnjson(code=1,msg="启动失败")
            
            i+=1
        data['configs']['serverstatus']=1
    file_set_content(WORK_DIR+"/config.conf",json_encode(data))
    return returnjson()
def start_mongos(types='restart'):
    '启动/停止路由服务'
    data=request.get_json()
    data['key']=''
    # for k in data
    #创建配置文件
    os.system("mkdir -p "+WORK_DIR+"/conf && mkdir -p "+WORK_DIR+"/mongos")
    f=open(WORK_DIR+"/conf/mongos.conf","w")
    f.write("logappend = true\n"+
            "fork=true\n"+
            data['mongos']['configdb']+" #这里必须是公共网ip或内网ip，千万不能是127.0.0.1\n"
            "keyFile="+WORK_DIR+"/key/mongo.key\n"+
            "maxConns=20000 #最大连接数")
    f.close()
    os.system("chmod 777 "+WORK_DIR+"/conf/mongos.conf")
    os.system("mkdir -p "+WORK_DIR+"/mongos")
    if types=='restart' or types=='stop': #停止服务
        i=1
        for k in data['mongos']['server']:
            pid=file_get_content(WORK_DIR+"/mongos/db"+str(i)+".pid")
            os.system("kill -9 "+str(pid))
            time.sleep(0.1)
            i+=1
        data['mongos']['serverstatus']=0
    if types=='restart' or types=='start': #启动服务
        i=1
        for k in data['mongos']['server']:
            startstatus=False
            cmd="mongos --bind_ip "+str(k['ip'])+" --port "+str(k['port'])+" -f "+WORK_DIR+"/conf/mongos.conf --logpath "+WORK_DIR+"/mongos/log"+str(i)+".log --pidfilepath "+WORK_DIR+"/mongos/db"+str(i)+".pid"
            print(cmd)
            result=os.popen(cmd)
            res = result.read()
            for line in res.splitlines():
                print("line",line)
                if 'process started successfully' in line:
                    startstatus=True
                    break
            if not startstatus:
                return returnjson(code=1,msg="启动失败")
            i+=1
        data['mongos']['serverstatus']=1
    file_set_content(WORK_DIR+"/config.conf",json_encode(data))
    return returnjson()
def start_shard(types='restart'):
    '启动/停止分片服务'
    data=request.get_json()
    data['key']=''
    os.system("mkdir -p "+WORK_DIR+"/conf")
    
    j=1
    for shard in data['shard']:#分片列表
        f=open(WORK_DIR+"/conf/shard"+str(j)+".conf","w")
        f.write("logappend=true\n"+
                "fork=true\n"+
                "maxConns=2000\n"+
                "storageEngine=mmapv1 #基于内存映射文件的存储引擎\n"+
                "shardsvr=true\n"+
                "replSet="+shard['servername']+"\n"+
                "keyFile="+WORK_DIR+"/key/mongo.key")
        f.close()
        i=1
        for k in shard['server']:
            os.system("mkdir -p "+WORK_DIR+"/shard"+str(j)+"/data"+str(i))
            i+=1
        if types=='restart' or types=='stop': #停止服务
            i=1
            for k in shard['server']:
                pid=file_get_content(WORK_DIR+"/shard"+str(j)+"/db"+str(i)+".pid")
                os.system("kill -9 "+str(pid))
                time.sleep(0.1)
                i+=1
            data['shard'][j-1]['serverstatus']=0
        if types=='restart' or types=='start': #启动服务
            i=1
            for k in shard['server']:#副本集列表
                startstatus=False
                cmd="mongod --bind_ip "+str(k['ip'])+" --port "+str(k['port'])+" -f "+WORK_DIR+"/conf/shard"+str(j)+".conf --dbpath "+WORK_DIR+"/shard"+str(j)+"/data"+str(i)+" --logpath "+WORK_DIR+"/shard"+str(j)+"/log"+str(i)+".log --pidfilepath "+WORK_DIR+"/shard"+str(j)+"/db"+str(i)+".pid"
                print("启动cmd:",cmd)
                result=os.popen(cmd)
                res = result.read()
                for line in res.splitlines():
                    print("line",line)
                    if 'process started successfully' in line:
                        startstatus=True
                        break
                if not startstatus:
                    file_set_content(WORK_DIR+"/config.conf",json_encode(data))
                    return returnjson(code=1,msg="启动失败")
                i+=1
            data['shard'][j-1]['serverstatus']=1
        j+=1
    file_set_content(WORK_DIR+"/config.conf",json_encode(data))
    return returnjson()
# def config_init(id):
#     "config副本集初始化,"
#     data=request.get_json()
#     port=data['configs']['server'][0]['port']
#     replicaset=data['configs']['replicaset']
#     members=[]
#     i=0
#     for k in replicaset:
#         zd={'_id':i,'host':k['ip']+':'+str(k['port'])}
#         members.append(zd)
#         i+=1
#     f=open(config.path['path']+"app/linuxweb/config_init.sh","w")
#     f.write("mongo --port "+str(port)+"\n"+
#             "use admin\n"+
#             "rs.initiate({_id:'configs',members:"+json_encode(members)+"})\n"+
#             "exit")
#     f.close()
#     os.system("cd "+config.path['path']+"app/linuxweb && bash config_init.sh")
#     return returnjson()