# @Author: Samaksh Jain <ybl>
# @Date:   Sunday, July 10th 2016, 7:45:54 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Monday, July 11th 2016, 10:59:45 am(IST)
# @License: MIT


from flask import Blueprint, render_template, abort, request, \
                  send_from_directory, jsonify
from jinja2 import TemplateNotFound
from bluhrg.models import BluhrgPost, Tag
import os

PER_PAGE = 20

main = Blueprint('main', __name__, template_folder='templates')


# retrives favicon from static folder
@main.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(os.path.join(os.getcwd(), 'static'),
                                   'favicon.ico',
                                   mimetype='image/vnd.microsoft.icon')
    except TemplateNotFound:
        abort(404)


# index/main route to show all posts
@main.route('/')
@main.route('/posts')
@main.route('/posts/<int:page>')
def index(page=1):
    tags = Tag.query.order_by(Tag.tag_name)
    entries = BluhrgPost.query.paginate(page, PER_PAGE, False)
    return render_template('main/main.html', entries=entries, tags=tags)


# Probably un-needed metadata route that returns the number all total posts
@main.route('/metadata')
def get_metadata():
    try:
        entries = BluhrgPost.query.all()
        total = len(entries)
        return jsonify(total_posts=total)
    except TemplateNotFound:
        abort(404)


# Route to search by tags
@main.route('/search/tags/<string:tag_name>')
def tag_search(tag_name):
    try:
        tags = Tag.query.order_by(Tag.tag_name)
        filtered_enteries = BluhrgPost.query.filter(
                            BluhrgPost.tags.any(tag_name=tag_name))
        return render_template('main/main.html', entries=filtered_enteries,
                               tags=tags)
    except TemplateNotFound:
        abort(404)


# Route to search by title
@main.route('/search/title', methods=['GET', 'POST'])
def title_search():
    try:
        tags = Tag.query.order_by(Tag.tag_name)
        filtered_enteries = BluhrgPost.query.filter(
                            BluhrgPost.title.ilike("%" + request.form['title']
                                                   + "%")
        )
        return render_template('main/main.html', entries=filtered_enteries,
                               tags=tags)
    except TemplateNotFound:
        abort(404)
