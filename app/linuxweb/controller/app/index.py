# -*- coding: utf-8 -*-
from app.linuxweb.common import *
def web(html='index',id=0):
    "app所有html页面"
    try:
        return tpl('/app/web/'+html+'.html',id=id)
    except Exception as e:
        err=traceback.format_exc().split(",")
        return tpl('/error.html',title="页面错误:"+str(e),content=err)