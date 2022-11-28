#! /bin/bash
cd /home/judge/judge_server/
nohup python3 ./match_system/src/main.py >>judge.log 2>&1 &
nohup python3 manage.py runserver 0.0.0.0:8000 >>mail.log 2>&1 &
/bin/bash