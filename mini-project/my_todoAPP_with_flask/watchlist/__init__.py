import os
import sys
from flask_sqlalchemy import SQLAlchemy   #导入扩展类
from flask import Flask
from flask_login import LoginManager

WIN = sys.platform.startswith('win') 
if WIN: # 如果是windows系统
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)  # 初始化app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app) #初始化扩展，传入程序实例 app

login_manager = LoginManager(app) # 实例化扩展类


@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户ID作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user # 返回用户对象

login_manager.login_view = 'login'


@app.context_processor
def inject_user(): # 函数名可以随意修改
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)

from watchlist import views, errors, commands

