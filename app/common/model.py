# -*- coding: utf-8 -*-
# 初始化数据库
from .plantask import *
class modelsqlitebase(model.model):
    config={'type':'sqlite'}
    model.dbtype.conf=config
class model_admin(modelsqlitebase):
    "管理员"
    table="admin" 
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
class model_task(modelsqlitebase):
    "任务"
    table="task" 
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "title":model.dbtype.varchar(LEN=1024,DEFAULT=''),       #项目名称
        "describes":model.dbtype.varchar(LEN=2048,DEFAULT=''),   #项目描述
        "code":model.dbtype.int(LEN=11,DEFAULT=2),              #是否默认版本 0成功 1失败 2等待中 3正在执行  4完成
        "res":model.dbtype.text(),                              #执行结果
        "key":model.dbtype.varchar(LEN=32,DEFAULT=''),          #项目描述
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0)            #添加时间
    }
class model_terminal(modelsqlitebase):
    "终端配表"
    table="terminal"
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
class model_start_command(modelsqlitebase):
    "控制板启动时执行命令列表"
    table="start_command"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #扩展名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #扩展描述
        "status":model.dbtype.int(LEN=2,DEFAULT=0),             # 1已执行 0未执行
        'msg':model.dbtype.varchar(LEN=1024,DEFAULT=''),        #最后一次执行结果信息
        'command':model.dbtype.varchar(LEN=1024,DEFAULT=''),    #命令
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
    }
class model_conf(modelsqlitebase):
    "配置表"
    table="conf"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "type":model.dbtype.varchar(LEN=128,DEFAULT='intapp'),  #配置类型
        "title":model.dbtype.varchar(LEN=128,DEFAULT=''),       #配置名称
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #配置描述
        "value":model.dbtype.text(),                            #配置值
    }
class model_firewall(modelsqlitebase):
    "防火墙"
    table="firewall"
    fields={
        "id":model.dbtype.int(LEN=11,PRI=True,A_L=True),        #设置id为自增主键
        "port":model.dbtype.varchar(LEN=128,DEFAULT=''),        #端口
        "describes":model.dbtype.varchar(LEN=256,DEFAULT=''),   #描述
        "addtime":model.dbtype.int(LEN=11,DEFAULT=0),           #添加时间
    }
class model_interval(modelsqlitebase):
    "定时任务"
    table="interval"
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
if not os.path.isfile(config.sqlite['db']):
    #基本数据库
    password="111111"
    model_admins=model_admin()
    # sqlite('').execute('DROP TABLE admin')
    model_admins.create_table()
    sqlite("admin").insert({"username":"kcw","password":md5("kcw"+str(password)),"phone":"","nickname":"kcw-linux控制板","name":"","logintime":times(),"addtime":times()})
    model_terminal=model_terminal()
    model_terminal.create_table()
    model_start_command=model_start_command()
    model_start_command.create_table()
    model_conf=model_conf()
    # sqlite('').execute('DROP TABLE conf')
    model_conf.create_table()
    model_conf.insert(
        [
            {'type':'intapp','title':'控制板名称','describes':'','value':'web控制板'},
            # {'type':'intapp','title':'访问端口','describes':'','value':'9501'},
            {'type':'system','title':'swap内存','describes':'交换内存','value':'1024'}
        ]
    )
    model_firewall=model_firewall()
    model_firewall.create_table()
    model_task=model_task()
    # sqlite('').execute('DROP TABLE task')
    model_task.create_table()
    model_interval=model_interval()
    # sqlite('').execute('DROP TABLE interval')
    model_interval.create_table()


class model_software(modelsqlitebase):
    config={'type':'sqlite','db':config.software['db']}
    model.dbtype.conf=config
    "软件列表"
    table="software"
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
class model_php_exten(modelsqlitebase):
    config={'type':'sqlite','db':config.software['db']}
    model.dbtype.conf=config
    "php扩展列表"
    table="php_exten"
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
if not os.path.isfile(config.software['db']):
    # #软件数据库
    model_softwares=model_software()
    model_softwares.create_table()
    model_php_exten=model_php_exten()
    model_php_exten.create_table()