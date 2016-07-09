# @Author: Samaksh Jain <ybl>
# @Date:   Wednesday, July 6th 2016, 12:19:55 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Saturday, July 9th 2016, 5:12:47 pm(IST)
# @License: MIT

from flask import Flask, request, redirect, url_for, \
     render_template, flash, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Flask config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import BluhrgPost, Tag

POSTS_PER_PAGE = 20

tags = Tag.query.order_by(Tag.tag_name)


@app.route('/')
@app.route('/posts')
@app.route('/posts/<int:page>')
def index(page=1):
    entries = BluhrgPost.query.paginate(page, POSTS_PER_PAGE, False).items
    return render_template('main.html', entries=entries, tags=tags)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


def get_or_create(session, model, **kwargs):
    '''Get or create a db object '''
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


@app.route('/add', methods=['POST'])
def bluhrg_post():
    print request.form['title'], request.form['content'], request.form['tags']
    bluhrg_post = BluhrgPost(title=request.form['title'],
                             content=request.form['content'])
    tags = request.form['tags'].strip().replace(" ", "").split(',')
    for tag in tags:
        tagToAdd = get_or_create(db.session, Tag, tag_name=tag)
        bluhrg_post.tags.append(tagToAdd)

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


@app.route('/search/tags/<string:tag_name>')
def tag_search(tag_name):
    filtered_enteries = BluhrgPost.query.filter(
                        BluhrgPost.tags.any(tag_name=tag_name))
    return render_template('main.html', entries=filtered_enteries, tags=tags)


@app.route('/search/title/', methods=['GET', 'POST'])
def title_search():
    filtered_enteries = BluhrgPost.query.filter(
                        BluhrgPost.title.ilike("%" + request.form['title'] + "%")
    )
    return render_template('main.html', entries=filtered_enteries, tags=tags)


if __name__ == "__main__":
    app.run()
