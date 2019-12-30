import os
import requests,json
import random
import time
import uuid
from flask import request, Blueprint, jsonify
from tiktok import db
from tiktok.modules.index.models import *
from tiktok.modules.index.common import sms_

my_blue = Blueprint('my_blue', __name__)

# 登录
@my_blue.route('/user/login', methods=("POST",))
def login():
    try:
        data = request.get_json()
        openid = data.get('openid')
        user = db.session.query(User).filter(User.openid == openid).first()
        phone = user.phone
        sett = db.session.query(Settle).filter(Settle.phone == phone).first()
        if sett:
            examine = sett.examine
        else:
            examine = ""
        datas = {
            "id": user.id,
            "phone": user.phone,
            "wxpic_url": user.wxpic_url,
            "wxname": user.wxname,
            "wxnumber": user.wxnumber,
            "examine": examine,
            "user_all_money": user.user_all_money,
            "user_identity": user.user_identity,
            "user_y_money": int(user.user_all_money) - int(user.user_s_money),
            "user_s_money": user.user_s_money,
            "user_icode": user.user_icode,
            "all_friend": user.user_all_friend,
            "up_phone": user.up_phone,
            "alipay": user.alipay,
            "reg_time": user.reg_time,
        }
    except:
        return jsonify({
            'error_code': 1,
            'msg': '该用户不存在'
        })
    return jsonify({
        'error_code': 0,
        'msg': 'ok',
        'data': datas
    })

# 注册
@my_blue.route('/user/register', methods=("POST",))
def register():
    try:
        data = request.get_json()
        openid = data.get('openid')
        phone = data.get('phone')
        wxname = data.get("wxname")
        user_icode = random.randint(10000, 99999)
        wxpic_url = data.get('wxpic_url')
        reg_time1 = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        reg_time = reg_time1.split(" ")[0]
        user = db.session.query(User).filter(User.phone == phone).first()
        if user:
            return jsonify({
                'error_code': 1,
                'msg': '该用户已经存在'
            })
        else:
            user = User(openid=openid, phone=phone, wxname=str(wxname), user_icode=user_icode,
                        wxpic_url=wxpic_url, reg_time=reg_time, user_all_money="0", user_y_money="0",
                        user_s_money='0', user_all_friend='0')
            db.session.add(user)
            db.session.commit()  # 提交事务
            user1 = db.session.query_property(User).filter(User.phone == phone).first()
            datas = {
                "id": user1.id,
                "phone": user1.phone,
                "wxpic_url": user1.wxpic_url,
                "wxname": user1.wxname,
                "wxnumber": user1.wxnumber,
                "user_all_money": user1.user_all_money,
                "user_y_money": user1.user_y_money,
                "user_s_money": user1.user_s_money,
                "user_icode": user1.user_icode,
                "all_friend": user1.user_all_friend,
                "up_phone": user1.up_phone,
                "alipay": user1.alipay,
                "reg_time": user1.reg_time,
            }
    except Exception as e:
        print(e)
        return jsonify({
            'error_code': 1,
            'msg': '该用户已经存在'
        })
    return jsonify({
        'code': 0,
        'msg': 'ok',
        'data': datas,
    })

# 入驻
@my_blue.route('/daren/settle', methods=("POST",))
def settle():
    try:
        data = request.get_json()
        openid = data.get('openid')
        user_identity = data.get('user_identity')
        name = data.get('name')
        phone = data.get('phone')
        douyincode = data.get('douyincode')
        i_card = data.get('i_card')
        email = data.get('email')
        credit_code = data.get('credit_code', '')
        invitation1 = data.get('invitation', '')
        positive_pic = data.get('positive_pic')
        side_pic = data.get('side_pic', '')
        examine = "审核中"
        license = data.get('license', '')
        sub_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        invitation2 = ''
        if invitation1:
            user1 = db.session.query(User).filter(User.user_icode == invitation1).first()
            if user1:
                invitation2 = invitation1
                user_all_friend = int(user1.user_all_friend)
                user_all_friend += 1
                user1.user_all_friend = user_all_friend
                db.session.add(user1)
                db.session.commit()
            else:
                return jsonify({
                    'status': 1,
                    'msg': '该邀请码不存在'
                })
        users = db.session.query(User).filter(User.phone == phone).first()
        user = db.session.query(Settle).filter(Settle.phone == phone).first()
        if (user is not None) and (users.user_identity in ["达人", "企业"]):
            user2 = db.session.query(User).filter(User.phone == phone).first()
            user2.user_identity = user_identity
            db.session.add(user2)
            db.session.commit()  # 提交事务
        else:
            user1 = db.session.query(User).filter(User.phone == phone).first()
            user1.user_identity = user_identity
            user = Settle(phone=phone, name=name, douyincode=douyincode,
                          i_card=i_card, email=email, invitation=invitation2, positive_pic=positive_pic,
                          side_pic=side_pic, credit_code=credit_code, examine=examine, license=license,
                          sub_date=sub_date,)
            db.session.add(user, user1)
            db.session.commit()  # 提交事务
    except Exception as e:
        return jsonify({
            'status': 1,
            'msg': '入驻失败'
        })
    return jsonify({
        'status': 0,
        'msg': '入驻成功'
    })

# 获取验证码
@my_blue.route('/daren/settle/code', methods=('GET',))
def send_code():
    try:
        # 获取手机号
        phone = request.args.get('phone')
        code = sms_.send_code(phone)
    except:
        return jsonify({
            'status': 1,
            'msg': '发送失败'
        })

    return jsonify({
        'status': 0,
        'msg': '发送成功',
        'code': code
    })

# 删除商品
@my_blue.route('/enter/del', methods=("POST",))
def enter_del():
    try:
        data = request.get_json()
        openid = data.get('openid')
        goodsid = data.get('goodsid')
        user = db.session.query(User).filter(User.openid == openid).first()
        if user:
            goods1 = db.session.query(Good).filter(Good.goodsid == goodsid).first()
            db.session.delete(goods1)
            db.session.commit()  # 提交事务
    except:
        return jsonify({
            'error_code': 1,
            'msg': '没有商品'
        })
    return jsonify({
        'status': 0,
        'msg': 'ok'
    })

# 发布商品
@my_blue.route('/enter/issuer', methods=("POST",))
def issuer():
    try:
        data = request.get_json()
        openid = data.get('openid')
        g_title = data.get('g_title')
        g_pic = data.get('g_pic')
        g_amount = data.get('g_amount')
        g_brokerage = data.get('g_brokerage')
        ambush = data.get('ambush')
        video_url = data.get('video_url')
        status = "审核中"
        classid = data.get('classid')
        issuerdate1 = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        issuerdate = issuerdate1.split(" ")[0]
        user = db.session.query(User).filter(User.openid == openid).first()
        issuerphone = user.phone
        goods1 = Good(issuerphone=issuerphone, g_title=g_title, g_pic=g_pic, g_amount=g_amount,
                      g_brokerage=g_brokerage, status=status, classid=classid, issuerdate=issuerdate,
                      video_url=video_url, ambush=ambush)
        db.session.add(goods1)
        db.session.commit()  # 提交事务
    except:
        return jsonify({
            'error_code': 1,
            'msg': '发布失败'
        })
    return jsonify({
        'ok_code': 0,
        'msg': 'ok'
    })

# 每日领取任务最大量
@my_blue.route('/task/max', methods=("GET",))
def task_max():
    max_task = db.session.query(Global.task_num).first()
    return jsonify({
        "status": 0,
        "msg": "ok",
        "cash_min": max_task[0]
    })

# 商品详情
@my_blue.route('/enter/details', methods=('GET',))
def derails():
    try:
        goodsid = request.args.get('goodsid')
        goods = db.session.query(Good).filter(Good.goodsid == goodsid).first()
        if goods:
            ambush = goods.ambush
            video_url = goods.video_url
            g_pic = goods.g_pic
            g_title = goods.g_title
            g_amount = goods.g_amount
            g_brokerage = goods.g_brokerage
            if g_brokerage.find('.') == 0:
                g_proportion = format((int(g_brokerage)/int(g_amount)) * 100, '.2f')
            else:
                g_proportion = format((float(g_brokerage)*100/int(g_amount)), '.2f')
            datas = {
                'ambush': ambush,
                'video_url': video_url,
                'g_title': g_title,
                'g_pic': g_pic,
                'g_amount': g_amount,
                'g_brokerage': g_brokerage,
                'g_proportion': g_proportion
            }
        else:
            return jsonify({
                'error_code': 1,
                'msg': '没有该商品'
            })

    except Exception as e:
        print(e)
        return jsonify({
            'error_code': 1,
            'msg': '查询失败'
        })
    return jsonify({
        'ok_code': 0,
        'msg': 'ok',
        'data': datas
    })

# 商品类
@my_blue.route('/enter/goods/class', methods=('GET',))
def classes():
    try:
        num = db.session.query(GoodsClas).filter(GoodsClas.classid).all()
        list1 = []
        for i in num:
            dict1 = {
                "classid": i.classid,
                "goodstype": i.goodstype,
            }
            list1.append(dict1)
    except:
        return jsonify({
            'erroe_code': 1,
            'msg':"加载出错"
        })
    return jsonify({
        'code': 0,
        'msg': 'ok',
        'data': list1
    })

# 商品列表
@my_blue.route('/enter/goods', methods=('GET',))
def goods():
    try:
        classid = request.args.get('classid')
        classid = int(classid)
        goods = db.session.query(Good).filter(Good.classid == classid,Good.status == '成功').all()
        if goods:
            list1 = []
            for good in goods:
                goodsid = good.goodsid
                g_pic = good.g_pic
                g_title = good.g_title
                g_amount = good.g_amount
                g_brokerage = good.g_brokerage
                if g_brokerage.find('.') == 0:
                    g_proportion = format((int(g_brokerage)/int(g_amount)) * 100, '.2f')
                else:
                    g_proportion = format((float(g_brokerage)*100/int(g_amount)), '.2f')
                datas={
                    "goodsid": goodsid,
                    "g_pic": g_pic,
                    "g_title": g_title,
                    "g_amount": g_amount,
                    "g_brokerage": g_brokerage,
                    "g_proportion": g_proportion
                }
                list1.append(datas)
        else:
            return jsonify({
                'error_code': 1,
                'msg': '没有该商品'
        })
    except Exception as e:
        print(e)
        return jsonify({
            'error_code': 1,
            'msg': '查询失败'
        })
    return jsonify({
        'ok_code': 0,
        'msg': 'ok',
        'data': list1
    })

# 达人用户领取商品任务
@my_blue.route('/daren/goods', methods=('POST',))
def daren():
    try:
        data = request.get_json()
        openid = data.get('openid')
        goodsid = data.get('goodsid')
        user = db.session.query(User).filter(User.openid == openid).first()
        getphone = user.phone
        renwu = db.session.query(GoodsReceive).filter(GoodsReceive.goodsid == goodsid, GoodsReceive.getphone == getphone).first()
        if not renwu:
            sub_date1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sub_date = sub_date1.split(" ")[0]
            R_num = len(db.session.query(GoodsReceive).filter(GoodsReceive.getphone == getphone, GoodsReceive.getid == sub_date).all())
            max_task = db.session.query(Global.task_num).first()
            if R_num < int(max_task[0]):
                renwu = GoodsReceive(getphone=getphone, goodsid=goodsid, getid=sub_date)
                goods1 = db.session.query(Good).filter(Good.goodsid == goodsid).first()
                goods1.status = "已领取"
                db.session.add(renwu, goods1)
                db.session.commit()  # 提交事务
                goods = db.session.query(Good).filter(Good.goodsid == goodsid).first()
                g_title = goods.g_title
                g_pic = goods.g_pic
                issuerdate = goods.issuerdate
                datas={
                    'g_title': g_title,
                    'g_pic': g_pic,
                    'issuerdate': issuerdate
                }
            else:
                return jsonify({
                    'status': 1,
                    'msg': "今日领取数量已达上限"
                })
        else:
            return jsonify({
                'status': 1,
                'msg': '已接收该任务'
            })
    except:
        return jsonify({
            'status': 1,
            'msg': '接收任务失败'
        })

    return jsonify({
        'status': 0,
        'msg': '接收任务成功',
        'data': datas
    })

# 达人用户取消领取商品任务
@my_blue.route('/daren/goods/del', methods=('POST',))
def daren_del():
    try:
        data = request.get_json()
        openid = data.get('openid')
        goodsid = data.get('goodsid')
        user = db.session.query(User).filter(User.openid == openid).first()
        goods = db.session.query(GoodsReceive).filter(GoodsReceive.getphone == user.phone, GoodsReceive.goodsid == goodsid).first()
        db.session.delete(goods)
        db.session.commit()
        goods1 = db.session.query(Good).filter(Good.goodsid == goodsid).first()
        goods1.status = "成功"
        db.session.add(goods1)
        db.session.commit()   
    except:
        return jsonify({
            'status': 1,
            'msg': '删除任务失败'
        })

    return jsonify({
        'status': 0,
        'msg': '删除任务成功'
    })

# 申请提现最低额度
@my_blue.route('/cash/min', methods=('GET',))
def cash_min():
    max_cash = db.session.query(Global.cash_min).first()
    return jsonify({
        "status": 0,
        "msg": "ok",
        "cash_min": max_cash[0]
    })

# 申请提现
@my_blue.route('/cash', methods=('POST',))
def user_cash():
    try:
        data = request.get_json()
        openid = data.get('openid')
        casher = db.session.query(User).filter(User.openid == openid).first()
        cashphone = casher.phone
        cashmoney = str(data.get('cashmoney'))
        monkey_code = str(data.get('monkey_code'))
        max_cash1 = db.session.query(Global.cash_min).first()
        max_cash = max_cash1.cash_min
        if cashmoney >= max_cash:
            date1 = str(time.time())
            cashid = date1.replace('.','')
            examine = "审核中"
            i = int(casher.user_s_money) + int(cashmoney)
            casher.user_s_money = i
            cash_date = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            cash = CashApply(cashid=cashid,examine=examine, cashphone=cashphone, cashmoney=cashmoney, monkey_code=monkey_code, cash_date=cash_date)
            db.session.add(cash)
            db.session.commit()
        else:
            return jsonify({
                "status": 0,
                "msg": "金额太少"
            })
    except:
        return jsonify({
            'status': 1,
            'msg': '提现申请失败'
        })

    return jsonify({
        'status': 0,
        'msg': '提现申请成功'
    })

# 查询佣金明细
@my_blue.route('/ission', methods=('GET',))
def ission_get():
    try:
        openid = request.args.get('openid')
        casher = db.session.query(User).filter(User.openid == openid).first()
        cashphone = casher.phone
        cashs = db.session.query(Brokerage).filter(Brokerage.phone == cashphone).all()
        list1 = []
        ission_sum = 0
        for cash in cashs:
            getphone = cash.getphone
            user = db.session.query(User).filter(User.phone == getphone).first()
            reg_time = user.reg_time
            wxpic_url = user.wxpic_url
            ission_sum += int(cash.brokerage_sum)
            datas={
                "getphone": getphone,
                "brokerage_sum": cash.brokerage_sum,
                "reg_time": reg_time,
                "wxpic_url": wxpic_url
            }
            list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': '查询失败'
        })

    return jsonify({
        'status': 0,
        'ission_sum':ission_sum,
        'msg': '查询成功',
        'data': list1
    })

# 提现明细
@my_blue.route('/cash/details', methods=('GET',))
def cash_details():
    try:
        openid = request.args.get('openid')
        casher = db.session.query(User).filter(User.openid == openid).first()
        cashphone = casher.phone
        cashs = db.session.query(CashApply).filter(CashApply.cashphone == cashphone).all()
        cash_sum = 0
        for i in cashs:
            if i.examine == "成功":
                cash_sum += int(i.cashmoney)
        list1 = []
        for cash in cashs:
            cashid = cash.cashid
            cashmoney = cash.cashmoney
            examine = cash.examine
            cash_date = cash.cash_date

            datas={
                "cashid": cashid,
                "cashmoney": cashmoney,
                "examine": examine,
                "cash_date": cash_date
            }
            list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': '查询失败'
        })

    return jsonify({
        'status': 0,
        'msg': '查询成功',
        "cash_sum": cash_sum,
        'data': list1
    })

# 邀请人明细
@my_blue.route('/invite/details', methods=('GET',))
def invite_details():
    try:
        openid = request.args.get('openid')
        user = db.session.query(User).filter(User.openid == openid).first()
        user_icode = user.user_icode
        user1 = db.session.query(Settle).filter(Settle.invitation == user_icode,
                                                Settle.examine == '成功').all()
        invite_sum = len(user1)
        print(user1)
        list1 = []
        for i in user1:
            phone = i.phone
            user2 = db.session.query(User).filter(User.phone == phone).first()
            user_identity = user2.user_identity
            datas={
                "phone": phone,
                "user_identity": user_identity,
                "wxpic_url": user2.wxpic_url,
                "examine": i.examine
            }
            list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': '查询失败'
        })

    return jsonify({
        'status': 0,
        'msg': '查询成功',
        'data': {
            "invite_sum": invite_sum,
            "user_icode": user_icode,
            "datas": list1
        }
    })

# 上传图片
@my_blue.route('/upload', methods=("POST",))
def upload():
    try:
        # print(type(request.files)) # ImmutableMultiDict包含的是所有上传文件的一些基本信息
        file = request.files['file']  # http请求是可以通过多文件上传的
        list1 = []
        if file.filename.find('.') > 0:
            # 截取上传的图片的后缀名rsplit找右侧的第一个.，设置成为新图片的后缀名
            file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
            if file_ext in ['png', 'jpg', 'jpeg', 'pdf', 'gif']:
                file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext
                UPLOAD_FOLDER = 'tiktok/img'
                file_dir = os.path.join(os.getcwd(), UPLOAD_FOLDER)
                file_path = os.path.join(file_dir, file_name)
                file.save(file_path)
                # print(file_path)
                img_path = str('/img/%s'%(file_name))

                # print(img_path)
                datas={
                    "url": img_path
                }
                list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': "上传失败"
        })

    return jsonify({
        "status": 0,
        "msg": "上传成功",
        "data": list1
    })

# 首页轮播
@my_blue.route('/wheel1', methods=('GET',))
def wheel1():
    try:
        wheels = db.session.query(Wheel).filter(Wheel.adress_pic == '1').all()
        list1 = []
        for i in wheels:
            datas={
                "url": i.url_pic,
            }
            list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': "加载失败"
        })

    return jsonify({
        "status": 0,
        "msg": "加载成功",
        "data": list1
    })

# 轮播2
@my_blue.route('/wheel2', methods=('GET',))
def wheel2():
    try:
        wheels = db.session.query(Wheel).filter(Wheel.adress_pic == '2').all()
        list1 = []
        for i in wheels:
            datas={
                "url": i.url_pic,
            }
            list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': "加载失败"
        })

    return jsonify({
        "status": 0,
        "msg": "加载成功",
        "data": list1
    })

# 公告
@my_blue.route('/content', methods=('GET',))
def conten():
    try:
        cons = db.session.query(Content.content).first()
        if cons:
            con = cons.content
        else:
            con = ''
    except:
        return jsonify({
            'status': 1,
            'msg': "加载失败"
        })

    return jsonify({
        "status": 0,
        "msg": "加载成功",
        "data": con
    })

# 全部领取任务详情
@my_blue.route('/daren/details/all', methods=('GET',))
def daren_details():
    try:
        openid = request.args.get('openid')
        user = db.session.query(User).filter(User.openid == openid).first()
        phone = user.phone
        gets = db.session.query(GoodsReceive).filter(GoodsReceive.getphone == phone).all()
        list1 = []
        for i in gets:
            goodsid = i.goodsid
            goods = db.session.query(Good).filter(Good.goodsid == goodsid).first()
            if goods:
                g_pic = goods.g_pic
                g_title = goods.g_title
                getid = i.getid
                datas = {
                    'goodsid': goodsid,
                    'g_pic': g_pic,
                    'g_title': g_title,
                    'getid': getid
                }
                list1.append(datas)

    except:
        return jsonify({
            'status': 1,
            'msg': '查询失败'
        })

    return jsonify({
        'status': 0,
        'msg': 'ok',
        'data': list1
    })

# 今日领取任务详情
@my_blue.route('/daren/details/today', methods=('GET',))
def daren_today():
    try:
        openid = request.args.get('openid')
        user = db.session.query(User).filter(User.openid == openid).first()
        phone = user.phone
        gets = db.session.query(GoodsReceive).filter(GoodsReceive.getphone == phone).all()
        reg_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        date1 = reg_time.split(" ")[0]
        list1 = []
        for j in gets:
            getid = j.getid
            if date1 == getid:
                goodsid = j.goodsid
                goods = db.session.query(Good).filter(Good.goodsid == goodsid).first()
                if goods:
                    g_pic = goods.g_pic
                    g_title = goods.g_title
                    getid = j.getid
                    datas = {
                        'goodsid': goodsid,
                        'g_pic': g_pic,
                        'g_title': g_title,
                        'getid': getid
                    }
                    list1.append(datas)
                else:
                    continue
            else:
                continue
    except:
        return jsonify({
            'status': 1,
            'msg': '查询失败'
        })

    return jsonify({
        'status': 0,
        'msg': 'ok',
        'data': list1
    })

# 某用户全部发布
@my_blue.route('/enter/issuer/all', methods=("GET",))
def issuer_all():
    try:
        openid = request.args.get('openid')
        user = db.session.query(User).filter(User.openid == openid).first()
        phone = user.phone
        iss = db.session.query(Good).filter(Good.issuerphone == phone).all()
        list1 = []
        for i in iss:
            goodsid = i.goodsid
            g_pic = i.g_pic
            g_title = i.g_title
            getid = i.issuerdate
            status = i.status
            get_sum = len(db.session.query(GoodsReceive).filter(GoodsReceive.goodsid == goodsid).all())
            datas = {
                'goodsid': goodsid,
                'g_pic': g_pic,
                'g_title': g_title,
                'getid': getid,
                'status':status,
                'get_sum': get_sum
            }
            list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': '查询失败'
        })

    return jsonify({
        'status': 0,
        'msg': 'ok',
        'data': list1
    })

# 某用户今日发布
@my_blue.route('/enter/issuer/today', methods=('GET',))
def issuer_today():
    try:
        openid = request.args.get('openid')
        user = db.session.query(User).filter(User.openid == openid).first()
        phone = user.phone
        iss = db.session.query(Good).filter(Good.issuerphone == phone).all()
        reg_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        date1 = reg_time.split(" ")[0]
        list1 = []
        for j in iss:
            date2 = j.issuerdate.split(" ")[0]
            if date1 == date2:
                goodsid = j.goodsid
                status = j.status
                goods = db.session.query(Good).filter(Good.goodsid == goodsid).first()
                num = len(db.session.query(GoodsReceive).filter(GoodsReceive.goodsid == goodsid).all())
                g_pic = goods.g_pic
                g_title = goods.g_title
                issuerdate = j.issuerdate
                datas = {
                    'goodsid': goodsid,
                    'g_pic': g_pic,
                    'g_title': g_title,
                    'status':status,
                    'num': num,
                    'issuerdate': issuerdate
                }
                list1.append(datas)
    except:
        return jsonify({
            'status': 1,
            'msg': '查询失败'
        })

    return jsonify({
        'status': 0,
        'msg': 'ok',
        'data': list1
    })

# 删除发布任务
@my_blue.route('/daren/issuer/del', methods=('POST',))
def issuer_del():
    try:
        data = request.get_json()
        openid = data.get('openid')
        goodsid = data.get('goodsid')
        user = db.session.query(User).filter(User.openid == openid).first()
        goods = db.session.query(Good).filter(Good.issuerphone == user.phone, Good.goodsid == goodsid).first()
        db.session.delete(goods)
        db.session.commit()
    except:
        return jsonify({
            'status': 1,
            'msg': '删除任务失败'
        })

    return jsonify({
        'status': 0,
        'msg': 'ok'
    })

# 获取openid
@my_blue.route('/open', methods=('GET',))
def opens():
    try:
        js_code = request.args.get('js_code')
        req_params = {
            "appid": 'wxe9ae1b91f8867aa2',  # 小程序的 ID
            "secret": 'db6e623d1b4b6cae832b07d1e682e97c',  # 小程序的 secret
            "js_code": js_code,
            "grant_type": 'authorization_code'
        }
        req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                                  params=req_params, timeout=3, verify=False)
        result = req_result.json()
        if result['session_key']:
            return jsonify({
                'status': 1,
                'msg': "ok",
                'data': result
            })
    except:
        return jsonify({
            'errcode': 40163,
            'errmsg': 'code been used, hints: [ req_id: BIkFMA.KRa-AkmHUa ]',
        })

# 升级
@my_blue.route('/daren/up', methods=("POST",))
def settles():
    try:
        data = request.get_json()
        print(data)
        openid = data.get('openid')
        user_identity = data.get('user_identity')
        phone = data.get('phone')
        print(user_identity, phone)
        user1 = db.session.query(User).filter(User.phone == phone).first()
        if user1:
            user2 = db.session.query(Settle).filter(Settle.phone == phone).first()
            issuerdate1 = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            issuerdate = issuerdate1.split(" ")[0]
            user2.sub_date = issuerdate
            user2.examine = "审核中"
            user1.user_identity = user_identity
            db.session.add(user1,user2)
            db.session.commit()  # 提交事务
        else:
            return jsonify({
                'status': 1,
                'msg': '入驻失败'
            })
    except Exception as e:
        print(e)
        return jsonify({
            'status': 1,
            'msg': '入驻失败'
        })

    return jsonify({
        'status': 0,
        'msg': '入驻成功'
    })

