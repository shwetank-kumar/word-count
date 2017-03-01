import os
from wordcounter import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import current_app
from config import config

app = create_app('docker')
manager = Manager(app)
migrate = Migrate(app, db)

@manager.option('-n', '--name', help='Your app name')
def celeryworker(name):
    celery_args = ['celery', 'worker', '-n', name, '-C', '--autoscale=10,1', '--without-gossip']
    with app.app_context():
        return celery_main(celery_args)


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
        manager.run()
