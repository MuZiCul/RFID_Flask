import re

from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify

from config.decorators import login_required
from config.exts import db, mail
from config.models import ConfigModel, UserModel
from utils.captchas import getCaptchaPic
from flask_mail import Message

bp = Blueprint('general', __name__, url_prefix='/')


@bp.route('/getCaptchaImg', methods=['POST'])
def getCaptchaImg():
    file_name, coding = getCaptchaPic(request.form.get('coding'))
    return jsonify({'code': 200, 'src': file_name, 'coding': coding})


@bp.route('/notice_setting', methods=['GET', 'POST'])
@login_required
def notice_setting():
    config_ = ConfigModel.query.filter_by(id=1).first()
    data = {'Inventory_notification_thresholds': config_.Inventory_notification_thresholds,
            'notification': config_.notification, 'mail_server': config_.mail_server, 'mail_port': config_.mail_port,
            'mail_use_tls': config_.mail_use_tls,
            'mail_use_ssl': config_.mail_use_ssl, 'mail_debug': config_.mail_debug,
            'mail_username': config_.mail_username,
            'mail_password': config_.mail_password,
            'mail_default_sender': config_.mail_default_sender, }
    return render_template('notice_setting.html', data=data)


@bp.route('/change_notification_data', methods=['GET', 'POST'])
@login_required
def change_notification_data():
    thresholds = request.form.get('thresholds')
    notification = request.form.get('notification')
    check_interval = request.form.get('check_interval')
    notice_config = ConfigModel.query.filter_by(id=1).first()
    notice_config.Inventory_notification_thresholds = thresholds
    notice_config.notification = notification
    notice_config.check_interval = check_interval
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/email_notice_users', methods=['GET', 'POST'])
@login_required
def email_notice_users():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    data = UserModel.query.filter_by(mail_notice=1).order_by(db.text('-create_date')).paginate(page, limit,
                                                                                               error_out=False)
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


@bp.route('/add_notice_user', methods=['GET', 'POST'])
@login_required
def add_notice_user():
    return render_template('add_notice_user.html')


@bp.route('/add_notice_user_data', methods=['GET', 'POST'])
@login_required
def add_notice_user_data():
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
        if i.mail_notice != 1:
            dit = {'id': i.id
                , 'username': i.username
                , 'email': i.email
                , 'sex': i.sex
                , 'phone': i.phone
                , 'mail_notice': i.mail_notice
                , 'type': 'admin' if i.type == 1 else 'other'
                , 'create_date': str(i.create_date)}
            data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': total, 'data': data_list}
    return dic


@bp.route('/set_mail_notice_user', methods=['GET', 'POST'])
@login_required
def set_mail_notice_user():
    id_ = request.args.get('id')
    notice = UserModel.query.filter_by(id=id_).first()
    if not notice:
        return jsonify({'code': 400, 'msg': 'FAIL'})
    notice.mail_notice = 1
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/unset_mail_notice_user', methods=['GET', 'POST'])
@login_required
def unset_mail_notice_user():
    id_ = request.args.get('id')
    notice = UserModel.query.filter_by(id=id_).first()
    if not notice:
        return jsonify({'code': 400, 'msg': 'FAIL'})
    notice.mail_notice = 0
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/test_email', methods=['GET', 'POST'])
@login_required
def test_email():
    mail_config = ConfigModel.query.filter_by(id=1).first()
    test_email_account = mail_config.mail_test_account
    if is_valid_email(test_email_account):
        email = test_email_account.replace(' ', '')
        if not is_valid_email(email):
            return jsonify({'code': 400, 'msg': '发件邮箱地址有误'})
        message = Message(subject='测试邮件',
                          recipients=[email],
                          body=f'本邮件为测试邮件，请勿回复！')
        mail.send(message)
        return jsonify({'code': 200, 'msg': 'SUCCESS'})
    else:
        return jsonify({'code': 400, 'msg': '测试收件邮箱地址有误'})


def is_valid_email(email):
    if email is None:
        return False
    # 邮箱正则表达式，简单版（不完全严格）
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # 使用match方法进行匹配
    match = re.match(pattern, email)

    # 如果匹配成功，则返回True，否则返回False
    return bool(match)
