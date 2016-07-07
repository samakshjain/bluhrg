# @Author: Samaksh Jain <ybl>
# @Date:   Friday, July 8th 2016, 1:42:12 am(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Friday, July 8th 2016, 1:43:17 am(IST)
# @License: MIT


from app import db

class BluhrgPost(db.Model):
    __tablename__ = 'blag'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    tags = db.Column(db.String())

    def __init__(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags

    def __repr__(self):
        return '<id {}>'.format(self.id)
