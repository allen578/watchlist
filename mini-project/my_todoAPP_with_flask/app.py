name = 'Allen'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy   #导入扩展类
import os
import sys

WIN = sys.platform.startswith('win') 
if WIN: # 如果是windows系统
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)  # 初始化app
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'
db = SQLAlchemy(app) #初始化扩展，传入程序实例 app

# ...

# 模板上下文处理函数, 避免每次都要输入用户名
@app.context_processor
def inject_user(): # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)
    

# @app.route('/')
# def index():
#     user = User.query.first()
#     movies = Movie.query.all()
#     return render_template('index.html', user=user, movies=movies)

from flask import request, url_for, redirect, flash

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是POST请求
        # 获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60 :
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year) # 创建记录
        db.session.add(movie)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


# 创建数据库模型
class User(db.Model):  # 表名将会是user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字
    
class Movie(db.Model): # 表名将会是movie
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


'''自定义命令initdb'''

import click

@app.cli.command()   # 注册为命令，可以传入name参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.') # 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")  # 输出提示信息


'''创建自定义命令forge'''
import click 
# 直接执行 flask forge 就可以将这些数据放到数据库中
@app.cli.command()
def forge():
    """Generate fake data"""
    db.create_all()
    
    # 全局的两个变量移动到这个函数内
    name = 'Allen'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]   
    
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo('Done.')
   
# 404报错页面函数    
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html'), 404  # 返回模板和状态码

# 编辑电影条目
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash("Invalid input.")
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        
        movie.title = title  # 更新标题
        movie.year = year    # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


# 删除条目
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受POST请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))

