# @Author: Samaksh Jain <ybl>
# @Date:   Sunday, July 10th 2016, 7:45:48 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Monday, July 11th 2016, 12:12:04 am(IST)
# @License: MIT


from flask import Blueprint, render_template, abort, request, flash, \
                  redirect, url_for
from jinja2 import TemplateNotFound
from bluhrg.models import BluhrgPost, Tag
from bluhrg import db

admin = Blueprint('admin', __name__)


# Get or create a model from/in the db
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


# Route to admin panel
@admin.route('/dashboard')
def dashboard():
    try:
        return render_template('admin/admin.html')
    except TemplateNotFound:
        abort(404)


# Route to add a bluhrg_post
@admin.route('/api/add', methods=['POST'])
def bluhrg_post():
    print request.form['title'], request.form['content'], request.form['tags']
    try:
        bluhrg_post = BluhrgPost(title=request.form['title'],
                                 content=request.form['content'])
        tags = request.form['tags'].strip().replace(" ", "").split(',')
        for tag in tags:
            tagToAdd = get_or_create(db.session, Tag, tag_name=tag)
            bluhrg_post.tags.append(tagToAdd)

        db.session.add(bluhrg_post)
        db.session.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('main.index'))
    except TemplateNotFound:
        abort(404)
