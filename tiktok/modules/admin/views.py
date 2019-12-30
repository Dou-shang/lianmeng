import time
import re
from werkzeug.utils import secure_filename
from . import admin_blu
from tiktok import db
from tiktok.modules.index import models
from flask import jsonify, request
from tiktok.modules.index.models import *
from tiktok.constants import RETCODE
from tiktok.utils import jwt_util


# 增
# 用户表_User
@admin_blu.route('/adduser')
def adminAddUser():
    try:
        user = User(
            phone="1332437752",
            openid= "hdssdhbfsdiubiusd",
            wxpic_url= "/root/fjdbid/sdjbsd",
            wxname= "pig",
            user_identity= "团长",
            user_all_money= "1000",
            user_y_money= "78",
            user_s_money= "36",
            user_icode="20",
            user_all_friend= "dsjfbskd",
            up_phone= "347738543y",
            alipay= "dsjbksdbjk",
            reg_time= "2019-04-19"
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(msg="ok")
    except:
        return jsonify(msg="error")
    
# 商品类别表_GoodsClas
@admin_blu.route('/addgoodcls', methods=['POST'])
def adminAddGCls():
    try:
        data = request.get_json()
    except:
        return jsonify(msg="no")
    goodstype = data.get("goodstype")
    classid = data.get("classid")

    if not all([goodstype,classid]):
        return jsonify(msg="no")

    try:
        good = GoodsClas(
            goodstype=goodstype,
            classid=classid
        )
        db.session.add(good)
        db.session.commit()
        return jsonify(msg="ok")
    except:
        return jsonify(msg="no")
# 商品表_Good
@admin_blu.route('/addgoods', methods=("POST",))
def adminAddGoods():
    # 获取表单
    try:
        data = request.form
    except:
        return jsonify(msg="no")
    f = request.files['pic']
    filename = f.filename
    dir_path = './tiktok/img/'
    path = 'https://api.ywcdy.com/img/'
    ext = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', filename)
    if len(ext) == 0:
        ext = filename
    else:
        ext = ext[0]

    file_name = str(int(time.time()))
    totalpath = dir_path+file_name+ext
    path = path+file_name+ext
    f.save(totalpath)

    goodsid = int(time.time())
    issuerphone = data.get("issuerphone")
    g_title = data.get("g_title")
    g_pic = path
    g_amount = data.get("g_amount")
    g_brokerage = data.get("g_brokerage")
    status = data.get("status")
    ambush = data.get("ambush")
    video_url = data.get("video_url")
    classid = data.get("classid")
    classid = int(classid)
    reg_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    issuerdate = reg_time.split(" ")[0]

    
    if not all([f,issuerphone,g_title,ambush,g_pic,g_amount,g_brokerage,status,video_url,classid]):
        return jsonify(msg="no")

    try:
        good = Good(
            goodsid=goodsid,
            issuerphone=issuerphone,
            g_title=g_title,
            g_pic=g_pic,
            g_amount=g_amount,
            g_brokerage=g_brokerage,
            status=status,
            ambush=ambush,
            video_url=video_url,
            classid=classid,
            issuerdate=issuerdate
        )
        db.session.add(good)
        db.session.commit()
        return jsonify(msg="ok")
    except:
        return jsonify(msg="no")
    
# 入驻资料表_Settle
@admin_blu.route('/stladd', methods=['POST'])
def adminAddSTLs():
    data = request.get_json()
    bringid = data.get("bringid")
    bringclass = data.get("bringclass")
    phone = data.get("phone")
    name = data.get("name")
    douyincode = data.get("douyincode")
    i_card = data.get("i_card")
    email = data.get("email")
    credit_code = data.get("credit_code")
    invitation = data.get("invitation")
    positive_pic = data.get("positive_pic")
    side_pic = data.get("side_pic")
    license = data.get("license")
    examine = data.get("examine")
    sub_date = data.get("sub_date")

    good = Settle(
        bringid=bringid,
        bringclass=bringclass,
        phone=phone,
        name=name,
        douyincode=douyincode,
        i_card=i_card,
        email=email,
        credit_code=credit_code,
        invitation=invitation,
        positive_pic=positive_pic,
        side_pic=side_pic,
        license=license,
        examine=examine,
        sub_date=sub_date
    )
    db.session.add(good)
    db.session.commit()
    return jsonify(msg="ok")
# 提现申请表_CashApply
# 佣金明细表_Brokerage
# 轮播图表_Wheel
@admin_blu.route('/whelladd', methods=['POST'])
def adminAddWhell():
    data = request.form
    # 上传图片
    f = request.files['pic']
    filename = secure_filename(f.filename)
    dir_path = './tiktok/img/'
    path = '/img/'
    ext = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', filename)[0]
    file_name = str(int(time.time()))
    totalpath = dir_path+file_name+ext
    path = path+file_name+ext
    f.save(totalpath)

    whell = models.Wheel(
        adress_pic=data.get('adress_pic'),
        url_pic=path
    )
    db.session.add(whell)
    db.session.commit()
    return jsonify(msg="ok")
# 公告表_Content
@admin_blu.route('/conadd', methods=['POST'])
def adminAddCon():
    data = request.get_json()
    content = data.get("content")

    good = Content(
        content=content
    )
    db.session.add(good)
    db.session.commit()
    return jsonify(msg="ok")
# 全局设置表_Global

# 删
# 管理员表_Superuser
# 用户表_User
# 商品类别表_GoodsClas
@admin_blu.route('/delgoodsclas/<classid>', methods=['DELETE'])
def DelGoodsClas(classid):
    classid = int(classid)
    goods_item = db.session.query(Good).all()
    goods_list = []
    if goods_item:
        for i in goods_item:
            goods_list.append(i.classid)
    else:
        goods_item = None
    if classid in goods_list:
        return jsonify(err_code=RETCODE.ERROR)

    try:
        query_item = db.session.query(GoodsClas).filter(GoodsClas.classid==classid).first()
        db.session.delete(query_item)
        db.session.commit()
        return jsonify(err_code=RETCODE.OK)
    except:
        return jsonify(err_code=RETCODE.ERROR)
    

# 商品表_Good
@admin_blu.route('/delgoods/<goods_id>', methods=("DELETE",))
def adminDelGoods(goods_id):
    good = db.session.query(Good).filter(Good.goodsid==goods_id).first()
    db.session.delete(good)
    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 入驻资料表_Settle
@admin_blu.route('/stldel/<id>', methods=['DELETE'])
def adminDelSTLs(id):
    whell = db.session.query(Settle).filter(Settle.id==id).first()
    db.session.delete(whell)
    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 提现申请表_CashApply
@admin_blu.route('/applydel/<cashid>', methods=("DELETE",))
def adminDelApply(cashid):
    apply = db.session.query(CashApply).filter(CashApply.cashid==cashid).first()
    db.session.delete(apply)
    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 佣金明细表_Brokerage
@admin_blu.route('/delbro/<id>', methods=("DELETE",))
def adminDelBro(id):
    bro = db.session.query(Brokerage).filter(Brokerage.id==id).first()
    db.session.delete(bro)
    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 轮播图表_Wheel
@admin_blu.route('/whelldel/<id>', methods=['DELETE'])
def adminDelWhell(id):
    whell = db.session.query(Wheel).filter(Wheel.id==id).first()
    db.session.delete(whell)
    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 公告表_Content
@admin_blu.route('/condel/<id>', methods=['DELETE'])
def adminConWhell(id):
    whell = db.session.query(Content).filter(Content.id==id).first()
    db.session.delete(whell)
    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 全局设置表_Global
@admin_blu.route('/delglb/<id>', methods=['DELETE'])
def adminGlbMod(id):
    whell = db.session.query(Global).filter(Global.id==id).first()
    db.session.delete(whell)
    db.session.commit()
    return jsonify(err_code=RETCODE.OK)

# 改
# 管理员表_Superuser
# 用户表_User
@admin_blu.route('/mod/<user_id>', methods=["PUT"])
def adminUpdateUser(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    data = request.get_json()

    phone = data.get("phone")
    avatarUrl = data.get("avatarUrl")
    nickname = data.get("nickname")
    user_identity = data.get("user_identity")
    user_all_money = data.get("user_all_money")
    user_y_money = data.get("user_y_money")
    user_s_money = data.get("user_s_money")
    user_icode = data.get("user_icode")
    user_all_friend = data.get("user_all_friend")
    up_phone = data.get("up_phone")
    alipay = data.get("alipay")
    reg_time = data.get("reg_time")

    user.phone = phone
    user.avatarUrl = avatarUrl
    user.nickname = nickname
    user.user_identity = user_identity
    user.user_all_money = user_all_money
    user.user_y_money = user_y_money
    user.user_s_money = user_s_money
    user.user_icode = user_icode
    user.user_all_friend = user_all_friend
    user.up_phone = up_phone
    user.alipay = alipay
    user.reg_time = reg_time

    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 商品类别表_GoodsClas
@admin_blu.route('modgoodcls/<classid>', methods=("PUT",))
def adminModGoodCLS(classid):
    cashid = int(classid)
    good = db.session.query(GoodsClas).filter_by(classid=classid).first()
    data = request.get_json()

    classid = data.get("classid")
    goodstype = data.get("goodstype")

    good.classid=classid
    good.goodstype=goodstype

    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 商品表_Good
@admin_blu.route('/modgoods/<goods_id>', methods=("PUT",))
def adminModGoods(goods_id):
    goods_id = int(goods_id)
    good = db.session.query(Good).filter_by(goodsid=goods_id).first()
    data = request.get_json()

    issuerphone = data.get('issuerphone')
    g_title = data.get('g_title')
    g_pic = data.get('g_pic')
    g_amount = data.get('g_amount')
    ambush = data.get('ambush')
    video_url = data.get('video_url')
    g_brokerage = data.get('g_brokerage')
    status = data.get('status')
    try:
        classname = data.get('classid')
        gc = db.session.query(GoodsClas).filter_by(goodstype=classname).first()
        classid = int(gc.classid)
    except:
        return jsonify(err_code=RETCODE.ERROR)
    reg_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    issuerdate = reg_time.split(" ")[0]

    good.issuerphone = issuerphone
    good.g_title = g_title
    good.g_pic = g_pic
    good.g_amount = g_amount
    good.g_brokerage = g_brokerage
    good.ambush = ambush
    good.video_url = video_url
    good.status = status
    good.classid = classid
    good.issuerdate = issuerdate

    db.session.commit()
    return jsonify(err_code=RETCODE.OK)
# 入驻资料表_Settle
@admin_blu.route('/stlmod/<id>', methods=("PUT",))
def adminModSTL(id):
    id = int(id)
    good = db.session.query(Settle).filter_by(id=id).first()
    data = request.get_json()

    bringid = data.get("bringid")
    bringclass = data.get("bringclass")
    phone = data.get("phone")
    name = data.get("name")
    douyincode = data.get("douyincode")
    i_card = data.get("i_card")
    email = data.get("email")
    credit_code = data.get("credit_code")
    invitation = data.get("invitation")
    positive_pic = data.get("positive_pic")
    side_pic = data.get("side_pic")
    license = data.get("license")
    examine = data.get("examine")
    sub_date = data.get("sub_date")

    good.bringid=bringid
    good.bringclass=bringclass
    good.phone=phone
    good.name=name
    good.douyincode=douyincode
    good.i_card=i_card
    good.email=email
    good.credit_code=credit_code
    good.invitation=invitation
    good.positive_pic=positive_pic
    good.side_pic=side_pic
    good.license=license
    good.examine=examine
    good.sub_date=sub_date

    db.session.commit()

    stl = db.session.query(Settle).filter(Settle.id==id).first()
    if stl.examine == '成功':
        user = db.session.query(User).filter(User.user_icode==invitation).first()
        if user:

            phone_u = user.phone
            reg_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            date1 = reg_time.split(" ")[0]
            gl = db.session.query(Global).first()
            g_money = int(gl.invite_money)
            u_money = int(user.user_all_money) + g_money
            user.user_all_money=u_money
            bro = Brokerage(phone=phone_u,getphone=stl.phone,operation=date1,brokerage_sum=g_money)
            db.session.add(bro)
            db.session.commit()
        else:
            return jsonify(err_code=RETCODE.ERROR)

    return jsonify(err_code=RETCODE.OK)
# 提现申请表_CashApply
@admin_blu.route('/modapply/<cashid>', methods=("PUT",))
def adminModApply(cashid):
    cashid = int(cashid)
    good = db.session.query(CashApply).filter_by(cashid=cashid).first()
    data = request.get_json()

    cashphone = data.get('cashphone')
    cashmoney = data.get('cashmoney')
    examine = data.get('examine')
    cash_date = data.get('cash_date')
    monkey_code = data.get('monkey_code')

    good.cashphone = cashphone
    good.cashmoney = cashmoney
    good.examine = examine
    good.cash_date = cash_date
    good.monkey_code = monkey_code

    db.session.commit()

    apply = db.session.query(CashApply).filter(CashApply.cashid==cashid).first()

    if apply.examine == '失败':
        phone = apply.cashphone
        cashmoney = int(cashmoney)
        user = db.session.query(User).filter(User.phone==phone).first()
        user_s_money = int(user.user_s_money)
        user_s_money -= cashmoney
        user.user_s_money = user_s_money
        db.session.commit()

    return jsonify(err_code=RETCODE.OK)
    
# 佣金明细表_Brokerage
@admin_blu.route('/modbrok/1/<id>', methods=("PUT",))
def adminModBrok(id):
    id = int(id)
    good = db.session.query(Brokerage).filter_by(id=id).first()
    data = request.get_json()

    phone = data.get('phone')
    brokerage_sum = data.get('brokerage_sum')
    operation = data.get('operation')
    getphone = data.get('getphone')

    good.phone = phone
    good.getphone = getphone
    good.brokerage_sum = brokerage_sum
    good.operation = operation

    db.session.commit()

    return jsonify(err_code=RETCODE.OK)
# 轮播图表_Wheel
# 公告表_Content
# 全局设置表_Global
@admin_blu.route('/modglb/<id>', methods=("PUT",))
def adminModGlb(id):
    id = int(id)
    good = db.session.query(Global).filter_by(id=id).first()
    data = request.get_json()

    cash_min = data.get("cash_min")
    task_num = data.get("task_num")
    invite_money = data.get("invite_money")

    good.cash_min=cash_min
    good.task_num=task_num
    good.invite_money=invite_money

    db.session.commit()

    return jsonify(err_code=RETCODE.OK)

# 查
# 管理员表_Superuser
@admin_blu.route('/auth', methods=("POST",))
def adminAuth():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        superuser = db.session.query(Superuser).filter(Superuser.username==username).first()
        token = superuser.token
        de_token = jwt_util.de_jwt(token)
        datax = {}
        if password == de_token['password']:
            datax = {
                'username':username,
                'user_id':superuser.id,
                'token':token
            }
        return jsonify({'error_code':0,'data':datax})
    except:
        return jsonify({
            'error_code': 1,
            'msg': '该用户不存在'
        })
# 用户表_User
@admin_blu.route('/users')
def adminUsers():
    try:
        page = request.args.get('pageNum')
        page = int(page)
    except Exception as e:
        page = 1
    current_page = 1
    total_page = 1
    paginate = db.session.query(User).paginate(page,RETCODE.PER_PAGE,False)
    users = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    user_list = []
    if users:
        for i in users:
            phone1 = i.phone
            b1 = db.session.query(Brokerage).filter(Brokerage.getphone == phone1).first()
            user = {
                "id":i.id,
                "phone":i.phone,
                "openid":i.openid,
                "avatarUrl":i.wxpic_url,
                "nickname":i.wxname,
                "user_identity":i.user_identity,
                "user_all_money":i.user_all_money,
                "user_y_money":str(int(i.user_all_money)-int(i.user_s_money)),
                "user_s_money":i.user_s_money,
                "user_icode":i.user_icode,
                "user_all_friend":i.user_all_friend,
                "up_phone":b1.phone if b1 else None,
                "alipay":i.alipay,
                "reg_time":i.reg_time
            }
            user_list.append(user)
    else:
        users = None
    users_data = {
        'user_list': user_list,
        'current_page':current_page,
        'total_page':total_page
    }
    return jsonify(data=users_data)
# 商品类别表_GoodsClas
@admin_blu.route('/goodcls')
def adminQueryGCls():
    whells = db.session.query(GoodsClas).all()
    whell_list = []
    if whells:
        for i in whells:
            whell = {
                "classid": i.classid,
                "goodstype": i.goodstype
            }
            whell_list.append(whell)
    else:
        whells = None
    apply_data = {
        'gcls_list': whell_list,
    }
    return jsonify(data=apply_data)
# 商品表_Good
@admin_blu.route('/querygoods')
def adminQueryGoods():
    try:
        page = request.args.get('pageNum')
        page = int(page)
    except Exception as e:
        page = 1
    current_page = 1
    total_page = 1
    paginate = db.session.query(
        Good.goodsid,
        Good.issuerphone,
        Good.g_title,
        Good.g_pic,
        Good.g_amount,
        Good.g_brokerage,
        Good.status,
        Good.ambush,
        Good.video_url,
        GoodsClas.goodstype,
        Good.issuerdate
    ).outerjoin(
        GoodsClas,
        Good.classid == GoodsClas.classid
    ).paginate(page,RETCODE.PER_PAGE,False)
    goods = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    goods_list = []
    if goods:
        for i in goods:
            user = {
                "goodsid": i.goodsid,
                "issuerphone": i.issuerphone,
                "g_title": i.g_title,
                "g_pic": i.g_pic,
                "g_amount": i.g_amount,
                "ambush": i.ambush,
                "video_url": i.video_url,
                "g_brokerage": i.g_brokerage,
                "status": i.status,
                "classid": i.goodstype,
                "issuerdate": i.issuerdate,
            }
            goods_list.append(user)
    else:
        goods = None
    goods_data = {
        'goods_list': goods_list,
        'current_page':current_page,
        'total_page':total_page
    }
    return jsonify(data=goods_data, err_code=RETCODE.OK)
# 入驻资料表_Settle
@admin_blu.route('/stl')
def adminQuerySTLs():
    try:
        page = request.args.get('pageNum')
        page = int(page)
    except Exception as e:
        page = 1
    current_page = 1
    total_page = 1

    paginate = db.session.query(
        Settle.id,
        Settle.bringid,
        Settle.phone,
        Settle.name,
        Settle.douyincode,
        Settle.i_card,
        Settle.email,
        Settle.credit_code,
        Settle.invitation,
        Settle.positive_pic,
        Settle.side_pic,
        Settle.license,
        Settle.examine,
        Settle.sub_date,
        User.user_identity
        ).outerjoin(
            User, 
            Settle.phone==User.phone
            ).distinct().paginate(page,RETCODE.PER_PAGE,False)
    whells = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    whell_list = []
    if whells:
        for i in whells:
            whell = {
                "id": i.id,
                "bringid": i.bringid,
                "bringclass": i.user_identity,
                "phone": i.phone,
                "name": i.name,
                "douyincode": i.douyincode,
                "i_card": i.i_card,
                "email": i.email,
                "credit_code": i.credit_code,
                "invitation": i.invitation,
                "positive_pic": i.positive_pic,
                "side_pic": i.side_pic,
                "license": i.license,
                "examine": i.examine,
                "sub_date": i.sub_date
            }
            whell_list.append(whell)
    else:
        whells = None
    apply_data = {
        'stl_list': whell_list,
        'current_page':current_page,
        'total_page':total_page
    }
    return jsonify(data=apply_data)
# 提现申请表_CashApply
@admin_blu.route('/apply')
def adminAddApply():
    try:
        page = request.args.get('pageNum')
        page = int(page)
    except Exception as e:
        page = 1
    current_page = 1
    total_page = 1
    paginate = db.session.query(CashApply).paginate(page,RETCODE.PER_PAGE,False)
    applys = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    apply_list = []
    if applys:
        for i in applys:
            apply = {
                "cashid": i.cashid,
                "cashphone": i.cashphone,
                "cashmoney": i.cashmoney,
                "examine": i.examine,
                "monkey_code": i.monkey_code,
                "cash_date": i.cash_date,
            }
            apply_list.append(apply)
    else:
        applys = None
    apply_data = {
        'apply_list': apply_list,
        'current_page':current_page,
        'total_page':total_page
    }
    return jsonify(data=apply_data)
# 佣金明细表_Brokerage
@admin_blu.route('/querybro')
def adminQueryBro():
    try:
        page = request.args.get('pageNum')
        page = int(page)
    except Exception as e:
        page = 1
    current_page = 1
    total_page = 1
    paginate = db.session.query(Brokerage).paginate(page,RETCODE.PER_PAGE,False)
    applys = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    apply_list = []
    if applys:
        for i in applys:
            apply = {
                "id": i.id,
                "brokerageid": i.brokerageid,
                "phone": i.phone,
                "getphone": i.getphone,
                "brokerage_sum": i.brokerage_sum,
                "operation": i.operation
            }
            apply_list.append(apply)
    else:
        applys = None
    apply_data = {
        'bro_list': apply_list,
        'current_page':current_page,
        'total_page':total_page
    }
    return jsonify(data=apply_data)
# 轮播图表_Wheel
@admin_blu.route('/whellquery')
def adminQueryWhell():
    whells = db.session.query(Wheel).all()
    whell_list = []
    if whells:
        for i in whells:
            whell = {
                "id": i.id,
                "adress_pic": i.adress_pic,
                "url_pic": i.url_pic,
            }
            whell_list.append(whell)
    else:
        whells = None
    apply_data = {
        'whell_list': whell_list,
    }
    return jsonify(data=apply_data)
# 公告表_Content
@admin_blu.route('/con')
def adminQueryContent():
    whells = db.session.query(Content).all()
    whell_list = []
    if whells:
        for i in whells:
            whell = {
                "id": i.id,
                "content": i.content
            }
            whell_list.append(whell)
    else:
        whells = None
    apply_data = {
        'con_list': whell_list,
    }
    return jsonify(data=apply_data)
# 全局设置表_Global
@admin_blu.route('/queryglb')
def adminGlbDel():
    whells = db.session.query(Global).all()
    whell_list = []
    if whells:
        for i in whells:
            whell = {
                "id": i.id,
                "cash_min": i.cash_min,
                "task_num": i.task_num,
                "invite_money": i.invite_money
            }
            whell_list.append(whell)
    else:
        whells = None
    apply_data = {
        'glb_list': whell_list,
    }
    return jsonify(data=apply_data)

# 过滤查
# 管理员表_Superuser
# 用户表_User
@admin_blu.route('/query/<phone>')
def adminQueryUser(phone):
    """
    根据手机号查询用户数据
    :return:
    """
    users = db.session.query(User).filter_by(phone=phone).all()
    user_list = []
    if users:
        for i in users:
            user = {
                "id": i.id,
                "phone": i.phone,
                "openid": i.openid,
                "avatarUrl": i.wxpic_url,
                "nickname": i.wxname,
                "user_identity": i.user_identity,
                "user_all_money": i.user_all_money,
                "user_y_money": i.user_y_money,
                "user_s_money": i.user_s_money,
                "user_icode": i.user_icode,
                "user_all_friend": i.user_all_friend,
                "up_phone": i.up_phone,
                "alipay": i.alipay,
                "reg_time": i.reg_time
            }
            user_list.append(user)
    else:
        users = None
    users_data = {
        'user_list': user_list
    }
    return jsonify(data=users_data,err_code=RETCODE.OK)
# 商品类别表_GoodsClas
# 商品表_Good
@admin_blu.route('/querygoods/<goodsid>')
def adminQueryGoodsFil(goodsid):
    goodsid = int(goodsid)
    goods = db.session.query(Good).filter_by(goodsid=goodsid).all()
    goods_list = []
    if goods:
        for i in goods:
            user = {
                "goodsid": i.goodsid,
                "issuerphone": i.issuerphone,
                "g_title": i.g_title,
                "g_pic": i.g_pic,
                "g_amount": i.g_amount,
                "g_brokerage": i.g_brokerage,
                "status": i.status,
                "classid": i.classid,
                "issuerdate": i.issuerdate,
            }
            goods_list.append(user)
    else:
        goods = None
    goods_data = {
        'goods_list': goods_list
    }
    return jsonify(data=goods_data, err_code=RETCODE.OK)
# 入驻资料表_Settle
# 提现申请表_CashApply
@admin_blu.route('/apply/<cashid>')
def adminQueryApplyFil(cashid):
    cashid = int(cashid)
    goods = db.session.query(CashApply).filter_by(cashid=cashid).all()
    goods_list = []
    if goods:
        for i in goods:
            user = {
                "cashid": i.cashid,
                "cashphone": i.cashphone,
                "cashmoney": i.cashmoney,
                "examine": i.examine,
                "cash_date": i.cash_date,
                "monkey_code": i.monkey_code,
            }
            goods_list.append(user)
    else:
        goods = None
    goods_data = {
        'apply_list': goods_list
    }
    return jsonify(data=goods_data, err_code=RETCODE.OK)
# 佣金明细表_Brokerage
@admin_blu.route('/brokqf/<id>')
def adminQueryBrokFil(id):
    id = int(id)
    goods = db.session.query(Brokerage).filter_by(id=id).all()
    goods_list = []
    if goods:
        for i in goods:
            user = {
                "id": i.id,
                "brokerageid": i.brokerageid,
                "phone": i.phone,
                "getphone": i.getphone,
                "brokerage_sum": i.brokerage_sum,
                "operation": i.operation
            }
            goods_list.append(user)
    else:
        goods = None
    goods_data = {
        'bro_list': goods_list
    }
    return jsonify(data=goods_data, err_code=RETCODE.OK)
# 轮播图表_Wheel
# 公告表_Content
# 全局设置表_Global
