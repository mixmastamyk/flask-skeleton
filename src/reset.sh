#!/bin/sh

rm -rf app.db migrations/

#~ echo 'from main import db; db.create_all()' |
echo 'from main import init_db; init_db()' | \
    env FLASK_DEBUG=1 FLASK_APP=main.py flask shell

# start migrations
#~ env FLASK_DEBUG=1 FLASK_APP=main.py flask db init

