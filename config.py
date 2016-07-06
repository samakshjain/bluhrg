# @Author: Samaksh Jain <ybl>
# @Date:   Wednesday, July 6th 2016, 9:17:28 pm(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Wednesday, July 6th 2016, 9:19:13 pm(IST)
# @License: MIT


import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DATABASE = 'bluhrg.db'
    SECRET_KEY = 'blahblahbluhrg'
    USERNAME = 'admin'
    PASSWORD = 'bluhrgadmin'
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
