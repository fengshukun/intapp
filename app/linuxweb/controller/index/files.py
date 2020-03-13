from app.linuxweb.common import *
import traceback
def lists(files='1'):
    paths=request.args.get('paths')
    if not paths:
        paths=os.path.abspath('.')+"/"
    paths=paths.replace("\\", "/")
    # lis=os.listdir(paths)
    try:
        lis=os.listdir(paths)
    except:
        return returnjson(code=1,msg="无法打开"+str(paths))
    lists=[]
    for files in lis:
        types="folder"
        if os.path.isfile(paths+"/"+files):
            types="file"
        zd={"name":files,"types":types}
        lists.append(zd)
    data=get_json_list(lists,count=len(lis),pagenow=1,pagesize=len(lis))
    data['paths']=paths
    "文件列表"
    return returnjson(data)
def get_files():
    "获取就内容"
    paths=request.args.get('paths')
    data=file_get_content(paths)
    return returnjson(data)
def del_folder():
    "删除文件夹"
    paths=request.args.get('paths')
    if os.path.exists(paths):
        shutil.rmtree(paths)
    return returnjson()