# -*- coding: utf-8 -*-
from app.common import *
#下面的方法在当前模块中有效
def check_login():
    if '127.0.0.1' not in globals.HEADER.HTTP_HOST and '192.168' not in globals.HEADER.HTTP_HOST:
        config.ssh['url']='https://'+globals.HEADER.HTTP_HOST.split(':')[0]+':4433'
    else:
        config.ssh['url']='http://'+globals.HEADER.HTTP_HOST.split(':')[0]+':39101'
    appkeyusername=request.args.get('appkeyusername')
    appkeypassword=request.args.get('appkeypassword')
    if appkeyusername and appkeypassword:
        G.userinfo=sqlite('admin').where("username = '"+str(appkeyusername)+"' and password = '"+md5('kcw'+str(appkeypassword))+"'").find()
        # return returnjson(appkeypassword,-1,msg=appkeyusername)
    else:
        G.userinfo=get_session("userinfo")
    if not G.userinfo:
        return returnjson({},-1,'签权失败')
def before_request():
    return check_login()
    # print('linuxweb模块在请求前执行，我是要在配置文件配置后才能生效哦！',G.userinfo)
def after_request():
    pass
    # print('linuxweb模块在请求后执行，我是要在配置文件配置后才能生效哦！')
    
def set_session(name,value,expire=None):
    "设置session"
    return session.set("applinuxweb"+str(name),value,expire)
def get_session(name):
    "获取session"
    return session.get("applinuxweb"+str(name))
def del_session(name):
    "删除session"
    return session.rm("applinuxweb"+str(name))
def tpl(path,**context):
    intapp=sqlite('conf').where('type','intapp').select()
    return Template("/linuxweb/tpl"+str(path),intapp=intapp,config=config,static=config.static,**context)
def get_json_list(lists,count,pagenow,pagesize):
    data={
        'count':count,
        'pagenow':pagenow,
        'pagesize':pagesize,
        'pagecount':math.ceil(count/pagesize),
        'list':lists
    }
    return data
class SOFT:
    def zxdownload(ar):
        if ar['platform']=='Linux':
            return SOFT.zxinstall(ar)
        elif ar['platform']=='Windows':
            return SOFT.zxinstall(ar)
        else:
            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此平台'})
            return 
    def zxinstall(ar):
        "安装软件"
        try:
            filename=ar['filename']
            paths=ar['paths']
            if ar['platform']=='Linux':
                if 'aliyun-oss' in ar['title']:
                    os.system("pip3.6 install oss2 -i https://mirrors.aliyun.com/pypi/simple/")
                    if not os.path.exists(config.path['linux_install_path']+"python/python3.6/lib/python3.6/site-packages"):
                        sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'})
                        return False
                    sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':''})
                    return True
                if 'kodexplorer' in filename or 'phpmyadmin' in filename or 'phpims' in filename:
                    if 'phpims' in filename:
                        if not sqlite('software',config.software).where([('title','eq','php7.2'),'and',('status','gt','4')]).count():
                            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'您必须安装php7.2后才能安装'})
                            return False 
                    elif not sqlite('software',config.software).where([('title','like','%php%'),'and',('status','gt','4')]).count() or not sqlite('software',config.software).where([('title','like','%nginx%'),'and',('status','gt','4')]).count():
                        sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'您必须安装nginx和php后才能安装'})
                        return False
                sqlite('software',config.software).where('id',ar['id']).update({'status':3})
                if '.sh' in filename:
                    shell="wget "+config.static['file']+"sh/install/"+filename
                    os.system(shell)
                    if 'phpmyadmin' in filename or 'phpims' in filename:
                        sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':''})
                        return True
                    elif 'php' in filename or 'nginx' in filename:
                        if not os.path.exists(paths+ar['title']+"/sbin"):
                            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'})
                            return False
                        return SOFT.start(ar)
                    elif 'redis' in filename:
                        if not os.path.exists(paths+ar['title']+"/bin/redis-server"):
                            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'})
                            return False
                        return SOFT.start(ar)
                    elif 'mysql' in filename:
                        if not os.path.isfile(paths+ar['title']+"/support-files/mysql.server"):
                            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'})
                            return False
                        return SOFT.start(ar)
                    elif 'frp' in filename:
                        if not os.path.isfile(paths+ar['title']+"/frps") or not os.path.isfile(paths+ar['title']+"/frpc"):
                            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'})
                            return False
                    sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':''})
                    return True
                else:
                    sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'找不到安装脚本'})
                    return False
            elif ar['platform']=='Windows':
                hosts=config.static['file']
                if 'nginx' in filename or 'php' in filename:
                    if not os.path.exists(paths):
                        os.makedirs(paths)
                    if os.path.exists(paths+ar['title']):
                        shutil.rmtree(paths+ar['title'])
                    if not os.path.isfile(paths+filename):
                        
                        r=requests.get(hosts+"software/Windows/"+filename)
                        f = open(paths+ar['title']+".zip", "wb")
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                f.write(chunk)
                        f.close()
                    zf = zipfile.ZipFile(paths+ar['title']+".zip")
                    zf.extractall(paths)
                    zf.close()
                    time.sleep(5)
                    if os.path.isfile(paths+ar['title']+"/start.bat"):
                        sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':''})
                        os.remove(paths+ar['title']+".zip")
                else:
                    sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此软件安装'})
                    return
            else:
                sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此平台'})
                return 
        except Exception as e:
            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'安装失败'+str(e)})
    def start(ar):
        "启动软件服务"
        filename=ar['filename']
        paths=ar['paths']
        if ar['platform']=='Linux':
            if 'nginx' in filename:
                os.system("nginx")
            elif 'php5.6' in filename:
                os.system("php56-fpm -c "+paths+"php5.6/bin/php.ini -R")
            elif 'php7.0' in filename:
                os.system("php70-fpm -c "+paths+"php7.0/bin/php.ini -R")
            elif 'php7.1' in filename:
                os.system("php71-fpm -c "+paths+"php7.1/bin/php.ini -R")
            elif 'php7.2' in filename:
                os.system("php72-fpm -c "+paths+"php7.2/bin/php.ini -R")
            elif 'php7.3' in filename:
                os.system("php73-fpm -c "+paths+"php7.3/bin/php.ini -R")
            elif 'php7.4' in filename:
                os.system("php74-fpm -c "+paths+"php7.4/bin/php.ini -R")
            elif 'phpims' in filename:
                os.system("phpims "+config.path['linux_install_path']+"other/phpims/V1/start.php start -d")
            elif 'redis' in filename:
                os.system("nohup redis-server "+paths+ar['title']+"/redis.conf > log 2>&1 &")
            elif 'mysql' in filename:
                os.system("mysqld start")
            sqlite('software',config.software).where('id',ar['id']).update({'status':10,'msg':''})
        elif ar['platform']=='Windows':
            if 'nginx' in ar['title'] or 'php' in ar['title']:
                os.system("cd "+paths+ar['title']+" & start.bat")
                sqlite('software',config.software).where('id',ar['id']).update({'status':10,'msg':''})
                return
            else:
                sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此软件启动'})
                return 
        else:
            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此平台'})
            return 
    def stop(ar): 
        "停止正在运行的软件"
        filename=ar['filename']
        paths=ar['paths']
        if ar['platform']=='Linux':
            if 'nginx' in filename:
                os.system("pkill nginx")
            elif 'php5.6' in filename:
                os.system("pkill php56-fpm")
            elif 'php7.0' in filename:
                os.system("pkill php70-fpm")
            elif 'php7.1' in filename:
                os.system("pkill php71-fpm")
            elif 'php7.2' in filename:
                os.system("pkill php72-fpm")
            elif 'php7.3' in filename:
                os.system("pkill php73-fpm")
            elif 'php7.4' in filename:
                os.system("pkill php74-fpm")
            elif 'phpims' in filename:
                os.system("phpims "+config.path['linux_install_path']+"other/phpims/V1/start.php stop")
            elif 'redis' in filename:
                os.system("pkill redis")
            elif 'mysql' in filename:
                os.system("mysqld stop")
            elif 'mongo' in filename:
                os.system("pkill mongo")
            sqlite('software',config.software).where('id',ar['id']).update({'status':4})
            return True
        elif ar['platform']=='Windows':
            if 'nginx' in ar['title'] or 'php' in ar['title']:
                os.system("cd "+paths+ar['title']+" & stop.bat")
                sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':''})
                return True
            else:
                sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此软件停止'})
                return 
        else:
            sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此平台'})
            return 
    def reboot(ar):
        "重启"
        # if 'phpims' in ar['filename']:
        #     os.system("phpims "+config.path['linux_install_path']+"other/phpims/V1/start.php restart -d")
        if SOFT.stop(ar):
            SOFT.start(ar)
    def uninstall(ar):
        "卸载软件"
        SOFT.stop(ar)
        filename=ar['filename']
        paths=ar['paths']
        try:
            if ar['platform']=='Linux':
                if 'aliyun-oss' in ar['title']:
                    os.system("pip3.6 uninstall oss2 -y")
                    if not os.path.exists(config.path['linux_install_path']+"python/python3.6/lib/python3.6/site-packages"):
                        sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':'卸载失败'})
                        return
                    sqlite('software',config.software).where('id',ar['id']).update({'status':0})
                    return True
                startpath=config.path['linux_install_start_path']
                os.system("rm -rf "+paths+ar['title'])
                if 'nginx' in filename:
                    os.system("rm -rf "+startpath+"nginx")
                elif 'php5.6' in filename:
                    os.system("rm -rf "+startpath+"php56-fpm")
                elif 'php7.0' in filename:
                    os.system("rm -rf "+startpath+"php70-fpm")
                elif 'php7.1' in filename:
                    os.system("rm -rf "+startpath+"php71-fpm")
                elif 'php7.2' in filename:
                    os.system("rm -rf "+startpath+"/php72-fpm")
                elif 'php7.3' in filename:
                    os.system("rm -rf "+startpath+"php73-fpm")
                elif 'php7.4' in filename:
                    os.system("rm -rf "+startpath+"php74-fpm")
                elif 'mysql' in filename:
                    os.system("rm -rf "+startpath+"mysqld && rm -rf "+startpath+"mysql && rm -rf /etc/my.cnf")
                elif 'mongodb' in filename:
                    os.system("rm -rf "+config.other['mongodbpath'])
                else:
                    if os.path.exists(paths+ar['title']):
                        sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':'卸载失败'})
                        return
                sqlite('software',config.software).where('id',ar['id']).update({'status':0})
                return True
            elif ar['platform']=='Windows':
                hosts=config.static['file']
                if 'nginx' in filename or 'php' in filename:
                    if os.path.exists(paths+ar['title']):
                        shutil.rmtree(paths+ar['title']+"/")
                    if os.path.isfile(paths+filename):
                        os.remove(paths+filename)
                    sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':''})
                    return
                else:
                    sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此软件卸载'})
                    return 
            else:
                sqlite('software',config.software).where('id',ar['id']).update({'status':0,'msg':'不支持此平台'})
                return 
        except Exception as e:
            sqlite('software',config.software).where('id',ar['id']).update({'status':4,'msg':'卸载失败'+str(e)})