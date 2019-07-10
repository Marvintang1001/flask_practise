import os

from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# from forms import LoginForm, UserForm, UserAvatarForm
import pymysql

from flask_form.forms import UserForm, UserAvatarForm, LoginForm

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['WTF_CSRF_SECRET_KEY'] = 'abcd12321'     #表单自己用的密钥
app.config['SECRET_KEY'] = 'CCSDFS'     #表单也用到session所以用到它
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), 'medias')
db = SQLAlchemy(app)


class User(db.Model):
    """ 用户ID """
    __tablename__ = 'weibo_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, default=0)


@app.route('/form')
def page_form():
    """ form表单渲染 """
    form = LoginForm()
    return render_template('form.html', form=form)


#提交表单需要支持get和post方法
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    """ 手动添加用户信息 """
    # form = UserForm(csrf_enabled=False)
    form = UserForm()
    if form.validate_on_submit():
        # 获取表单数据
        username = form.username.data
        password = form.password.data
        birth_date = form.birth_date.data
        age = form.age.data
        # 保存到数据
        user = User(username=username,
                    password=password,
                    birth_date=birth_date,
                    age=age)
        db.session.add(user)
        db.session.commit()
        # 提示/跳转
        print('添加成功')
        return redirect(url_for('index'))   #url_for 是地址解析
    else:
        print('表单验证未通过')
        print(form.errors)
    return render_template('add_user.html', form=form)


@app.route('/img/upload', methods=['GET', 'POST'])
def img_upload():           #post提交文件上传
    """ 图片上传 """
    # base_dir = os.path.join(os.path.dirname(__file__), 'medias')
    if request.method == 'POST':
        # 取文件
        files = request.files
        file1 = files['file1']  #字典
        file2 = files['file2']
        # 保存文件
        if file1:
            # 文件名称格式化
            filename = secure_filename(file1.filename)      #安全文件名：空格变成下划线
            # file_name = os.path.join(base_dir, filename)
            file_name = os.path.join(app.config['UPLOAD_PATH'], filename)
            file1.save(file_name)
    return render_template('img_upload.html')


@app.route('/avatar/upload', methods=['GET', 'POST'])
def avatar_upload():
    """ 头像上传 """
    form = UserAvatarForm()
    if form.validate_on_submit():
        f = form.avatar.data
        filename = secure_filename(f.filename)
        file_name = os.path.join(app.config['UPLOAD_PATH'], filename)
        f.save(file_name)
        print('上传头像成功')
    else:
        print(form.errors)
    return render_template('avatar_upload.html', form=form)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
