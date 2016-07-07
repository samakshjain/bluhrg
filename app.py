# @Author: Samaksh Jain <ybl>
# @Date:   Wednesday, July 6th 2016, 12:19:55 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Wednesday, July 6th 2016, 9:35:16 pm(IST)
# @License: MIT

import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory
from contextlib import closing
from flask_sqlalchemy import SQLAlchemy

# Flask config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import BluhrgPost

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    entries = BluhrgPost.query.all()
    return render_template('main.html', entries=entries)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/add', methods=['POST'])
def bluhrg_post():
    print request.form['title'], request.form['content'], request.form['tags']
    bluhrg_post = BluhrgPost(request.form['title'], request.form['content'], request.form['tags'])
    db.session.add(bluhrg_post)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
