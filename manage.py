# -*- coding: UTF-8 -*-
# !/usr/bin/python
# 桂声后台脚本管理文件:支持命令行启动、数据库迁移和更新

import os
from app import create_app, db

from app.models import User,Role, Permission, NewsPost,OriginPost,ZonghePost,Comment

from flask.ext.script import Manager, Shell

from flask.ext.migrate import Migrate, MigrateCommand

#-------------------编码设置---------------------------
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#------------------------------------------------------

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():

    return dict(app=app, db=db, User=User,Role=Role,Permission=Permission, NewsPost=NewsPost,OriginPost=OriginPost,ZonghePost=ZonghePost,Comment=Comment)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
