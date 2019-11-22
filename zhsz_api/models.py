from zhsz_api.extensions import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db=SQLAlchemy()

class User(db.Model, UserMixin):
    '''
    用户模型
    '''
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        password = bcrypt.generate_password_hash(password)
        kwargs['password'] = password
        super(User, self).__init__(**kwargs)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def to_json(self):
        return {'id': self.id, 'username': self.username}

'''
#计算机工程技术学院
class College_of_computer_engineering_technology(db.Model,UserMixin):
    __tablename__ = 'computer_engineering'
    primary_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    style_id = db.Column(db.String(50), nullable=True)  # 不能以学号为主键，因为在17级第一学期和第二学期的时候，同一个人会发生主键冲突
    stu_name = db.Column(db.String(100))
    political_edu = db.Column(db.Float)
    physical_heal = db.Column(db.Float)
    innovation_entrep = db.Column(db.Float)
    technical_skills = db.Column(db.Float)
    volunte = db.Column(db.Float)
    human_art = db.Column(db.Float)
    zh_theory = db.Column(db.Float)
    score = db.Column(db.Float)
    GPA = db.Column(db.Float)
    zh_score = db.Column(db.Float)
    gk_class = db.Column(db.String(100))
    grade = db.Column(db.String(50))  # 年度 比如这个表是2018年度的
    semester = db.Column(db.String(50))  # 学期
    year = db.Column(db.String(50))  # 年级比如 17大数据1班，那么就是2017级
'''

#大数据与人工智能
class Bigtable(db.Model,UserMixin):
    #__tablename__='bigdata_ai'
    __tablename__ = 'zhsz'
    primary_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    style_id=db.Column(db.String(50),nullable=True)  #不能以学号为主键，因为在17级第一学期和第二学期的时候，同一个人会发生主键冲突
    stu_name=db.Column(db.String(100))
    political_edu=db.Column(db.Float)
    physical_heal=db.Column(db.Float)
    innovation_entrep=db.Column(db.Float)
    technical_skills=db.Column(db.Float)
    volunte=db.Column(db.Float)
    human_art=db.Column(db.Float)
    zh_theory=db.Column(db.Float)
    score=db.Column(db.Float)
    GPA=db.Column(db.Float)
    zh_score=db.Column(db.Float)
    gk_class=db.Column(db.String(100))
    grade=db.Column(db.String(50))  #年度 比如这个表是2018年度的
    semester=db.Column(db.String(50))  #学期
    year = db.Column(db.String(50))   #年级比如 17大数据1班，那么就是2017级
    college=db.Column(db.String(50))