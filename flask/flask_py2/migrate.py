# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(
        __name__,
        static_url_path = '/python', #默认是static
        static_folder = './static', # 静态文件目录
        template_folder = './templates'
)

manage = Manager(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/flask_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



# 创建数据库工具对象
db = SQLAlchemy(app)


#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app, db)

#manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manage.add_command('db', MigrateCommand)

# 创建表
class User(db.Model):

    __tablename__ = "tbl_users"  # 指定数据库名
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id"))



# user.role

class Role(db.Model):

    __tablename__ = 'tbl_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship("User", backref='role')# 这个是属性不是数据库字段，不加backref获取的就是id

    def __repr__(self):

        return 'object name %s' % self.name



if __name__ == "__main__":


    #清楚当前数据库中的所有数据,小心使用
    #db.drop_all()
    #创建表
    #db.create_all()

    #app.run(debug=True)
    #ro1 = Role(name='admin')
    #ro2 = Role(name='user')
    #db.session.add_all([ro1, ro2])
    #db.session.commit()
    #us1 = User(name='wang', password='123456', role_id=ro1.id)
    #us2 = User(name='zhang', password='201512', role_id=ro2.id)
    #us3 = User(name='chen', password='987654', role_id=ro2.id)
    #us4 = User(name='zhou',  password='456789', role_id=ro1.id)
    #db.session.add_all([us1, us2, us3, us4])
    #db.session.commit()
    manage.run()