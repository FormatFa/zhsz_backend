from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user
from zhsz_api.models import User, db
from zhsz_api.forms import RegisterForm, LoginForm
from zhsz_api.extensions import bcrypt
from . import api_blue
from utils.api import api_result


@api_blue.route('/auth/register', methods=['POST'])
def register():
    user_data = request.get_json()
    print(user_data)
    form = RegisterForm(data=user_data)
    if form.validate():
        user = User(username=user_data['username'], password=user_data['password'])
        db.session.add(user)
        db.session.commit()
        return api_result(0,msg="注册成功")
    return api_result(-1,data=form.errors,msg="注册失败")


@api_blue.route('/auth/login', methods=['POST'])
def login():
    user_data = request.get_json()
    form = LoginForm(data=user_data)
    if form.validate():
        user = form.get_user()
        login_user(user, remember=form.remember.data)
        return api_result(0,msg="登录成功",data=user.to_json())

    return api_result(-1,msg="登录失败",data=form.errors)

# 修改密码，为了方便，从下面的路由里提取出来了
def alterPassword(username,password,checkOld=True,old_password=''):
    print('修改密码',username,password,old_password)
    user = User.query.filter(User.username ==username).first()
    if user == None:
        return {
             'code':-1,
            'msg':'用户不存在'
        }
    if  checkOld and  not bcrypt.check_password_hash(user.password.encode(), old_password):
        return {
            'code':-1,
            'msg':'原密码错误'
        }
    user.password = bcrypt.generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    return {
            'code':0,
            'msg':'修改成功'
        }

@api_blue.route('/auth/login/alterPassword', methods=['POST'])
def alter():
    formdata = request.json
    if len(formdata['password'])<8:
        return jsonify({
            'code': -1,
            'msg': '密码长度至少为8个'
        })
    if formdata['password'] != formdata['password2']:
        return api_result(
            -1,
            msg='两个密码不一样'
        )
    result = alterPassword( formdata['username'], formdata['password'],checkOld=True,old_password=formdata['old_password'] )
    # 退出登录
    logout()
    return api_result(result['code'],msg=result['msg'])
    


@api_blue.route('/auth/session')
def get_session():
    if not current_user.is_authenticated:
        return api_result(-1,"用户未登录")
    return api_result(0,data= current_user.to_json())
    # jsonify({'status': 'success', 'user': current_user.to_json()})


@api_blue.route('/auth/logout')
def logout():
    logout_user()
    return api_result(0,"退出成功")
