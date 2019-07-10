import re

from django.forms import DateField, IntegerField
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError


# class LoginForm(FlaskForm):
#     """ 用户登录 """
#     username = StringField(label='用户名')
#     password = PasswordField(label='密码')
#
#     submit = SubmitField('登录')

def phone_required(form, field):
    """ 自定义的验证 """
    username = field.data
    # 强制用户名为手机号码
    pattern = r'^1[0-9]{10}$'
    if not re.search(pattern, username):
        raise ValidationError('请输入手机号码[公共部分]')
    return field


class LoginForm(FlaskForm):
    """ 用户登录 """
    username = StringField(label='用户名', validators=[
        phone_required
    ])
    password = PasswordField(label='密码')

    submit = SubmitField('登录')


class UserForm(FlaskForm):
    """ 新增用户 """
    # def __init__(self, csrf_enabled, *args, **kwargs):
    #     super().__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

    username = StringField(label='用户名')
    password = PasswordField(label='密码')

    # birth_date = DateField(label='生日')
    birth_date = DateField(label='生日', validators=[DataRequired('请输入生日')])  #内置表单验证器使用
    age = IntegerField(label='年龄')

    submit = SubmitField('新增')

  # def validate_username(self, field):
    #     username = field.data
    #     # 强制用户名为手机号码
    #     pattern = r'^1[0-9]{10}$'
    #     if not re.search(pattern, username):
    #         raise ValidationError('请输入手机号码')
    #     return field


class UserAvatarForm(FlaskForm):
    avatar = FileField(label='上传头像', validators=[
        FileRequired('请选择图片文件'),    #必须上传
        FileAllowed(['png'], '仅支持png')])  #必须是png
