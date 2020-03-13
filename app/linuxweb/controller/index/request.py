from app.linuxweb.common import *
import re

def treeadd(pid=0):
    "添加节点  父节点pid"
    data=request.get_json()
    if int(data['pid']) > 0 and not sqlite('request',config.doc).where('id',data['pid']).count():
        return returnjson(code=1,msg="pid错误"+str(data['pid']))
    data['adminid']=G.userinfo['id']
    data['addtime']=times()
    data['updtime']=times()
    sqlite('request',config.doc).insert(data)
    return returnjson()
def treedel(id):
    "删除节点"
    def getSubNode(id,arr=[]):
        a=sqlite("request",config.doc).where('pid',id).field('id').select()
        for k in a:
            arr.append(k['id'])
            getSubNode(k['id'],arr)
        return arr
    arrid=getSubNode(id)
    if arrid:
        sqlite("request",config.doc).where('pid','in',arrid).delete()
    sqlite("request",config.doc).where('id',id).delete()
    return returnjson()