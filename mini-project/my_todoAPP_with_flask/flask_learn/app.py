from flask import Flask

app = Flask(__name__)  # 实例化Flask类来创建一个程序对象app

# @app.route('/')   # 第一个参数是URL规则字符串，这里的 / 指的是根地址
# def hello():
#     # 返回值作为响应的主体，默认会被浏览器当作HTML格式解析
#     return 'Welcome to My WatchList!'

@app.route('/home/index')
@app.route('/home')
@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
















'''
如果将文件名改成了别的名字，比如hello.py，那么执行flask run就会报错。
因为Flask默认会假设你把程序存储在名为 app.py 或 wsgi.py 的文件中
如要更改，就要设置系统环境变量FLASK_APP来告诉Flask你要启动哪个程序
export FLASK_APP=hello.py
在windows中使用set命令
set FLASK_APP=hello.py
'''
