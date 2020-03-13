# -*- coding: utf-8 -*-
from app.linuxweb.common import *
class sqlitebase(model.model):
    config={'type':'sqlite'}
    model.dbtype.conf=config
class modeldoctext(sqlitebase):
    config={'type':'sqlite','db':config.doc['db']}
    model.dbtype.conf=config
    "文档内容"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        'doclist_id':model.dbtype.int(LEN=11,DEFAULT=0),        #文档列表id
        'types':model.dbtype.int(LEN=1,DEFAULT=0),              #0目录  1文件
        "pid":model.dbtype.int(LEN=11,DEFAULT=0),               #父级id
        "icon":model.dbtype.varchar(LEN=128,DEFAULT=''),        #图标
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #文档名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #文档描述
        "opens":model.dbtype.int(LEN=1,DEFAULT=1),              #是否展开节点
        "contents":model.dbtype.text(NULL=True),                #文档内容
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }
class doclist(sqlitebase):
    config={'type':'sqlite','db':config.doc['db']}
    model.dbtype.conf=config
    "文档项目"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        'pid':model.dbtype.int(LEN=11,DEFAULT=0),               #0项目  1版本
        "icon":model.dbtype.varchar(LEN=128,DEFAULT=''),        #图标
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #项目名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #项目描述
        "defaults":model.dbtype.int(LEN=1,DEFAULT=0),           #是否默认版本
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }
class requests(sqlitebase):
    "request收藏夹"
    config={'type':'sqlite','db':config.doc['db']}
    model.dbtype.conf=config
    table="request" 
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        'adminid':model.dbtype.int(LEN=11,DEFAULT=0),           #管理员id
        'types':model.dbtype.int(LEN=1,DEFAULT=0),              #0目录  1文件
        "pid":model.dbtype.int(LEN=11,DEFAULT=0),               #父级id
        "icon":model.dbtype.varchar(LEN=128,DEFAULT=''),        #图标
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #描述
        "opens":model.dbtype.int(LEN=1,DEFAULT=1),              #是否展开节点
        "contents":model.dbtype.text(NULL=True),                #内容
        "intos":model.dbtype.text(NULL=True),                #内容
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }

class admin(sqlitebase):
    "管理员"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "icon":model.dbtype.varchar(LEN=512,DEFAULT=''),
        "username":model.dbtype.varchar(LEN=32,DEFAULT=''),     #用户名
        "password":model.dbtype.varchar(LEN=32,DEFAULT=''),     #登录密码 MD5值
        "phone":model.dbtype.varchar(LEN=11,DEFAULT=''),        #手机
        "nickname":model.dbtype.varchar(LEN=64,DEFAULT=''),     #昵称
        "name":model.dbtype.varchar(LEN=8,DEFAULT=''),          #姓名
        "logintime":model.dbtype.int(LEN=11,DEFAULT=0),         #登录时间
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0)            #添加时间
    }
class task(sqlitebase):
    "任务"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "title":model.dbtype.varchar(LEN=1024,DEFAULT=''),       #项目名称
        "describes":model.dbtype.varchar(LEN=2048,DEFAULT=''),   #项目描述
        "code":model.dbtype.int(LEN=11,DEFAULT=2),              #是否默认版本 0成功 1失败 2等待中 3正在执行  4完成
        "res":model.dbtype.text(),                              #执行结果
        "key":model.dbtype.varchar(LEN=32,DEFAULT=''),          #项目描述
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0)            #添加时间
    }
class terminal(sqlitebase):
    "终端配表"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "icon":model.dbtype.varchar(LEN=128,DEFAULT=''),        #图标
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #描述
        "status":model.dbtype.int(LEN=1,DEFAULT=1),             #0关闭 1开启
        "defaults":model.dbtype.int(LEN=1,DEFAULT=0),           #0不是默认 1默认
        "host":model.dbtype.varchar(LEN=64,DEFAULT=''),         #需要连接服务器的ip
        "port":model.dbtype.varchar(LEN=8,DEFAULT='22'),        #需要连接服务器的端口
        "user":model.dbtype.varchar(LEN=32,DEFAULT='root'),     #需要连接服务器的用户名
        "password":model.dbtype.varchar(LEN=64,DEFAULT=''),     #需要连接服务器的密码
        "bgcolor":model.dbtype.varchar(LEN=32,DEFAULT=''),      #终端背景颜色
        "command ":model.dbtype.varchar(LEN=512,DEFAULT=''),    #登录后立即执行的命令
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }

class app_web(sqlitebase):
    "网站列表"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "domain":model.dbtype.varchar(LEN=512,DEFAULT=''),      #域名
        "port":model.dbtype.varchar(LEN=8,DEFAULT='80'),        #端口
        "icon":model.dbtype.varchar(LEN=128,DEFAULT=''),        #图标
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #描述
        "status":model.dbtype.int(LEN=1,DEFAULT=1),             #网站状态 0停止  1开启
        "path":model.dbtype.varchar(LEN=256,DEFAULT=''),        #网站目录
        "client_max_body_size":model.dbtype.int(LEN=11,DEFAULT=20),#上传限制
        "phpeditionath":model.dbtype.varchar(LEN=256,DEFAULT=''),#php版本
        "servers":model.dbtype.varchar(LEN=256,DEFAULT=''),     #服务器名字  nginx名字
        "only":model.dbtype.varchar(LEN=32,DEFAULT=''),         #唯一字段
        "balancing":model.dbtype.varchar(LEN=2048,DEFAULT=''),  #负载均衡服务器信息
        "proxy_set_header":model.dbtype.varchar(LEN=1024,DEFAULT=''),#自定义转发请求头
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
        
    }



class software(sqlitebase):
    config={'type':'sqlite','db':config.software['db']}
    model.dbtype.conf=config
    "软件列表"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "icon":model.dbtype.varchar(LEN=128,DEFAULT=''),        #图标
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #软件名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #软件描述
        "paths":model.dbtype.varchar(LEN=256,DEFAULT=''),       #软件安装目录  卸载软件时用到
        "status":model.dbtype.int(LEN=2,DEFAULT=0),             #0未安装 1等待中 2下载中 3安装中 4已安装 5卸载中 9启动中... 10运行中 11正在停止服务...
        "filename":model.dbtype.varchar(LEN=256,DEFAULT=''),     #软件源文件地址
        "platform":model.dbtype.varchar(LEN=256,DEFAULT='Linux'),#支持的系统
        'msg':model.dbtype.varchar(LEN=1024,DEFAULT=''),        #最后一次执行结果信息
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }
class php_exten(sqlitebase):
    config={'type':'sqlite','db':config.software['db']}
    model.dbtype.conf=config
    "php扩展列表"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "pid":model.dbtype.int(LEN=11),                         #软件列表id
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #扩展名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #扩展描述
        "status":model.dbtype.int(LEN=2,DEFAULT=0),             #0未安装 1等待中 2下载中 3安装中 4已安装 5卸载中
        "filename":model.dbtype.varchar(LEN=256,DEFAULT=''),    #软件源文件地址
        'msg':model.dbtype.varchar(LEN=1024,DEFAULT=''),        #最后一次执行结果信息
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
        "updtime":model.dbtype.int(LEN=11,DEFAULT=0)            #更新时间
    }
class start_command(sqlitebase):
    "控制板启动时执行命令列表"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #扩展名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #扩展描述
        "status":model.dbtype.int(LEN=2,DEFAULT=0),             # 1已执行 0未执行
        'msg':model.dbtype.varchar(LEN=1024,DEFAULT=''),        #最后一次执行结果信息
        'command':model.dbtype.varchar(LEN=1024,DEFAULT=''),    #命令
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
    }
class conf(sqlitebase):
    "配置表"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "type":model.dbtype.varchar(LEN=128,DEFAULT='intapp'),  #配置类型
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #配置名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #配置描述
        "value":model.dbtype.text(),                            #配置值
    }
class firewall(sqlitebase):
    "防火墙"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "port":model.dbtype.varchar(LEN=128,DEFAULT=''),        #端口
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #描述
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
    }
class interval(sqlitebase):
    "定时任务"
    fields={ 
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "name":model.dbtype.varchar(LEN=128,DEFAULT=''),        #任务名字
        "types":model.dbtype.varchar(LEN=128,DEFAULT='shell'),  #任务类型
        "cycle":model.dbtype.varchar(LEN=8,DEFAULT=''),         #执行周期
        "value":model.dbtype.varchar(LEN=2056,DEFAULT=''),     #要执行的内容
        "year":model.dbtype.varchar(LEN=32,DEFAULT=''),         #年
        "month":model.dbtype.varchar(LEN=32,DEFAULT=''),        #月
        "day":model.dbtype.varchar(LEN=32,DEFAULT=''),          #日
        "week":model.dbtype.varchar(LEN=32,DEFAULT=''),         #周
        "day_of_week":model.dbtype.varchar(LEN=32,DEFAULT=''),  #周几
        "hour":model.dbtype.varchar(LEN=32,DEFAULT=''),         #时
        "minute":model.dbtype.varchar(LEN=32,DEFAULT=''),       #分
        "second":model.dbtype.varchar(LEN=32,DEFAULT=''),       #秒
        "oss":model.dbtype.varchar(LEN=32,DEFAULT=''),          #是否上传到oss
        "iden":model.dbtype.varchar(LEN=32,DEFAULT=''),         #标识
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0)            #添加时间
    }
# #基本数据库

# doclist=doclist()
# doclist.create_table()
# requests=requests()
# requests.create_table()

# password="111111"
# admin=admin()
# sqlite('').execute('DROP TABLE admin')
# admin.create_table()
# admin.insert({"username":"kcw","password":md5("kcw"+str(password)),"phone":"18559899059","nickname":"kcw-linux控制板","name":"一滴","logintime":times(),"addtime":times()})
# print("您的登录信息是：账号 kcw","密码 "+str(password))

# terminal=terminal()
# terminal.create_table()
# app_web=app_web()
# app_web.create_table()

# #软件数据库
# softwares=software()
# softwares.create_table()
# php_exten=php_exten()
# php_exten.create_table()

# start_command=start_command()
# start_command.create_table()

# conf=conf()
# sqlite('').execute('DROP TABLE conf')
# conf.create_table()
# conf.insert(
#     [
#         {'type':'intapp','title':'控制板名称','describes':'','value':'web控制板'},
#         # {'type':'intapp','title':'访问端口','describes':'','value':'9501'},
#         {'type':'system','title':'swap内存','describes':'交换内存','value':'1024'}
#     ]
# )
# firewall=firewall()
# firewall.create_table()

# task=task()
# sqlite('').execute('DROP TABLE task')
# task.create_table()

# interval=interval()
# sqlite('').execute('DROP TABLE interval')
# interval.create_table()