from http.client import HTTPException
from flask import Flask, render_template, jsonify,redirect
from flask_cors import CORS
from settings import config,here

from .models import db,User
from zhsz_api.controllers import auth
from zhsz_api.extensions import cors,lm,bcrypt,oid
import os
from .controllers import api_blue


def create_app():

    app = Flask(
        __name__,
        static_folder=os.path.join(here,'dist'),
        static_url_path='/'
        # template_folder=FRONTEND_FOLD
        # ER
    )
    print("静态文件夹路径:",os.path.join(here,'dist'))
    
    app.config['JSON_AS_ASCII'] = False
    #app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"
    app.config.from_object(config)
    #app的额外扩展
    db.init_app(app)
    #csrfp.init_app(app)
    CORS(app, resources=r'/*')
    bcrypt.init_app(app)
    oid.init_app(app)
    lm.init_app(app)

    @lm.user_loader
    def load_user(uid):
        return User.query.get(uid)

    @app.route('/')
    def index():
        return redirect("index.html")

    #测试
    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template('index.html'),404

    #注册登录注册的蓝图
    app.register_blueprint(api_blue)
    # print("前端地址: http://127.0.0.1:5000/index.html")

    return app


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return jsonify({'status': 'error', 'description': exc.description}), exc.code
