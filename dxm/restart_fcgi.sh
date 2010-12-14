#!/bin/bash

# Replace these three settings.
PROJDIR="."
PIDFILE="$PROJDIR/fcgi.pid"
SOCKET="$PROJDIR/mysite.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  python ./manage.py runfcgi host=127.0.0.1 port=8080 pidfile=$PIDFILE
