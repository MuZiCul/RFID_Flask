from config.exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), default='')
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, default=0)
    sex = db.Column(db.Integer, default=0)
    mail_notice = db.Column(db.Integer, default=0)
    phone = db.Column(db.String(100), default='')
    create_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class InboundModel(db.Model):
    __tablename__ = "inbound"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rfid = db.Column(db.String(200), default='')
    num = db.Column(db.String(200), default='')
    batch = db.Column(db.String(200), default='')
    state = db.Column(db.Integer, default='')
    lm = db.Column(db.String(200), default='')
    diameter = db.Column(db.String(200), default='')
    kg = db.Column(db.String(200), default='')
    warehouse = db.Column(db.String(200), default='')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class OutboundModel(db.Model):
    __tablename__ = "outbound"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rfid = db.Column(db.String(200), default='')
    num = db.Column(db.String(200), default='')
    batch = db.Column(db.String(200), default='')
    lm = db.Column(db.String(200), default='')
    diameter = db.Column(db.String(200), default='')
    kg = db.Column(db.String(200), default='')
    state = db.Column(db.Integer, default=1)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class StockModel(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rfid = db.Column(db.String(200), default='')
    num = db.Column(db.String(200), default='')
    batch = db.Column(db.String(200), default='')
    state = db.Column(db.Integer, default='')
    lm = db.Column(db.String(200), default='')
    diameter = db.Column(db.String(200), default='')
    kg = db.Column(db.String(200), default='')
    warehouse = db.Column(db.String(200), default='')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class InventoryModel(db.Model):
    __tablename__ = "inventory"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num = db.Column(db.String(200), default='')
    create_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)



class ConfigModel(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Inventory_notification_thresholds = db.Column(db.Integer, default=0)
    notification = db.Column(db.Integer, default=0)
    mail_server = db.Column(db.String(200), default='')
    mail_port = db.Column(db.String(200), default='')
    mail_use_tls = db.Column(db.String(200), default='')
    mail_use_ssl = db.Column(db.String(200), default='')
    mail_debug = db.Column(db.String(200), default='')
    mail_username = db.Column(db.String(200), default='')
    mail_password = db.Column(db.String(200), default='')
    mail_default_sender = db.Column(db.String(200), default='')
    mail_test_account = db.Column(db.String(200), default='')
    check_interval = db.Column(db.Integer, default=0)
