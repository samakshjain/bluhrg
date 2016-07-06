# @Author: Samaksh Jain <ybl>
# @Date:   Wednesday, July 6th 2016, 12:19:55 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Wednesday, July 6th 2016, 9:35:16 pm(IST)
# @License: MIT

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory
from contextlib import closing

# Flask config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# connect to db
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# init db
def init_db():
    db = get_db()
    with app.open_resource('db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# adding commnad to initdb
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('select heading, content from blag order by id desc')
    entries = [dict(heading=row[0], content=row[1]) for row in cur.fetchall()]
    return render_template('main.html', entries=entries)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/add', methods=['POST'])
def bluhrg_post():
    db = get_db()
    db.execute('insert into blag (heading, content) values (?, ?)',
                 [request.form['heading'], request.form['content']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
