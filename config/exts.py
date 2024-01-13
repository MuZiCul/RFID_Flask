from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from flask_redis import FlaskRedis


redis_client = FlaskRedis()
db = SQLAlchemy()
mail = Mail()

