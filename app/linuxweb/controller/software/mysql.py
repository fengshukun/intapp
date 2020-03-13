from app.linuxweb.common import *
def get_data(id):
    ar=sqlite('software',config.software).where('id',id).find()
    text=file_get_content(ar['paths']+ar['title']+"/config.conf")
    conf=json_decode(text)
    if not conf:
        conf={
            "base":{'rootpassword':'intapppasswordtest','path':ar['paths']+ar['title']+'/data'},
        }
    data={
        'conf':conf,
        'ar':ar,
        "my":file_get_content("/etc/my.cnf")
    }
    return returnjson(data)
def upd_my():
    "修改配置文件"
    data=request.get_json()
    file_set_content("/etc/my.cnf",data['text'])
    return returnjson()
def upd_data(id):
    ar=sqlite('software',config.software).where('id',id).find()
    data=request.get_json()
    filetext=file_get_content(ar['paths']+ar['title']+"/config.conf")
    filedata=json_decode(filetext)
    if not filedata or data['base']['rootpassword']!=filedata['base']['rootpassword']:#修改mysql密码
        os.system("mysqld restart --skip-grant-tables")
        cmd="mysql -uroot -e "
        cmd=cmd+'"use mysql;flush privileges;update user set authentication_string=password('
        cmd=cmd+"'"+str(data['base']['rootpassword'])
        cmd=cmd+"'"
        cmd=cmd+') where user='
        cmd=cmd+"'root';set password=password('"+str(data['base']['rootpassword'])+"');"
        cmd=cmd+'"'
        pi=subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        ars=pi.stdout.read().decode()
        ars=ars.split("\n")
        strs=ars[len(ars)-2]
        os.system("mysqld restart")
        print(type(strs),strs)
        if 'error' in strs:
            return returnjson(code=1,msg="密码修改失败"+strs)
            
        # mysqld restart --skip-grant-tables && mysql -uroot -e "flush privileges;update mysql.user set authentication_string=password('123456') where user = 'root'";
    # print(data['base']['rootpassword'],filedata['base']['rootpassword'])
    if not filedata or data['base']['path']!=filedata['base']['path']:
        os.system('mysqld stop')
        os.system("mkdir -p "+str(data['base']['path']))
        if not filedata:
            print("cp -r "+ar['paths']+ar['title']+"/data/. "+data['base']['path']+"/")
            os.system("cp -r "+ar['paths']+ar['title']+"/data/. "+data['base']['path']+"/")
        else:
            print("cp -r "+filedata['base']['path']+"/. "+data['base']['path']+"/")
            os.system("cp -r "+filedata['base']['path']+"/. "+data['base']['path']+"/")
        os.system("chown -R mysql "+str(data['base']['path'])+" && chgrp -R mysql "+str(data['base']['path']))
        
        f = open('/etc/my.cnf')
        con=''
        while True:
            line = f.readline()
            if not line:
                break
            elif 'datadir=' in line:
                line="datadir="+str(data['base']['path'])+"\n"
            con=con+line
        f.close()
        f= open('/etc/my.cnf', "w")
        f.write(con)
        f.close()
        time.sleep(1)
        os.system('mysqld start')
    text=json_encode(data)
    file_set_content(ar['paths']+ar['title']+"/config.conf",text)
    
    return returnjson()
