# @Author: Samaksh Jain <ybl>
# @Date:   Friday, July 8th 2016, 1:29:43 am(IST)
# @Email:  samakshjain@live.com
# @Last modified by:   ybl
# @Last modified time: Friday, July 8th 2016, 1:43:21 am(IST)
# @License: MIT


import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
