# intapp

## 介绍
集成应用，windows、linux集成运维应用

## 安装 
```
CentOS安装 yum install -y wget && wget http://file.kwebapp.cn/sh/install/intapp/intapp.sh && bash intapp.sh
需要安装扩展,如果使用什么的方式安装，下面的扩展会自动安装好
1. pip3.8 install -i https://pypi.tuna.tsinghua.edu.cn/simple kcweb
2. pip3.8 install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn
3. pip3.8 install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil==5.7.0
4. pip3.8 install -i https://pypi.tuna.tsinghua.edu.cn/simple apscheduler==3.6.3
5. pip3.8 install -i https://pypi.tuna.tsinghua.edu.cn/simple websockets==8.1
6. pip3.8 install -i https://pypi.tuna.tsinghua.edu.cn/simple pexpect==4.8.0
7. pip3.8 install -i https://pypi.tuna.tsinghua.edu.cn/simple webssh==1.5.1
## 启动运行
调试启动  (适合开发环境)
```
python3.8 server.py
```
#### 守护进程方式运行
启动
1. 后台方式启动
```
chmod 777 /intapp/intapp
cd /intapp && nohup ./intapp -w 1 -b 0.0.0.0:9501 server:app > log 2>&1 &
```
停止
```
cd /intapp && ./intapp stop
```
全局重启
```
startkcweb
```
以上是关于linux系统上的操作



## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


