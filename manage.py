import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application import appl, db

# application.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(appl, db)
manager = Manager(appl)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
