# @Author: Samaksh Jain <ybl>
# @Date:   Saturday, July 9th 2016, 12:45:33 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Monday, July 11th 2016, 11:44:49 am(IST)
# @License: MIT


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
                    help='maximum number of posts to fetch (defaults to all)')
args = parser.parse_args()
args.type = 'text' if args.type is None else args.type
args.blog = 'fuckyeahexistentialism' if args.blog is None else args.blog
args.count = 1 if args.count is None else args.count

print 'Getting ' + args.type + ' posts from ' + args.blog + '.tumblr.com...'


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
    posts = client.posts(args.blog + '.tumblr.com', type=args.type, limit=20,
                         filter='html', offset=offset)
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
