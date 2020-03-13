#!/bin/bash
chmod 777 /intapp/intapp
chmod -R 777 /intapp
pkill -9 python3.6intapp
pkill -9 wssh
cd app/cli
nohup python3.6intapp websocket.py > log 2>&1 &
cd ../../
sleep 2
nohup ./intapp -w 1 -b 0.0.0.0:9501 server:app > log 2>&1 &
nohup /usr/local/python/python3.6/bin/wssh --address=0.0.0.0 --port=39101 --sslport=4433 --certfile='app/file/key/cert.crt' --keyfile='app/file/key/cert.key'  > log 2>&1 &