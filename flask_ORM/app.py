from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pymysql  # 没有话，就pip安装

pymysql.install_as_MySQLdb()

app = Flask(__name__)

#配置数据库的连接参数
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:abcd1234@localhost/test_flask'


db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'weibo_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, default=0)


class UserAddress(db.Model):
    """ 用户地址 """
    __tablename__ = 'weibo_user_addr'

    id = db.Column(db.Integer, primary_key=True)
    addr = db.Column(db.String(64), nullable=False)
    #外键关联到weibo_user.id
    user_id = db.Column(db.Integer, db.ForeignKey('weibo_user.id'), nullable=False)
    #反向引用：可以通过user.address找到address
    user = db.relationship('User', backref=db.backref('address', lazy=True))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


@app.route('/user/<int:page>/')
def page_user(page):
    """ 分页操作 """
    page_size = 10   # 每一页10条数据
    page_data = User.query.paginate(page=page, per_page=page_size)
    return render_template('page_user.html', page_data=page_data)


## ORM学习
