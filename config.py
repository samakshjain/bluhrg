# @Author: Samaksh Jain <ybl>
# @Date:   Wednesday, July 6th 2016, 9:17:28 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Monday, July 11th 2016, 11:23:32 am(IST)
# @License: MIT


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = 'blahblahbluhrg'
    CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
