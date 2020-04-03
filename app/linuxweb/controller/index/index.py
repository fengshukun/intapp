
# -*- coding: utf-8 -*-
from app.linuxweb.common import *
import traceback
def before_request():
    pass
def index(html='index'):
    "index所有html页面"
    if html=='login':
        return tpl('/error.html',title="禁止重复登录",content="您已处于登录状态")
    if html!='request':
        G.userinfo=get_session("userinfo")
        if not G.userinfo:
            username=request.args.get('username') if request.args.get('username') else ''
            password=request.args.get('password') if request.args.get('password') else ''
            return tpl('/index/index/login.html',username=username,password=password)
    try:
        return tpl('/index/index/'+html+'.html')
    except Exception as e:
        err=traceback.format_exc().split(",")
        return tpl('/error.html',title="页面错误:"+str(e),content=err)
def doc(html='index',id=0):
    "doc所有html页面"
    try:
        return tpl('/index/doc/'+html+'.html',id=id)
    except Exception as e:
        err=traceback.format_exc().split(",")
        return tpl('/error.html',title="页面错误:"+str(e),content=err)