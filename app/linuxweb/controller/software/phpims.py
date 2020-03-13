from app.linuxweb.common import *
def base(id,is_upd=0):
    "phpims配置文件信息"
    is_upd=int(is_upd)
    ar=sqlite('software',config.software).where('id',id).find()
    paths=ar['paths']
    filenames=ar['title']
    if ar['platform']=='Linux':
        jsonpath=paths+filenames+"/config.json"
    else:
        return returnjson(code=1,msg="不支持此时平台")
    if is_upd: #修改配置
        data=request.get_json()
        if data:
            file_set_content(jsonpath,json_encode(data))
            return returnjson(msg="内容保存在:"+jsonpath)
        else:
            return returnjson(code=1,msg='失败')
    else:
        v=file_get_content(jsonpath)
        data=json_decode(v)
        return returnjson(data)
def get_conf():
    jsonpath=config.path['linux_install_path']+"other/phpims/config.json"
    v=file_get_content(jsonpath)
    data=json_decode(v)
    return returnjson(data)
        