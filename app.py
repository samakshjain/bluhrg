# @Author: Samaksh Jain <ybl>
# @Date:   Wednesday, July 6th 2016, 12:19:55 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Wednesday, July 6th 2016, 9:35:16 pm(IST)
# @License: MIT

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Flask config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/')
@app.route('/<int:id>')
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
    bluhrg_post = BluhrgPost(title=request.form['title'], content=request.form['content'], tags=request.form['tags'])
    db.session.add(bluhrg_post)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/metadata')
def get_metadata():
    entries = BluhrgPost.query.all()
    total = len(entries)
    return jsonify(total_posts=total)


if __name__ == "__main__":
    app.run()
