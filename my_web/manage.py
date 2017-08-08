#coding=utf-8
#!/usr/bin/env/ python

import os 
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User,Role,Content

app=create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

#注册回调函数，方便导入数据库
def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Content=Content )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# __name__是python内置环境变量，当文件被直接执行时为__main__，被导入执行的时候为模块名
if __name__ == '__main__':
	#app.run(debug=True)
	manager.run()

