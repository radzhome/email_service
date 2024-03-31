#!/bin/bash
LOG=/var/log/gunicorn/email_service.log
LOGDIR=$(dirname $LOG)
test -d $LOGDIR || mkdir -p $LOGDIR
cd /var/web/email_service/
source /var/web/email_service/.venv/bin/activate
exec gunicorn --workers=1 --log-file=$LOG --bind=127.0.0.1:8001 --log-level=info email_service.wsgi:application
