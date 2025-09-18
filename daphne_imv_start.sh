#!/bin/bash
cd /home/pmota/WEB/IMV_T
source IMV_T_env/bin/activate
python IMV_T/index2.py -b 127.0.0.1 -p 8002 --access-log=logs/python.log IMV_T.asgi:application

