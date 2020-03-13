from app.linuxweb.common import *
def index(id='',types='getinfo'):
    "nginx相关"
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    if types=='getinfo':
        if os.path.isfile(paths+filenames+'/logs/error.log'):
            # print(paths+filenames+'/logs/error.log')
            # f=open(paths+filenames+'/logs/error.log','r')
            # logserror=f.read()
            # f.close()
            logserror=''
        else:logserror=''
        if os.path.isfile(paths+filenames+'/logs/access.log'):
            # f=open(paths+filenames+'/logs/access.log','r',encoding="utf-8")
            # logsaccess=f.read()
            # f.close()
            logsaccess=''
        else:logsaccess=''
        f=open(paths+filenames+'/conf/nginx.conf','r',encoding="utf-8")
        confnginx=f.read()
        data={
            'logs':{'error':logserror,'access':logsaccess},
            'conf':{'nginx':confnginx},
        }
        return returnjson(data)
    elif types=='updconf':
        con=request.get_json()
        f=open(paths+filenames+'/conf/nginx.conf','w',encoding="utf-8")
        f.write(con['text'])
        f.close()
        return returnjson()
    else:
        return returnjson(code=1,msg="未知类型")