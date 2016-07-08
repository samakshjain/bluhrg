import pytumblr
from app import db
from models import *
client = pytumblr.TumblrRestClient('E5aSN7BmN5pEgJrqlc3D79R94voOKw59SkRCkVyGaXQ8811xxL')

end_of_posts = True
offset = 0
while(end_of_posts):
    posts = client.posts('fuckyeahexistentialism.tumblr.com', type='text', limit=20, filter='html', offset=offset)
    print "Get", str(offset), posts['total_posts'], offset != posts['total_posts']
    if (offset != posts['total_posts']):
        for post in posts['posts']:
            tags = ''
            for tag in post['tags']:
                tags = tags + tag + ', '
            data = {
                'title': post['title'],
                'content': post['body'],
                'tags': tags
            }
            bluhrg_post = BluhrgPost(data)
            db.session.add(bluhrg_post)
        offset = offset + len(posts['posts'])
    else:
        end_of_posts = False
db.session.commit()
