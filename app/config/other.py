# -*- coding: utf-8 -*-
from kcweb.config import *
import os
#路由配置
route['default']=True   #是否开启默认路由  默认路由开启后面不影响以下配置的路由，模块名/版本名/控制器文件名/方法名 作为路由地址   如：http://www.kcw.com/api/v1/index/index/
route['modular']='linuxweb' #[{"intapp":"linuxweb"},{"app":"linuxweb"},{"www":"linuxweb"},{"127":"linuxweb"},{"212":"linuxweb",'47':'linuxweb','120':'linuxweb'}] #配置域名模块 配置后地址为：http://www.kcw.com/v1/index/index/  注意:如果使用的是代理服务器需要把代理名称设置为当前配置的域名，否则不生效
route['files']='index'  #默认路由文件 
route['funct']='index'  #默认路由函数
route['methods']=['POST','GET','PUT','DELETE']   #默认支持的请求方式


sqlite['db']='app/file/sqlite/kcwlicuxweb' #sqlite数据库
software={'db':'app/file/sqlite/software'}
doc={'db':'app/file/sqlite/doc'}

# 静态资源域名配置
static={
    'img':'//img.kwebapp.cn/',
    'static':'//static.kwebapp.cn/',
    'file':'http://file.kwebapp.cn/'
}

#ssh配置 
ssh={}
ssh['url']='http://127.0.0.1:39101/'
ssh['host']='127.0.0.1'
ssh['port']='22'
ssh['user']='root'
ssh['password']=''
ssh['bgcolor']='#000'

app['appmode']='develop'  #produc 生产环境  develop 开发环境

#目录配置
path={
    "path":os.path.abspath('.')+"/",        #当前脚本启动目录
    "linux_install_path":"/usr/local/",     #linux软件安装目录
    "linux_install_start_path":"/usr/bin/", #linux软件安启动目录
    "windows_install_path":'C:/www/'             #windows 软件安装目录
}
other={
    'app_path':path['path']+"app/",               #应用目录
    'mongodbpath':"/data/mongodb"  #mongodb数据存储目录  linux
}
websoeket={
    "ip":"0.0.0.0",
    "port":9502,
    'authkey':"desgvedgvrehgtrhbtgrsefdvsdgfdgfdsgfdf"
}
# import os
# if not os.path.exists(path['linuxinstallpath']):
#     os.makedirs(path['linuxinstallpath'])
# if not os.path.exists(path['windowsinstallpath']):
#     os.makedirs(path['windowsinstallpath'])