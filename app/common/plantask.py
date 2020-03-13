# -*- coding: utf-8 -*-
import asyncio,websockets
from kcweb.common import *
from app import config
from queue import Queue
import math,threading,shutil,traceback,subprocess,socket,requests,zipfile,random,re,pexpect,multiprocessing
from apscheduler.schedulers.blocking import BlockingScheduler
if not os.path.exists(config.cache['folder']+"/plan/"):
    os.makedirs(config.cache['folder']+"/plan/")
class plan():
    def log(self,iden):
        "获取任务日志"
        if os.path.isfile(config.cache['folder']+"/plan/"+str(iden)):
            f=open(config.cache['folder']+"/plan/"+str(iden),"r",encoding='utf-8')
            k=f.read()
            f.close()
            return k
        else:
            return ''
    def shells(self,shell,iden):
        shell=shell+" >> "+config.cache['folder']+"/plan/"+iden+" 2>&1 &"
        f=open(config.cache['folder']+"/plan/"+str(iden),"w+",encoding='utf-8')
        f.write("---------"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"--OPEN shell SUCCESS---------\n"+shell+"\n")
        f.close()
        # os.system(shell) 
        subprocess.Popen(shell,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # ars=pi.stdout.read().decode()
    def openurls(self,url,iden):
        http=Http()
        http.httpurl(url)
        f=open(config.cache['folder']+"/plan/"+str(iden),"w+",encoding='utf-8')
        f.write("---------"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"--OPEN URL SUCCESS---------\n"+http.get_text+"\n---------OPEN URL END---------\n\n\n")
        f.close()
    def backupmysql(self,paths,iden,types='backup',upload_aliyun=1):
        "备份或恢复mysql数据"
        shell="cd "+config.APP_PATH+"/cli && ./backupmysql "+types+" "+paths+" "+str(upload_aliyun)+" >> "+config.cache['folder']+"/plan/"+iden+" 2>&1 &"
        f=open(config.cache['folder']+"/plan/"+str(iden),"w+",encoding='utf-8')
        f.write("---------"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"--OPEN shell SUCCESS---------\n"+shell+"\n")
        f.close()
        os.system(shell)
    def plantaskdsfsdfsafdsafsd(self,func,targger="cron",args=None,year=None,month=None,week="*",day_of_week='*',day=None,hour=None,minute=None,second='0'):
        """添加定时器任务、计划任务

        func 函数名

        args 函数参数  例：(1,)

        year 年

        month 月

        day 日

        hour 几点

        minute 几分

        second 几秒
        """
        BlockingSchedulers = BlockingScheduler()
        if targger=='cron':
            BlockingSchedulers.add_job(func,targger,args=args,year=year,month=month,week=week,day_of_week=day_of_week,day=day,hour=hour, minute=minute,second=second)
        elif targger=='interval':
            if day:
                BlockingSchedulers.add_job(func,targger,args=args,days=int(day))
            elif hour:
                BlockingSchedulers.add_job(func,targger,args=args,hours=int(hour))
            elif minute:
                BlockingSchedulers.add_job(func,targger,args=args,minutes=int(minute))
            elif second:
                BlockingSchedulers.add_job(func,targger,args=args,seconds=int(second))
        try:
            BlockingSchedulers.start()
        except:
            BlockingSchedulers.shutdown()
    def plantask(self,data):
        "添加任务"
        if data['types']=='shell':
            func=self.shells
            args=(data['value'],data['iden'])
        elif data['types']=='openurl':
            func=self.openurls
            args=(data['value'],data['iden'])
        elif data['types']=='backupmysql': #备份mysql到阿里云
            func=self.backupmysql
            args=(data['value'],data['iden'])
        targger="cron"
        year=None
        month=None
        day=None
        week="*"
        day_of_week="*"
        hour=None
        minute=None
        second='0'
        if data['cycle']=='minute':
            second=data['second']
        elif data['cycle']=='hour':
            second=data['second']
            minute=data['minute']
        elif data['cycle']=='day_of_week':
            second=data['second']
            minute=data['minute']
            day_of_week=data['day_of_week']
        elif data['cycle']=='day':
            second=data['second']
            minute=data['minute']
            hour=data['hour']
        elif data['cycle']=='month':
            second=data['second']
            minute=data['minute']
            hour=data['hour']
            day=data['day']
        elif data['cycle']=='year':
            second=data['second']
            minute=data['minute']
            hour=data['hour']
            day=data['day']
            month=data['month']
        elif data['cycle']=='fixed':
            second=data['second']
            minute=data['minute']
            hour=data['hour']
            day=data['day']
            month=data['month']
            year=data['year']
        elif data['cycle']=='NS':
            targger="interval"
            second=data['second']
        elif data['cycle']=='NM':
            targger="interval"
            minute=data['minute']
        elif data['cycle']=='NH':
            targger="interval"
            hour=data['hour']
        elif data['cycle']=='NH':
            targger="interval"
            day=data['day']
        # print(data)
        # print(targger,args,year,month,week,day_of_week,day,hour,minute,second)
        try:
            t=multiprocessing.Process(target=self.plantaskdsfsdfsafdsafsd,args=(func,targger,args,year,month,week,day_of_week,day,hour,minute,second))
            t.start()
        except:
            pass
        return True






