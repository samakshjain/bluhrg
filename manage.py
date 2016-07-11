# @Author: Samaksh Jain <ybl>
# @Date:   Friday, July 8th 2016, 1:29:43 am(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Sunday, July 10th 2016, 11:02:34 pm(IST)
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

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print "hello"
    for rule in app.url_map.iter_rules():
        print rule
    manager.run()
