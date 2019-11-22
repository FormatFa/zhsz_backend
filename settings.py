import os

import pymysql
from sqlalchemy import create_engine

here = os.path.dirname(__file__)
class Config(object):
    SECRET_KEY = '\x83u\x1ah\xd1\xa2\xb2\xac\xbf\xa5A\xba\x83[C."\xdc\xd9\xe0\xe5N\xaf\x80'

    RECAPTCHA_PUBLIC_KEY='ADASDGSDVGFS56465FSD1F2SDF452'

    PECAPTCHA_PRIVATE_KEY='ADASDGSDVGFS87487-8615546221'

    DEBUG = True
    
    database="mysql"

    #数据库是mysql时的配置


    DATABASE = 'GK_ZH'
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = 'root'
    HOST = 'localhost'
    PORT = 3306
    

    conn = pymysql.connect(
        host=HOST,  # 你的主机IP
        port=PORT,  # 主机端口，不能加双引号
        user=USERNAME,  # MySQL用户
        password=PASSWORD,  # MySQL密码
        charset='utf8'  # 使用的编码格式，不能使用  utf-8 ，不能加多一个横杠
    )
    db = conn.cursor()  # 创建光标

    db.execute("create database if not exists GK_ZH character set utf8;")  # 创建数据库
    db.execute("use GK_ZH;")
    conn.commit()  # 一定要进行事务更新
    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER,USERNAME,PASSWORD, HOST, PORT, DATABASE)
    #sqlite 时有问题
    # #数据库为sqlite 时的 配置
    # elif database=="sqlite":
    #     SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/bigdata/Documents/zhsz/zhsz_flask/zhsz.db'
    #     conn = sqlite3.connect("C:/Users/bigdata/Documents/zhsz/zhsz_flask/zhsz.db")
    #     db = conn.cursor()

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
    


# 生产环境
class ProConfig(Config):
    pass

## 开发环境
class DevConfig(Config):

   pass
    #DB_CONNECT_STRING = 'mysql+pymysql://root:root@localhost:3306/test2?charset=utf8'







class FileConfig():
    need_word={
                '学号':'style_id',
                '姓名':'stu_name',
                '思想政治':'political_edu',
                '身心健康':'physical_heal',
                '创新创业':'innovation_entrep',
                '技术技能':'technical_skills',
                '志愿服务':'volunte',
                '人文艺术':'human_art',
                '综合素质理论':'zh_theory',
                '总分':'score',
                'GPA(教务处提供）':'GPA',
                '综合成绩':'zh_score',
                '班级':'gk_class',
                '年级':'grade',
                '学期': 'semester',
                '年度':'year',
                '学院':'college'
    }

    key=list(need_word.keys())

    need_columns = [
        ['学号', '姓名', '思想政治', '身心健康', '创新创业', '技术技能', '志愿服务', '人文艺术', '综合素质理论', '总分', 'GPA(教务处提供）', '综合素质测评分（P2)', '排名','班级'],
        ['学号', '姓名', '思想政治', '身心健康', '创新创业', '技术技能', '志愿服务', '人文艺术', '综合素质理论', '总分', 'GPA(教务处提供）', '综合成绩', '排名', '班级'],
        ['学号', '姓名', '思想政治', '身心健康', '创新创业', '技术技能', '志愿服务', '人文艺术', '综合素质理论', '总分', 'GPA(教务处导出）', '综合素质测评分', '排名','班级'],
    ]



config = DevConfig()


