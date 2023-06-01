from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from watchlist import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # 用户名
    password_hash = db.Column(db.String(20)) # 密码散列值
    
    # 该方法生成密码，接受密码作为参数
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password) # 将生成的密码保持到对应字段
    
    # 该方法验证密码，接受密码作为参数
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) # 返回布尔值

class Movie(db.Model): # 表名将会是movie
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
