from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app, celery
from admin import db
from production import *

try:
    from local_settings import *
except Exception:
    pass

app = create_app(ENV)
migrate = Migrate(app, db)

# 让python支持命令行工作
manager = Manager(app)

manager.add_command("runserver",
                    Server(host='0.0.0.0',
                           port=12341,
                           ))
manager.add_command("db", MigrateCommand)


if __name__ == '__main__':
    manager.run()
