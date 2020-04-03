pip install -i https://pypi.tuna.tsinghua.edu.cn/simple kcweb
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil==5.7.0
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple apscheduler==3.6.3
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple websockets==8.1
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pexpect==4.8.0
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple webssh==1.5.1
taskkill  /f  /im  python.exe
REM taskkill  /f  /im  wssh.exe
@echo off 
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit 
:begin
REM cd app/cli
REM python websocket.py
REM wssh --address=0.0.0.0 --port=39101
REM cd ../../
python server.py
