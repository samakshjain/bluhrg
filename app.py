# @Author: Samaksh Jain <ybl>
# @Date:   Wednesday, July 6th 2016, 12:19:55 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Wednesday, July 6th 2016, 9:35:16 pm(IST)
# @License: MIT


import sqlite3, os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# Flask config
bluhrg = Flask(__name__)
bluhrg.config.from_object(os.environ['APP_SETTINGS'])

# init db
def init_db():
    with closing(connect_db()) as db:
        with bluhrg.open_resource('db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# connect to db
def connect_db():
    return sqlite3.connect(bluhrg.config['DATABASE'])

# connect to db before each request
@bluhrg.before_request
def before_request():
    g.db = connect_db()

# disconnect when done (even when exceptions)
@bluhrg.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@bluhrg.route('/')
def index():
    return "<h3>Hallo! Let's start the bluhrg!</h3>"

if __name__ == "__main__":
    bluhrg.run()
