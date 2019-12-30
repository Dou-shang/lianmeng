# coding: utf-8
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Brokerage(Base):
    __tablename__ = 'brokerage'

    id = Column(INTEGER(11), primary_key=True)
    brokerageid = Column(INTEGER(11))
    phone = Column(String(11))
    getphone = Column(String(11))
    brokerage_sum = Column(String(20))
    operation = Column(String(100))


class CashApply(Base):
    __tablename__ = 'cash_apply'

    id = Column(INTEGER(11), primary_key=True)
    cashphone = Column(String(11))
    cashmoney = Column(String(20))
    cashid = Column(String(50))
    examine = Column(String(20))
    cash_date = Column(String(100))
    monkey_code = Column(String(50))


class Content(Base):
    __tablename__ = 'contents'

    id = Column(INTEGER(11), primary_key=True)
    content = Column(String(256))


class Global(Base):
    __tablename__ = 'globals'

    id = Column(INTEGER(11), primary_key=True)
    cash_min = Column(String(20))
    task_num = Column(String(10))
    invite_money = Column(String(10))


class GoodsClas(Base):
    __tablename__ = 'goods_class'

    id = Column(INTEGER(11))
    classid = Column(INTEGER(11), primary_key=True)
    goodstype = Column(String(80))


class GoodsReceive(Base):
    __tablename__ = 'goods_receive'

    id = Column(INTEGER(11), primary_key=True)
    goodsid = Column(INTEGER(11))
    getphone = Column(String(11))
    getid = Column(String(100))


class Settle(Base):
    __tablename__ = 'settle'

    id = Column(INTEGER(11), primary_key=True)
    bringid = Column(INTEGER(11))
    bringclass = Column(String(50))
    phone = Column(String(11))
    name = Column(String(50))
    douyincode = Column(String(10))
    i_card = Column(String(20))
    email = Column(String(20))
    credit_code = Column(String(20))
    invitation = Column(String(10))
    positive_pic = Column(String(100))
    side_pic = Column(String(100))
    license = Column(String(100))
    examine = Column(String(20))
    sub_date = Column(String(100))


class Superuser(Base):
    __tablename__ = 'superuser'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(100))
    token = Column(String(256))
    password = Column(String(100))


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    phone = Column(String(11))
    openid = Column(String(256))
    wxpic_url = Column(String(256))
    wxname = Column(String(80))
    wxnumber = Column(String(20))
    user_identity = Column(String(50))
    user_all_money = Column(String(20))
    user_y_money = Column(String(20))
    user_s_money = Column(String(20))
    user_icode = Column(String(10))
    user_all_friend = Column(String(10))
    up_phone = Column(String(11))
    alipay = Column(String(30))
    reg_time = Column(String(100))


class Wheel(Base):
    __tablename__ = 'wheel'

    id = Column(INTEGER(11), primary_key=True)
    adress_pic = Column(String(256))
    url_pic = Column(String(256))


class Good(Base):
    __tablename__ = 'goods'

    goodsid = Column(INTEGER(11), primary_key=True, nullable=False)
    issuerphone = Column(String(11))
    g_title = Column(String(100))
    g_pic = Column(String(256))
    g_amount = Column(String(20))
    g_brokerage = Column(String(20))
    status = Column(String(10))
    ambush = Column(String(256))
    video_url = Column(String(256))
    classid = Column(ForeignKey('goods_class.classid', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False, index=True)
    issuerdate = Column(String(100))

    goods_clas = relationship('GoodsClas')
