from flask import Flask, current_app, g, request, session, make_response, render_template, redirect, abort, \
    render_template_string, url_for, flash

import constants

app = Flask(__name__)

#消息闪现需要用到session，jinja2考虑安全问题需要提供一个字符串当密钥，随机即可：
app.secret_key = 'absdfbccc-sdf'

# 为模板引擎添加扩展，支持break\continue语法
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# #请求钩子:
# @app.before_first_request
# def first_request():
#     print('before_first_request')       #仅第一个请求到达前执行
#
#
# @app.before_request
# def before_reqest():
#     print('before_reqest')      #每次请求到达前
#
#
# @app.after_request
# def after_request(resp):    #因为是请求后，所以需要返回一个response(响应)
#     print('after-requst')
#     return resp


#全局变量g
@app.before_request
def before_request():
    g.user= 'zhangsan'


@app.context_processor
def inject_const():
    """ 为模板上下文添加新的对象 """
    return dict({
        'constants': constants
    })


#url_for全局函数：
@app.route('/')
def index():
    # 从模板文件得到HTML
    print(url_for('index'))     #不加_external，显示局部url
    print(url_for('mine', _external=True))      #加_external，显示完整url
    return render_template('index.html')

    # 打印当前应用
    # print(current_app)
    # return "welcome"

    # 从字符串得到HTML
    # html = """
    #         <!DOCTYPE html>
    # <html lang="en">
    # <head>
    #     <meta charset="UTF-8">
    #     <title>Title</title>
    # </head>
    # <body>
    #     <h3>欢迎html</h3>
    # </body>
    # </html>
    #     """
    # return render_template_string(html)


#全局变量g的使用
@app.route('/m')
def mine():
    return render_template('mine.html')


@app.route('/hello/')       #默认url也是要配置的，不然参数不填会报错
@app.route('/hello/<username>')     #装饰器添加路由(更加推荐)
def hello(username='Marvin'):   #可设置默认值
    return 'hello,{}'.format(username)


@app.route('/test')
def test():
    # rest =  '找不到了', 403, {
    #     'user_id': 'abc123'
    # }
    # rest['token'] = 'cccc'
    # return rest

    # 构造一个响应对象
    # resp = make_response(
    #     '这是一个测试页面',
    #     404
    # )
    # resp.headers['token'] = 'my token'
    # return resp

    # 使用重定向
    # return redirect('/html')

    print('业务逻辑...')
    # 用户IP地址黑名单
    ip_list = ['127.0.0.1']
    ip = '127.0.0.1'
    if ip in ip_list:
        abort(403)  #指定错误处理
    return 'hello, success'


@app.errorhandler(404)
def not_found(err):
    """重写404"""
    # print(err)
    # return '您要的页面丢失了', 404, {
    #     'user_id': 'abc123'
    # }
    # #不写404的话浏览器的status是200


@app.route('/html')
def html():
    """ 显示HTML内容 """
    return render_template('test.html')


@app.route('/hello')
#视图函数
def hello_world():
    # #获取get请求中的参数：
    # page = request.args.get('page', None)   #没有就返回默认值None
    # print(page)
    # #get、post请求中的数据集合
    # name = request.values.get('name', None)     #values是两种请求都能获取
    # print(name)
    #
    # #获取请求头：
    # headers = request.headers
    # print(headers)

    #获取用户ip地址:
    ip = request.remote_addr
    print(ip)
    return 'Hello World!---'

# 获取路由规则
# print(app.url_map)


#模板中变量的使用：
@app.route('/var')
def var():
    # dict
    user_dict = {
        'username': 'zhangsan',
        'address.city': '广州',
        'address.town': '**镇'
    }
    # list
    list_city = [
        '广州',
        '深圳',
        '北京'
    ]
    list_obj = [
        {'user': 'lisi'},
        {'user': 'wangwu'},
    ]
    return render_template('var.html', user_dict=user_dict, list_city=list_city,
                           list_obj=list_obj)


#标签的使用
@app.route('/tag')
def use_tag():
    var = 1
    list_city = [
        # '广州',
        # '深圳',
        # '北京'
    ]
    list_obj = [
        {'user': 'lisi', 'passwd': '123456'},
        {'user': 'wangwu', 'passwd': '123456', 'sex': '1'},
    ]
    return render_template('tag.html', var=var,
                           list_city=list_city,
                           list_obj=list_obj)


@app.route('/filter')
def use_filter():
    """ 使用过滤器 """
    hello = 'hello, lucy'
    var = None
    html = '<h2>hello</h2>'
    phone = '13500000000'
    return render_template('use_filter.html', hello=hello,
                           var=var,
                           html=html,
                           phone=phone)


#自定义过滤器:
@app.template_filter('phone_format')
def phone_format(phone_no):
    """ 手机号格式化 """
    return phone_no[0:3] + '***'


@app.route('/gf')
def g_func():
    """ 模板全局函数的使用 """
    for i in range(10):
        print(i)
    return render_template('gf.html')


#模板的继承：
@app.route('/son')
def son():
    return render_template('son.html')


@app.route('/tips')
def tips():
    flash('欢迎回来', 'success')    #加入类型
    flash('警告你一下', 'error')
    return redirect('/message')
    # return render_template('tips.html')


@app.route('/message')
def message():
    """ 消息闪现的展示 """
    return render_template('message.html')
