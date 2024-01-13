import os

from flask import Flask, session, g, render_template
from flask_migrate import Migrate

from config import config
from blueprints import user_bp, general_bp, inventory_bp
from config.decorators import login_required
from config.exts import redis_client, db
from config.models import UserModel

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)
redis_client.init_app(app)
app.register_blueprint(user_bp)
app.register_blueprint(general_bp)
app.register_blueprint(inventory_bp)
app.config['UPLOAD_PATH'] = os.path.join(os.path.dirname(__file__), 'file')
# user_infos = [{'id': 0, 'name': 'test', 'pwd': 'test'},{'id': 1, 'name': 'tes1', 'pwd': 'tes1'}]
# import json
#
# # 将字典序列化为JSON字符串
# json_str = json.dumps(user_infos)
#
# # 将JSON字符串写入文件
# with open('config/user_info.json', 'w') as f:
#     f.write(json_str)




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
            # # 读取JSON文件并反序列化为字典
            # with open('config/user_info.json', 'r') as f:
            #     user_infos = json.load(f)
            #
            # # 根据id查询用户信息
            # for user_info in user_infos:
            #     if user_info['id'] == user_id:
            #         g.user = user_info
            #     else:
            #         g.user = ''

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


if __name__ == '__main__':
    app.run()
