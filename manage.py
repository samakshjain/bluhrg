# @Author: Samaksh Jain <ybl>
# @Date:   Friday, July 8th 2016, 1:29:43 am(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Monday, July 11th 2016, 12:44:54 pm(IST)
# @License: MIT

from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bluhrg import db
from bluhrg.blueprints import admin, main
import os

# Flask config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
# registering blueprints
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(main)


@manager.command
def getTumblrPosts():
    import pytumblr
    from manage import db
    from bluhrg.models import BluhrgPost, Tag
    import argparse
    import os

    client = pytumblr.TumblrRestClient(os.environ['TUMBLR_KEY'])
    description = 'Get <type | [Text, Photo, Quote, Link, Chat, Audio, Video,'\
                  'Answer]> posts from <blog>.tumblr.com'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-b', '--blog',
                        help="name of the blog (e.g. fuckyeahexistentialism)")
    parser.add_argument('-t', '--type', help="type of the posts to fetch")
    parser.add_argument('-c', '--count',
                        help='maximum number of posts to fetch \
                        (defaults to all)')
    args = parser.parse_args()
    args.type = 'text' if args.type is None else args.type
    args.blog = 'fuckyeahexistentialism' if args.blog is None else args.blog
    args.count = 1 if args.count is None else args.count

    print 'Getting ' + args.type + ' posts from ' + args.blog + \
        '.tumblr.com...'

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

    posts_remaining = True
    offset = 0
    while(posts_remaining):
        posts = client.posts(args.blog + '.tumblr.com', type=args.type,
                             limit=20, filter='html', offset=offset)
        print "GET", str(offset), '/', posts['total_posts']
        if (offset != posts['total_posts']):
            for post in posts['posts']:
                data = {
                    'title': post['title'],
                    'content': post['body']
                }
                bluhrg_post = BluhrgPost(data)

                # Make a csv string of tags
                for tag in post['tags']:
                    tagToAdd = get_or_create(db.session, Tag, tag_name=tag)
                    bluhrg_post.tags.append(tagToAdd)

                # Add posts to session
                db.session.add(bluhrg_post)
            offset = offset + len(posts['posts'])
        else:
            posts_remaining = False

    # commit all posts to db
    db.session.commit()


manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print rule
    manager.run()
