import os

from zhsz_api import create_app
from flask_script import Manager,Server
from flask_migrate import MigrateCommand,Migrate
from zhsz_api.models import db,User
app=create_app()

migrate=Migrate(app,db)

manager=Manager(app=app)
manager.add_command("server",Server())
manager.add_command("db",MigrateCommand)

#自定义命令, 修改用户密码
@manager.option('-u','--user',dest='user')
@manager.option('-p','--password',dest='password')
def passwd(user,password):
    from zhsz_api.controllers.auth import alterPassword
    print(user,password)
    result = alterPassword(user,password,checkOld=False)
    print("修改密码结果:",result)

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User)


if __name__ == '__main__':
    manager.run()
    # vs code 调试时使用
    # app.run(host='0.0.0.0')


