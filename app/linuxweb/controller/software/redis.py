from app.linuxweb.common import *
def conf(id,is_upd=0):
    "redis配置文件信息"
    is_upd=int(is_upd)
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    if ar['platform']=='Linux':
        filepath=paths+filenames+"/redis.conf"
    else:
        return returnjson(code=1,msg="不支持此时平台")
    if is_upd: #修改配置
        data=request.get_json()
        if not data['text']:
            return returnjson(code=1,msg='不允许清空配置文件')
        file_set_content(filepath,data['text'])
        return returnjson()
    else:
        data=file_get_content(filepath)
        print(filepath)
    return returnjson(data)
def base(id,is_upd=0):
    "redis配置文件信息"
    is_upd=int(is_upd)
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    
    if ar['platform']=='Linux':
        filepath=paths+filenames+"/redis.conf"
        jsonpath=paths+filenames+"/redis.json"
    else:
        return returnjson(code=1,msg="不支持此时平台")
    if is_upd: #修改配置
        data=request.get_json()
        f = open(filepath)
        con=''
        while True:
            line = f.readline()
            if not line:
                break
            elif 'bind ' in line and '\n' in line and '#' not in line:
                line="bind "+data['bind']+"\n"
            elif 'port ' in line and '\n' in line and '#' not in line:
                line="port "+data['port']+"\n"
            elif 'timeout ' in line and '\n' in line and '#' not in line:
                line="timeout "+data['timeout']+"\n"
            elif 'maxclients ' in line and '\n' in line:
                line="maxclients "+data['maxclients']+"\n"
            elif 'databases ' in line and '\n' in line and '#' not in line:
                line="databases "+data['databases']+"\n"
            elif 'requirepass ' in line and '\n' in line:
                if data['requirepass']:
                    line="requirepass "+data['requirepass']+"\n"
                else:
                    line="# requirepass "+data['requirepass']+"\n"
            elif 'maxmemory ' in line and '\n' in line and len(line)<20:
                line="maxmemory "+data['maxmemory']+"\n"
            con=con+line
        f.close()
        f= open(filepath, "w")
        f.write(con)
        f.close()
        file_set_content(jsonpath,json_encode(data))
        return returnjson()
    else:
        v=file_get_content(jsonpath)
        data=json_decode(v)
    return returnjson(data)