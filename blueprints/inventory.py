from flask import Blueprint, render_template, redirect, g, url_for, request, flash, session, jsonify

from config.decorators import login_required
from config.exts import db
from config.models import InboundModel, OutboundModel, InventoryModel, ConfigModel, StockModel
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
    stock = StockModel.query.filter_by(rfid=notice.rfid).first()
    if notice.num!=stock.num:
        return jsonify({'code': 400, 'msg': '该货物已全部或部分出库，不允许修改！'})
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
    if not num.isdigit() or not kg.isdigit():
        return jsonify({'code': 400, 'msg': '数量和重量必须为数字！'})
    user = InboundModel.query.filter_by(id=id_).first()
    if user.rfid != rfid:
        if not check_rfid(rfid):
            return jsonify({'code': 400, 'msg': 'RFID已存在！'})
    stock = StockModel.query.filter_by(rfid=rfid).first()
    if user.num!=stock.num:
        return jsonify({'code': 400, 'msg': '该货物已全部或部分出库，不允许修改！'})
    stock.state = state
    stock.rfid = rfid
    stock.num = num
    stock.batch = batch
    stock.lm = lm
    stock.diameter = diameter
    stock.kg = kg

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
    if not check_rfid(rfid):
        return jsonify({'code': 400, 'msg': 'RFID已存在！'})
    if not num.isdigit() or not kg.isdigit():
        return jsonify({'code': 400, 'msg': '数量和重量必须为数字！'})
    user = InboundModel(rfid=rfid, num=num, batch=batch, state=state, lm=lm, diameter=diameter, kg=kg,
                        warehouse=warehouse)
    stock = StockModel(rfid=rfid, num=num, batch=batch, state=state, lm=lm, diameter=diameter, kg=kg,
                        warehouse=warehouse)
    db.session.add(stock)
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
    key = request.args.get('key', '')
    if key:
        data = OutboundModel.query.filter(OutboundModel.rfid.contains(key)).order_by(
            db.text('-create_date'))
        total = data.count()
    else:
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
            , 'state': i.state
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
            'diameter': user.diameter, 'kg': user.kg, 'state': user.state}
    return render_template('change_outbound.html', data=data)


@bp.route('/restocking', methods=['GET', 'POST'])
@login_required
def restocking():
    rfid = request.args.get('rfid')
    outb = OutboundModel.query.filter_by(rfid=rfid).first()
    outb.state = 3
    inb = InboundModel.query.filter_by(rfid=rfid).first()
    inb.state = 4
    stock = StockModel.query.filter_by(rfid=rfid).first()
    stock.num += int(outb.num)
    stock.kg += int(outb.kg)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/change_outbound_data', methods=['GET', 'POST'])
@login_required
def change_outbound_data():
    id_ = request.form.get('id')
    num = request.form.get('num')
    batch = request.form.get('batch')
    lm = request.form.get('lm')
    diameter = request.form.get('diameter')
    kg = request.form.get('kg')
    state = request.form.get('state')
    if not num.isdigit() or not kg.isdigit():
        return jsonify({'code': 400, 'msg': '数量和重量必须为数字！'})
    user = OutboundModel.query.filter_by(id=id_).first()
    stock = StockModel.query.filter_by(rfid=user.rfid).first()
    stock.state = state
    stock.num = int(user.num)+int(stock.num)-int(num)
    stock.batch = batch
    stock.lm = lm
    stock.diameter = diameter
    stock.kg = int(user.kg)+int(stock.kg)-int(kg)

    user.state = state
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
    stock = StockModel.query.filter_by(rfid=rfid).first()
    if not stock:
        return jsonify({'code': 400, 'msg': 'RFID不存在'})
    num = request.form.get('num')
    batch = request.form.get('batch')
    lm = request.form.get('lm')
    diameter = request.form.get('diameter')
    kg = request.form.get('kg')
    if not num.isdigit() or not kg.isdigit():
        return jsonify({'code': 400, 'msg': '数量和重量必须为数字！'})
    if int(stock.num) < int(num) or int(stock.kg) < int(kg):
        return jsonify({'code': 400, 'msg': '库存不足'})
    if int(stock.num) > int(num):
        state = 2
        stock.state = 5
        stock.num = int(stock.num) - int(num)
        stock.kg = int(stock.kg) - int(kg)
    else:
        state = 1
        stock.state = 6
        stock.num = 0
        stock.kg = 0
    user = OutboundModel(rfid=rfid, num=num, batch=batch, lm=lm, diameter=diameter, kg=kg, state=state)
    db.session.add(user)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'SUCCESS'})


@bp.route('/inventory_check', methods=['GET', 'POST'])
@login_required
def inventory_check():
    num = Calculate_inventory()
    Inventory = InventoryModel(num=num)
    db.session.add(Inventory)
    db.session.commit()
    return render_template('inventory_check.html')


def Calculate_inventory():
    stock = StockModel.query.all()
    num = 0
    for i in stock:
        num += int(i.num)
    return num


@bp.route('/inventory_check_data', methods=['GET', 'POST'])
@login_required
def inventory_check_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    key = request.args.get('key', '')
    if key:
        data = InventoryModel.query.filter(InventoryModel.rfid.contains(key)).order_by(
            db.text('-create_date'))
        total = data.count()
    else:
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


@bp.route('/location_manage', methods=['GET', 'POST'])
@login_required
def location_manage():
    return render_template('location_manage.html', total=Calculate_inventory())


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
        dit = {'rfid': i.rfid
            , 'num': i.num
            , 'warehouse': i.warehouse
            , 'create_date': str(i.create_date)}
        data_list.append(dit)
    dic = {'code': 0, 'msg': 'SUCCESS', 'count': total, 'data': data_list}
    return dic


@bp.route('/get_rfid_data', methods=['GET', 'POST'])
@login_required
def get_rfid_data():
    rfid = request.args.get('rfid')
    stock = StockModel.query.filter_by(rfid=rfid).first()
    if not stock:
        return jsonify({'code': 400, 'msg': 'RFID不存在'})
    return jsonify({'code': 200, 'rfid': rfid, 'num': stock.num, 'batch': stock.batch, 'kg': stock.kg, 'diameter': stock.diameter, 'lm': stock.lm, 'msg': 'SUCCESS'})


@bp.route('/check_rfid_data', methods=['GET', 'POST'])
@login_required
def check_rfid_data():
    rfid = request.args.get('rfid')
    if check_rfid(rfid):
        return jsonify({'code': 200, 'msg': 'RFID可用'})
    else:
        return jsonify({'code': 400, 'msg': 'RFID已存在'})


def check_rfid(rfid):
    stock = StockModel.query.filter_by(rfid=rfid).first()
    if stock:
        return False
    else:
        return True


@bp.route('/stock_check', methods=['GET', 'POST'])
@login_required
def stock_check():
    return render_template('stock_manage.html', )


@bp.route('/stock_check_data', methods=['GET', 'POST'])
@login_required
def stock_check_data():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 50))
    key = request.args.get('key', '')
    if key:
        data = StockModel.query.filter(StockModel.rfid.contains(key)).order_by(
            db.text('-create_date'))
        total = data.count()
    else:
        data = StockModel.query.order_by(db.text('-create_date')).paginate(page, limit, error_out=False)
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

