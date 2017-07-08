#!/bin/sh

rm -rf app.db migrations/

env FLASK_DEBUG=1 FLASK_APP=main.py flask initdb

# start migrations
#~ env FLASK_DEBUG=1 FLASK_APP=main.py flask db init

