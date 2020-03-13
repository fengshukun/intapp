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