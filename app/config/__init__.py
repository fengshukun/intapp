# -*- coding: utf-8 -*-
from .other import *
import re
#下面的配置都是全局的
APP_PATH=os.path.realpath(__file__) #app目录
APP_PATH=APP_PATH[:-19]
#目录配置
# 应用配置
app['app_debug']=True  #是否开启调试模式
app['tpl_folder']=path['path']+'app'  #设置模板文件目录名 注意：所有的配置目录都是以您的运行文件所在目录开始
app['before_request']='before_request'  #设置请求前要执行的函数名
app['after_request']='after_request'    #设置请求后要执行的函数名
app['staticpath']='app/static'

# redis配置
redis['host']='127.0.0.1' #服务器地址
redis['port']=6379 #端口
redis['password']='fk459915476'  #密码
redis['db']=0 #Redis数据库    注：Redis用0或1或2等表示
redis['pattern']=True # True连接池链接 False非连接池链接
redis['ex']=0  #过期时间 （秒）


#缓存配置
cache['type']='File' #驱动方式 支持 File Redis 
cache['folder']=APP_PATH+'/runtime' #缓存文件夹
cache['path']=APP_PATH+'/runtime/cachepath' #缓存保存目录 
cache['expire']=120 #缓存有效期 0表示永久缓存
cache['host']=redis['host'] #Redis服务器地址
cache['port']=redis['port'] #Redis 端口
cache['password']=redis['password'] #Redis登录密码
cache['db']=1 #Redis数据库    注：Redis用1或2或3等表示
if not os.path.exists(APP_PATH+'/runtime/cachepath'):
    os.makedirs(APP_PATH+'/runtime/cachepath')
# session配置
session['type']='File' #session 存储类型  支持 file、Redis
session['path']=APP_PATH+'/runtime/session/temp' #session缓存目录
session['expire']=86400 #session默认有效期 该时间是指session在服务的保留时间，通常情况下浏览器上会保留该值的10倍
session['prefix']="KCW" # SESSION 前缀
session['host']=redis['host'] #Redis服务器地址
session['port']=redis['port'] #Redis 端口
session['password']=redis['password'] #Redis登录密码
session['db']=2 #Redis数据库    注：Redis用1或2或3等表示




database['type']='mysql' # 数据库类型  目前支持mysql和sqlite
database['host']=['127.0.0.1']#服务器地址 [地址1,地址2,地址3...] 多个地址分布式(主从服务器)下有效
database['port']=[3306] #端口 [端口1,端口2,端口3...]
database['user']=['root']  #用户名 [用户名1,用户名2,用户名3...]
database['password']=['a3e1998385b']  #密码 [密码1,密码2,密码3...]
database['db']=['test']  #数据库名 [数据库名1,数据库名2,数据库名3...]
database['charset']='utf8'   #数据库编码默认采用utf8
database['pattern']=True # True数据库长连接模式 False数据库短连接模式  注：建议web应用使用短连接，cli应用使用长连接
database['cli']=True # 是否以cli方式运行
database['dbObjcount']=1 # 连接池数量（单个数据库地址链接数量），数据库链接实例数量 mysql长链接模式下有效
database['deploy']=0 # 数据库部署方式:0 集中式(单一服务器),1 分布式(主从服务器)  mysql数据库有效
database['master_num']=1 #主服务器数量 不能超过host服务器数量  （等于服务器数量表示读写不分离：主主复制。  小于服务器表示读写分离：主从复制。） mysql数据库有效
database['master_dql']=False #主服务器是否可以执行dql语句 是否可以执行select语句  主服务器数量大于等于host服务器数量时必须设置True
database['break']=1 #断线重连次数，0表示不重连。 注：cli模式下 10秒进行一次重连并且连接次数是当前配置的300倍
