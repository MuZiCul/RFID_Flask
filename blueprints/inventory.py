from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify

from config.decorators import login_required
from config.exts import db
from config.models import InboundModel, OutboundModel, InventoryModel, ConfigModel
from utils.captchas import getCaptchaPic

bp = Blueprint('inventory', __name__, url_prefix='/')


@bp.route('/inbound_manage', methods=['GET', 'POST'])
@login_required
def inbound_manage():
    return render_template('inbound_manage.html')


@bp.route('/inbound_manage_data', methods=['GET', 'POST'])
@login_required
def inbound_manage_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    data = InboundModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
    total = data.total
    data = data.items
    data_list = []
    for i in data:
        dit = {'id': i.id
            , 'rfid': i.rfid
            , 'num': i.num
            , 'lm': i.lm
            , 'diameter': i.diameter
            , 'kg': i.kg
            , 'batch': i.batch
            , 'state': i.state
            , 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': total, 'data': data_list}
    return dic


@bp.route('/inbound_del', methods=['GET', 'POST'])
@login_required
def inbound_del():
    id_ = request.args.get('id')
    notice = InboundModel.query.filter_by(id=id_).first()
    if not notice:
        return jsonify({'code': 400, 'msg': 'FAIL'})
    db.session.delete(notice)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/change_inbound/<id>', methods=['GET', 'POST'])
@login_required
def change_inbound(id):
    user = InboundModel.query.filter_by(id=id).first()
    data = {'rfid': user.rfid, 'num': user.num, 'batch': user.batch, 'state': user.state, 'id': user.id, 'lm': user.lm,
            'diameter': user.diameter, 'kg': user.kg}
    return render_template('change_inbound.html', data=data)


@bp.route('/change_inbound_data', methods=['GET', 'POST'])
@login_required
def change_inbound_data():
    id_ = request.form.get('id')
    rfid = request.form.get('rfid')
    num = request.form.get('num')
    batch = request.form.get('batch')
    state = int(request.form.get('state'))
    lm = request.form.get('lm')
    diameter = request.form.get('diameter')
    kg = request.form.get('kg')
    warehouse = request.form.get('warehouse')
    user = InboundModel.query.filter_by(id=id_).first()
    user.rfid = rfid
    user.num = num
    user.batch = batch
    user.state = state
    user.lm = lm
    user.diameter = diameter
    user.kg = kg
    user.warehouse = warehouse
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/add_inbound_html', methods=['GET', 'POST'])
@login_required
def add_inbound_html():
    return render_template('add_inbound.html')


@bp.route('/add_inbound_data', methods=['GET', 'POST'])
@login_required
def add_inbound_data():
    rfid = request.form.get('rfid').replace(" ", "")
    num = request.form.get('num')
    batch = request.form.get('batch')
    state = int(request.form.get('state'))
    lm = request.form.get('lm')
    diameter = request.form.get('diameter')
    kg = request.form.get('kg')
    warehouse = request.form.get('warehouse')
    user = InboundModel(rfid=rfid, num=num, batch=batch, state=state, lm=lm, diameter=diameter, kg=kg, warehouse=warehouse)
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/outbound_manage', methods=['GET', 'POST'])
@login_required
def outbound_manage():
    return render_template('outbound_manage.html')


@bp.route('/outbound_manage_data', methods=['GET', 'POST'])
@login_required
def outbound_manage_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    data = OutboundModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
    total = data.total
    data = data.items
    data_list = []
    for i in data:
        dit = {'id': i.id
            , 'rfid': i.rfid
            , 'num': i.num
            , 'lm': i.lm
            , 'diameter': i.diameter
            , 'kg': i.kg
            , 'batch': i.batch
            , 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': total, 'data': data_list}
    return dic


@bp.route('/outbound_del', methods=['GET', 'POST'])
@login_required
def outbound_del():
    id_ = request.args.get('id')
    notice = OutboundModel.query.filter_by(id=id_).first()
    if not notice:
        return jsonify({'code': 400, 'msg': 'FAIL'})
    db.session.delete(notice)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/change_outbound/<id>', methods=['GET', 'POST'])
@login_required
def change_outbound(id):
    user = OutboundModel.query.filter_by(id=id).first()
    data = {'rfid': user.rfid, 'num': user.num, 'batch': user.batch, 'id': user.id, 'lm': user.lm,
            'diameter': user.diameter, 'kg': user.kg}
    return render_template('change_outbound.html', data=data)


@bp.route('/change_outbound_data', methods=['GET', 'POST'])
@login_required
def change_outbound_data():
    id_ = request.form.get('id')
    rfid = request.form.get('rfid')
    num = request.form.get('num')
    batch = request.form.get('batch')
    lm = request.form.get('lm')
    diameter = request.form.get('diameter')
    kg = request.form.get('kg')
    user = OutboundModel.query.filter_by(id=id_).first()
    user.rfid = rfid
    user.num = num
    user.batch = batch
    user.lm = lm
    user.diameter = diameter
    user.kg = kg
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/add_outbound_html', methods=['GET', 'POST'])
@login_required
def add_outbound_html():
    return render_template('add_outbound.html')


@bp.route('/add_outbound_data', methods=['GET', 'POST'])
@login_required
def add_outbound_data():
    rfid = request.form.get('rfid').replace(" ", "")
    num = request.form.get('num')
    batch = request.form.get('batch')
    lm = request.form.get('lm')
    diameter = request.form.get('diameter')
    kg = request.form.get('kg')
    user = OutboundModel(rfid=rfid, num=num, batch=batch, lm=lm, diameter=diameter, kg=kg)
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/inventory_check', methods=['GET', 'POST'])
@login_required
def inventory_check():
    return render_template('inventory_check.html')


@bp.route('/inventory_check_data', methods=['GET', 'POST'])
@login_required
def inventory_check_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    data = InventoryModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
    total = data.total
    data = data.items
    data_list = []
    for i in data:
        dit = {'id': i.id
            , 'num': i.num
            , 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': total, 'data': data_list}
    return dic


@bp.route('/notice_setting', methods=['GET', 'POST'])
@login_required
def notice_setting():
    user = ConfigModel.query.filter_by(id=1).first()
    data = {'Inventory_notification_thresholds': user.Inventory_notification_thresholds,
            'notification': user.notification}
    return render_template('notice_setting.html', data=data)


@bp.route('/change_notification_data', methods=['GET', 'POST'])
@login_required
def change_notification_data():
    thresholds = request.form.get('thresholds')
    notification = request.form.get('notification')
    user = ConfigModel.query.filter_by(id=1).first()
    user.Inventory_notification_thresholds = thresholds
    user.notification = notification
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/location_manage', methods=['GET', 'POST'])
@login_required
def location_manage():
    return render_template('location_manage.html')


@bp.route('/location_manage_data', methods=['GET', 'POST'])
@login_required
def location_manage_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    key = request.args.get('key', '')
    if key:
        data = InboundModel.query.filter(InboundModel.rfid.contains(key)).order_by(
            db.text('-create_date'))
        total = data.count()
    else:
        data = InboundModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
        total = data.total
        data = data.items
    data_list = []
    for i in data:
        dit = {'id': i.id
            , 'rfid': i.rfid
            , 'warehouse': i.warehouse
            , 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': total, 'data': data_list}
    return dic
