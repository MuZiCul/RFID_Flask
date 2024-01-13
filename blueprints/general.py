from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify


from utils.captchas import getCaptchaPic

bp = Blueprint('general', __name__, url_prefix='/')


@bp.route('/getCaptchaImg', methods=['POST'])
def getCaptchaImg():
    file_name, coding = getCaptchaPic(request.form.get('coding'))
    return jsonify({'code': 200, 'src': file_name, 'coding': coding})
