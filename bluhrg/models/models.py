# @Last modified time: Sunday, July 10th 2016, 9:40:36 pm(IST)
# @Author: Samaksh Jain <ybl>
# @Date:   Friday, July 8th 2016, 1:42:12 am(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @License: MIT


from sqlalchemy.ext.hybrid import hybrid_property
from bluhrg import db

# Helper table for tagging
tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('bluhrg_post_id', db.Integer,
                          db.ForeignKey('blag.id'))
                )


class BluhrgPost(db.Model):
    __tablename__ = 'blag'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('blag', lazy='dynamic'))

    def __init__(self, *initial_data, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String())

    @hybrid_property
    def post_count(self):
        return len(self.blag.all())

    def __init__(self, *initial_data, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])

    def __repr__(self):
        return '<tag {}>'.format(self.id)
