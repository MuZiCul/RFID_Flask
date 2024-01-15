import datetime
import json
import random
import re
import string

from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify
from flask_mail import Message

from config import config
from config.decorators import login_required
from config.exts import redis_client, db
from werkzeug.security import generate_password_hash, check_password_hash

from config.models import UserModel
from utils.Aescrypt import Aescrypt
from utils.captchas import getCaptchaPic

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def login():
    CaptchaPic, coding = getCaptchaPic('')
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        captcha = request.form.get('captcha')
        if not redis_client.keys(captcha.lower()):
            error = '验证码有误'
            CaptchaPic, coding = getCaptchaPic('')
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=account)
        user_username = UserModel.query.filter_by(email=account).first()
        if not user_username:
            error = '账户不存在'
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=account)
        if user_username and check_password_hash(user_username.password, password):
            session['userid'] = user_username.id
            return redirect(url_for('index'))
        else:
            error = '账户或密码有误'
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=account)
    return render_template('login.html', CaptchaPic=CaptchaPic, coding=coding)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if hasattr(g, 'user'):
        try:
            print(g.user.id)
            return redirect(url_for('index'))
        except Exception as e:
            session.clear()
            CaptchaPic, coding = getCaptchaPic('')
            return render_template('login.html', CaptchaPic=CaptchaPic, coding=coding)
    if request.method == 'GET':
        CaptchaPic, coding = getCaptchaPic('')
        return render_template('login.html', CaptchaPic=CaptchaPic, coding=coding)
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        captcha = request.form.get('captcha')
        if not redis_client.keys(captcha.lower()):
            error = '验证码有误！'
            CaptchaPic, coding = getCaptchaPic('')
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=email)
        if UserModel.query.filter_by(email=email).first():
            error = '该邮箱已注册！'
            CaptchaPic, coding = getCaptchaPic('')
            return render_template('login.html', error=error, CaptchaPic=CaptchaPic, coding=coding, account=email)
        user = UserModel(email=email, username=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        user_username = UserModel.query.filter_by(email=email).first()
        session['userid'] = user_username.id
        return redirect(url_for('index'))


# @login_required
# @bp.route('/items_info', methods=['GET', 'POST'])
# def items_info():
#     page = int(request.args.get('page', 1))
#     limit = int(request.args.get('limit', 50))
#     with open('config/item_info.json', 'r') as f:
#         item_infos = json.load(f)

    # 根据id查询用户信息
    # for item_info in item_infos:
    #     if item_info['name'] == account:
    #         user_username = user_info
    # data = SearchModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
    # data_list = []
    # for i in data.items:
    #     dit = {'id': i.id,
    #            'user_id': i.user_id,
    #            'key': i.key,
    #            'times': i.times,
    #            'create_date': i.create_date,
    #            }
    #     data_list.append(dit)
    # dic = {'code': 0, 'msg': 'SUCCESS', 'count': 3, 'data': item_infos}
    # return dic


# @bp.route('/tags_info', methods=['GET', 'POST'])
# def tags_info():
#     page = int(request.args.get('page', 1))
#     limit = int(request.args.get('limit', 50))
#     with open('config/tag_info.json', 'r') as f:
#         tag_infos = json.load(f)

    # # 根据id查询用户信息
    # for tag_info in tag_infos:
    #     if tag_info['name'] == account:
    #         user_username = user_info
    # data = SearchModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
    # data_list = []
    # for i in data.items:
    #     dit = {'id': i.id,
    #            'user_id': i.user_id,
    #            'key': i.key,
    #            'times': i.times,
    #            'create_date': i.create_date,
    #            }
    #     data_list.append(dit)
    # dic = {'code': 0, 'msg': 'SUCCESS', 'count': 3, 'data': tag_infos}
    # return dic


# @login_required
# @bp.route('/items_html', methods=['GET', 'POST'])
# def items_html():
#     return render_template('items_info.html')
#
#
# @bp.route('/tags_html', methods=['GET', 'POST'])
# def tags_html():
#     return render_template('tag_info.html')


@bp.route('/logoff')
def logoff():
    session.clear()
    return redirect(url_for('user.login'))


# @bp.route('/email_login', methods=['GET', 'POST'])
# def email_login():
#     email = request.form.get('email')
#     if not is_valid_email(email):
#         return jsonify({'code': 400, 'msg': '邮箱格式不正确'})
#     getCaptchaTimeReturn = getCaptchaTime(email)
#     if getCaptchaTimeReturn:
#         return getCaptchaTimeReturn
#     user_email = [user_dict for user_dict in config.user if user_dict.get('email') == email][0]
#     if not user_email:
#         return jsonify({'code': 400, 'msg': '邮箱未注册'})
#     email = email.replace(' ', '')
#     session['email'] = email
#     captcha = ''.join(random.sample(string.digits, 6))
#     message = Message(subject='【开发者登录】验证码',
#                       recipients=[email],
#                       body=f'【开发者管理】您的本次验证码是：{captcha}，请勿告知任何人，本次验证码将在几秒后失效！')
#     mail.send(message)
#     captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
#     AescryptOb = Aescrypt()
#     captcha = generate_password_hash(AescryptOb.encryption(captcha))
#     if captcha_model:
#         captcha_model.captcha = captcha
#         captcha_model.type = 1
#         captcha_model.create_time = datetime.datetime.now()
#         db.session.commit()
#     else:
#         captcha_model = EmailCaptchaModel(email=email, captcha=captcha, type=1)
#         db.session.add(captcha_model)
#         db.session.commit()
#     return jsonify({'code': 200})
#
#
# @bp.route('/check_captcha', methods=['GET', 'POST'])
# def check_captcha():
#     from datetime import datetime
#     captcha = request.form.get('captcha')
#     if 'email' not in session or not captcha:
#         return render_template('no_pwd_login.html', type=1)
#     captcha_model = EmailCaptchaModel.query.filter_by(email=session['email']).first()
#     AescryptOb = Aescrypt()
#     if not captcha_model:
#         return render_template('no_pwd_login.html', error='请重新获取验证码', type=2)
#     else:
#         time_1 = captcha_model.create_time
#         time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         time_1_struct = datetime.strptime(str(time_1), "%Y-%m-%d %H:%M:%S")
#         time_2_struct = datetime.strptime(str(time_2), "%Y-%m-%d %H:%M:%S")
#         total_seconds = (time_2_struct - time_1_struct).total_seconds()
#         captcha_model.type = 0
#         db.session.commit()
#         data = AescryptOb.encryption(captcha)
#         if total_seconds > 60:
#             return render_template('no_pwd_login.html', error='验证码已过期', type=2)
#         elif not check_password_hash(captcha_model.captcha, data):
#             return render_template('no_pwd_login.html', error='验证码不正确', type=2)
#         else:
#             session['userid'] = UserModel.query.filter_by(email=session['email']).first().id
#             return redirect(url_for('index'))
#
#
# def getCaptchaTime(email):
#     captcha_model = EmailCaptchaModel.query.filter_by(email=email).order_by(db.text('-create_time')).first()
#     if captcha_model:
#         time_1 = captcha_model.create_time
#         time_2 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         time_1_struct = datetime.datetime.strptime(str(time_1), "%Y-%m-%d %H:%M:%S")
#         time_2_struct = datetime.datetime.strptime(str(time_2), "%Y-%m-%d %H:%M:%S")
#         total_seconds = (time_2_struct - time_1_struct).total_seconds()
#         if total_seconds < 60:
#             return jsonify({'code': 400, 'message': '获取验证码过于频繁，请稍后再试！'})
#         else:
#             return False
#
#
# def is_valid_email(email):
#     # 邮箱的正则表达式模式
#     pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#
#     # 使用re.match函数进行匹配
#     match = re.match(pattern, email)
#
#     if match:
#         return True
#     else:
#         return False


@bp.route('/user_manage', methods=['GET', 'POST'])
@login_required
def user_manage():
    return render_template('user_manage.html', url='/user_manage_data')


@bp.route('/user_manage_data', methods=['GET', 'POST'])
@login_required
def user_manage_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    key = request.args.get('key', '')
    if key:
        data = UserModel.query.filter(UserModel.username.contains(key) | UserModel.email.contains(key)).order_by(
            db.text('-create_date'))
        total = data.count()
    else:
        data = UserModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
        total = data.total
        data = data.items

    data_list = []
    for i in data:
        dit = {'id': i.id
            , 'username': i.username
            , 'email': i.email
            , 'sex': i.sex
            , 'phone': i.phone
            , 'type': 'admin' if i.type == 1 else 'other'
            , 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': total, 'data': data_list}
    return dic


@bp.route('/user_del', methods=['GET', 'POST'])
@login_required
def user_del():
    id_ = request.args.get('id')
    notice = UserModel.query.filter_by(id=id_).first()
    if not notice:
        return jsonify({'code': 400, 'msg': 'FAIL'})
    db.session.delete(notice)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/user_add', methods=['GET', 'POST'])
@login_required
def user_add():
    return render_template('user_add.html')

@bp.route('/user_register', methods=['GET', 'POST'])
@login_required
def user_register():
    username = request.form.get('username')
    email = request.form.get('email')
    user = UserModel.query.filter_by(email=email).first()
    if user:
        return jsonify({'code': 400, 'msg': 'This email has been registered!'})
    password = request.form.get('password')
    type = request.form.get('type')
    sex = request.form.get('sex')
    phone = request.form.get('phone')
    if not username or not email or not password or not type or not sex or not phone:
        return jsonify({'code': 400, 'msg': 'Fill in the incomplete!'})
    user = UserModel(email=email, username=username, type=type, sex=int(sex), phone=phone,
                     password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/change_user/<id_>', methods=['GET', 'POST'])
@login_required
def change_user(id_):
    user = UserModel.query.filter_by(id=id_).first()
    data = {'username': user.username, 'email': user.email, 'phone': user.phone,
            'id': id_, 'sex': user.sex, 'type': user.type}
    return render_template('user_change.html', data=data)


@bp.route('/change_user_data', methods=['GET', 'POST'])
@login_required
def change_user_data():
    username = request.form.get('username')
    id_ = request.form.get('id')
    email = request.form.get('email')
    sex = int(request.form.get('sex'))
    password = request.form.get('password')
    type = int(request.form.get('type'))
    phone = request.form.get('phone')
    user = UserModel.query.filter_by(id=id_).first()
    user.username = username
    if password:
        user.password = generate_password_hash(password)
    user.email = email
    user.sex = sex
    user.type = type
    user.phone = phone
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


