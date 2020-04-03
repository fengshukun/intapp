from app.linuxweb.common import *
def ini(id,is_upd=0):
    "php.ini配置文件"
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    if ar['platform']=='Linux':
        filepath=paths+filenames+"/bin/php.ini"
    elif ar['platform']=='Windows':
        filepath=paths+filenames+"/php.ini"
    else:
        return returnjson(code=1,msg="不支持此时平台")
    if is_upd: #修改配置
        data=request.get_json()
        file_set_content(filepath,data['text'])
        return returnjson()
    else:
        data={
            'ini':file_get_content(filepath),
            'php':ar
        }
        return returnjson(data)
def www_conf(id,is_upd=0):
    "www.conf配置文件"
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    if ar['platform']=='Linux':
        filepath=paths+filenames+"/etc/php-fpm.d/www.conf"
        if 'php5.6' in filenames:
            filepath=paths+filenames+"/etc/php-fpm.conf"
    elif ar['platform']=='Windows':
        filepath=''
    else:
        return returnjson(code=1,msg="不支持此时平台")
    if is_upd: #修改配置
        data=request.get_json()
        file_set_content(filepath,data['text'])
        return returnjson()
    else:
        data={
            'www_conf':file_get_content(filepath),
            'php':ar
        }
        return returnjson(data)
def phpfpm(id,is_upd=0):
    "phpfpm配置信息"
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    if ar['platform']=='Linux':
        if not os.path.exists(paths+filenames+"/bin/conf"):
            os.makedirs(paths+filenames+"/bin/conf")
        filepath=paths+filenames+"/bin/conf/phpfpm.conf"
        phpfpmpath=paths+filenames+"/etc/php-fpm.d/www.conf"
        if 'php5.6' in filenames:
            phpfpmpath=paths+filenames+"/etc/php-fpm.conf"
    else:
        filepath=''
        phpfpmpath=''
    if is_upd: #修改php-fpm配置信息
        data=request.get_json()
        f = open(phpfpmpath)
        con=''
        while True:
            line = f.readline()
            if not line:
                break
            elif 'pm = ' in line and '=' in line: #运行描述
                line="pm = "+data['text']['pm']+"\n"
            elif 'pm.max_children' in line and '=' in line:# 允许创建的最大子进程数
                line="pm.max_children = "+data['text']['max_children']+"\n"
            elif 'pm.start_servers' in line and '=' in line:# 起始进程数（服务启动后初始进程数量）
                line="pm.start_servers = "+data['text']['start_servers']+"\n"
            elif 'pm.min_spare_servers' in line and '=' in line:# 起始进程数（服务启动后初始进程数量）
                line="pm.min_spare_servers = "+data['text']['min_spare_servers']+"\n"
            elif 'pm.max_spare_servers' in line and '=' in line:# 最大空闲进程数（当空闲进程达到此值时清理）
                line="pm.max_spare_servers = "+data['text']['max_spare_servers']+"\n"
            con=con+line
        f.close()
        f= open(phpfpmpath, "w")
        f.write(con)
        f.close()
        file_set_content(filepath,json_encode(data['text']))
        return returnjson()
    else:
        phpfpm=json_decode(file_get_content(filepath))
        if not phpfpm:
            phpfpm=''
        data={
                'phpfpm':phpfpm,
                'php':ar
            }
        return returnjson(data)
def base(id,is_upd=0):
    "基本配置信息"
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    if ar['platform']=='Linux':
        if not os.path.exists(paths+filenames+"/bin/conf"):
            os.makedirs(paths+filenames+"/bin/conf")
        filepath=paths+filenames+"/bin/conf/base.ini"
        phpinipath=paths+filenames+"/bin/php.ini"
    elif ar['platform']=='Windows':
        if not os.path.exists(paths+filenames+"/conf"):
            os.makedirs(paths+filenames+"/conf")
        filepath=paths+filenames+"/conf/base.ini"
        phpinipath=paths+filenames+"/php.ini"
    if is_upd: #修改基本配置信息
        #修改php.ini配置
        data=request.get_json()
        f = open(phpinipath)
        con=''
        while True:
            line = f.readline()
            if not line:
                break
            elif 'max_execution_time' in line and '=' in line:#最大执行时间
                line="max_execution_time = "+data['text']['max_execution_time']+"\n"
            elif 'max_input_time' in line and '=' in line:#最大输入时间
                line="max_input_time = "+data['text']['max_input_time']+"\n"
            elif 'memory_limit' in line and '=' in line:#内存限制
                line="memory_limit = "+data['text']['memory_limit']+"M\n"
            elif 'file_uploads' == line[0:12] and '=' in line:#是否允许文件上传
                line="file_uploads = "+data['text']['file_uploads']+"\n"
            elif 'upload_max_filesize' in line and '=' in line:#上传大小限制
                line="upload_max_filesize = "+data['text']['upload_max_filesize']+"M\n"
            elif 'max_file_uploads' in line and '=' in line:#上传数量限制
                line="max_file_uploads = "+data['text']['max_file_uploads']+"\n"
            elif 'post_max_size' in line and '=' in line:#上传数量限制
                line="post_max_size = "+data['text']['post_max_size']+"M\n"
            elif 'allow_url_fopen' in line and '=' in line:
                line="allow_url_fopen = "+data['text']['allow_url_fopen']+"\n"
            elif 'allow_url_include' in line and '=' in line:
                line="allow_url_include = "+data['text']['allow_url_include']+"\n"
            elif 'default_socket_timeout' in line and '=' in line:
                line="default_socket_timeout = "+data['text']['default_socket_timeout']+"\n"
            con=con+line
        f.close()
        f= open(phpinipath, "w")
        f.write(con)
        f.close()
        file_set_content(filepath,json_encode(data['text']))
        # print(data['text'])
        return returnjson()
    else:
        base=json_decode(file_get_content(filepath))
        if not base:
            base=''
        data={
            'base':base,
            'php':ar
        }
        return returnjson(data)
def extenlist(id,is_upd=0):
    "php扩展信息列表"
    ar=sqlite('software',config.software).where('id',id).find()
    lists=sqlite('php_exten',config.software).where('pid',id).select()
    data={
        'extenlist':lists,
        'php':ar
    }
    return returnjson(data)
def log(id):
    "待完善"
    ar=sqlite('software',config.software).where('id',id).find()
    filename=ar['filename']
    paths=ar['paths']
    filenames=ar['title']
    if ar['platform']=='Linux':
        filepath=paths+filenames+""
    elif ar['platform']=='Windows':
        filepath=paths+filenames+""
    data={
            'log':file_get_content(filepath),
            'php':ar
        }
    return returnjson(data)

def add_php_exten():
    "增加php扩展"
    data=request.get_json()
    data['addtime']=times()
    data['updtime']=times()
    sqlite('php_exten',config.software).insert(data)
    return returnjson()
def del_php_exten(id):
    "删除php扩展"
    sqlite('php_exten',config.software).where('id',id).delete()
    return returnjson()

def installext(id):
    is_del=False #是否删除成功
    "安装php扩展和下载扩展"
    ar=sqlite('php_exten',config.software).where('id',id).find()
    if ar['status']==0:
        sqlite('php_exten',config.software).where('id',ar['id']).update({'status':1,'msg':''})
        add_queue(target=__installextqu,args=(ar,),title="安装"+ar['title'])
    elif ar['status']==4:
        "卸载扩展"
        paths=request.get_json()['paths']
        if get_sysinfo()['uname'][0]=='Linux':
            if os.path.exists(paths):
                
                confile=paths+"bin/php.ini"
                f= open(confile, "r")
                con=''
                while True:
                    line = f.readline()
                    if not line:
                        break
                    elif str(ar['title']) in line:
                        line=""
                        is_del=True
                    con=con+line
                f.close()
                f= open(confile, "w")
                f.write(con)
                f.close()

                # confile=paths+"bin/php.ini"
                # f= open(confile, "r")
                # con=f.read()
                # f.close()
                # con=con.replace("extension="+str(ar['title'])+".so\n","")
                # f= open(confile, "w")
                # f.write(con)
                # f.close()
                if is_del:
                    sqlite('php_exten',config.software).where('id',ar['id']).update({'status':0,'msg':''})
                    if 'php7.0' in paths:
                        os.system("pkill php70-fpm && php70-fpm -c "+paths+"php7.0/etc/php.ini")
                    elif 'php7.1' in paths:
                        os.system("pkill php71-fpm && php71-fpm -c "+paths+"php7.1/etc/php.ini")
                    elif 'php7.2' in paths:
                        os.system("pkill php72-fpm && php72-fpm -c "+paths+"php7.2/etc/php.ini")
                    elif 'php7.3' in paths:
                        os.system("pkill php73-fpm && php73-fpm -c "+paths+"php7.3/etc/php.ini")
                    elif 'php7.4' in paths:
                        os.system("pkill php74-fpm && php74-fpm -c "+paths+"php7.4/etc/php.ini")
                else:
                    return returnjson(code=1,msg='卸载失败')
            else:
                return returnjson(code=1,msg='php文件夹错误')
    return returnjson()
def get_exten(id):
    return returnjson(sqlite('php_exten',config.software).where('id',id).find())
def __installextqu(ar):
    "安装php扩展"
    sqlite('php_exten',config.software).where('id',ar['id']).update({'status':3,'msg':''})
    try:
        cmd="wget "+config.static['file']+"/"+ar['filename']
        # os.system(cmd)
        pi=subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        ars=pi.stdout.read().decode()
        ars=ars.split("\n")
        strs=ars[len(ars)-2]
        if 'success' in strs:
            sqlite('php_exten',config.software).where('id',ar['id']).update({'status':4,'msg':''})
        else:
            sqlite('php_exten',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'})
        # sqlite('php_exten',config.software).where('id',ar['id']).update({'status':4,'msg':''})
    except Exception as e:
        sqlite('php_exten',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'+str(e)})