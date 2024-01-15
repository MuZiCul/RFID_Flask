import os

from flask import Flask, session, g, render_template, request, jsonify
from flask_migrate import Migrate

from config import config
from blueprints import user_bp, general_bp, inventory_bp
from config.decorators import login_required
from config.exts import redis_client, db, mail
from config.models import UserModel, ConfigModel
from flask_apscheduler import APScheduler

from utils.captchas import delCaptcha

app = Flask(__name__)
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)
redis_client.init_app(app)
scheduler = APScheduler()
scheduler.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(general_bp)
app.register_blueprint(inventory_bp)
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), 'file')
scheduler.start()


def load_config_from_database():
    # Get mail configuration from the database (replace this with your actual implementation)
    mail_config = ConfigModel.query.filter_by(id=1).first()

    # Update Flask app configuration with the retrieved mail configuration
    app.config['MAIL_SERVER'] = mail_config.mail_server
    app.config['MAIL_PORT'] = mail_config.mail_port
    app.config['MAIL_USE_TLS'] = mail_config.mail_use_tls
    app.config['MAIL_USE_SSL'] = mail_config.mail_use_ssl
    app.config['MAIL_DEBUG'] = mail_config.mail_debug
    app.config['MAIL_USERNAME'] = mail_config.mail_username
    app.config['MAIL_PASSWORD'] = mail_config.mail_password
    app.config['MAIL_DEFAULT_SENDER'] = mail_config.mail_default_sender

    # Initialize the Mail object with the app
    mail.init_app(app)


@app.route('/mail_setting', methods=['POST'])
@login_required
def mail_setting():
    mail_server = request.form.get('mail_server')
    mail_port = request.form.get('mail_port')
    mail_use_tls = request.form.get('mail_use_tls')
    mail_use_ssl = request.form.get('mail_use_ssl')
    mail_debug = request.form.get('mail_debug')
    mail_username = request.form.get('mail_username')
    mail_password = request.form.get('mail_password')
    mail_default_sender = request.form.get('mail_default_sender')
    mail_test_account = request.form.get('mail_test_account')
    user = ConfigModel.query.filter_by(id=1).first()
    user.mail_server = mail_server
    user.mail_port = mail_port
    user.mail_use_tls = mail_use_tls
    user.mail_use_ssl = mail_use_ssl
    user.mail_username = mail_username
    user.mail_debug = mail_debug
    user.mail_password = mail_password
    user.mail_default_sender = mail_default_sender
    user.mail_test_account = mail_test_account
    db.session.commit()
    load_config_from_database()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


# Register the load_config_from_database function to run before the first request
@app.before_first_request
def before_first_request():
    load_config_from_database()
    delCaptcha()


@app.before_request
def before_request():
    user_id = session.get('userid')
    g.DATABASE_DATA = 0
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            if user:
                g.user = user
            else:
                g.user = ''
        except Exception as e:
            print(e)
            g.user = ''


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


# 定时清理验证码图片
@scheduler.task('interval', id='delCaptcha', minutes=10)
def check_net():
    try:
        with scheduler.app.app_context():
            delCaptcha()
    finally:
        pass


if __name__ == '__main__':
    app.run()
