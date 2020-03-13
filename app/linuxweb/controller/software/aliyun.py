from app.linuxweb.common import *
dar=config.path['linux_install_path']+"python/python3.6/lib/python3.6/site-packages/oss2"
def getconfig():
    text=file_get_content(dar+"/config")
    data=json_decode(text)
    return returnjson(data)
def updconfig():
    data=request.get_json()
    text=json_encode(data)
    file_set_content(dar+"/config",text)
    return returnjson()