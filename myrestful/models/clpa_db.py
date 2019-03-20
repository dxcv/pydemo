# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 14:39
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : clpa_db.py

import pymysql
from flask_sqlalchemy import SQLAlchemy
from myrestful.app import flaskapp
from myrestful.models import pyDbRowFactory
from myrestful.util.Util import DictObj

import requests

flaskapp.config["SQLALCHEMY_DATABASE_URI"]= 'mysql://clpa:Clpa123$%^@101.91.212.146:3306/clpa'
flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
flaskapp.config['SQLALCHEMY_ECHO'] = True

#使用flask_sqlalchemy  orm
db2=SQLAlchemy(flaskapp)




#pymysql 使用
db = pymysql.connect(host="101.91.212.146",
                     user="clpa", password="Clpa123$%^",
                     db="clpa", port=3306, cursorclass=pymysql.cursors.DictCursor)


# class Event2(object):
#     def __init__(self):
#         self.id=None
#         self.event_type=None
#         self.event_data = None
#         self.create_time = None
#
#
# sql =""" select * from event """
# from sqlalchemy import create_engine
# engine = create_engine('mysql://cljj_base_event:cljj_base_event@192.168.1.99:3306/cljj_base_event?charset=utf8', echo=False)
# resultProxy = engine.execute(sql)
# rowFactory = pyDbRowFactory.DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "Event2")
# # print(len(rowFactory.fetchAllRowObjects()))
# for rowObject in rowFactory.fetchAllRowObjects():
#     print(rowObject.event_data)




class PaAccountProd():
    prodcode=None
    fundname=None
    applyamount=None
    balance=None
    accountid=None
    producttype=None
    profit=None
    benchmarkrate=None


class ProductAssetDetail():
    apkind=None
    ordertraceno=None
    accountid=None
    prodcode=None
    fundname=None
    bankcardno= None
    apply_amount=None
    confirm_amount= None
    datetime=None
    lastfour_bankcard=None
    confirm_share=None
    apply_status=None
    producttype=None
    bank_name=None




def queryProductAsset(lb, accountid, prodcode):
    '''资产查询'''

    if lb == "0":  # 在途
        # sql ="""
        #     select t.prodcode,t.fundname,t.applyamount ,t.balance ,t.accountid,t.producttype,
        #     t.profit ,t.benchmarkrate from v_pa_ontheway t
		#     where  t.accountid = '{accountid}' and t.prodcode = '{prodcode}'
        # """.format(accountid=accountid,prodcode=prodcode)

        # cur=db.cursor()
        # cur.execute(sql)
        # results=cur.fetchall()

        # stmt = db2.text("""
        #             select t.prodcode,t.fundname,t.applyamount ,t.balance ,t.accountid,t.producttype,
        #             t.profit ,t.benchmarkrate from v_pa_ontheway t
        # 		    where  t.accountid = :accountid and t.prodcode = :prodcode
        #         """)
        # results = db2.get_engine().execute(stmt, accountid=accountid, prodcode=prodcode).fetchall()

        stmt = db2.text("""
            select t.prodcode,t.fundname,t.applyamount ,t.balance ,t.accountid,t.producttype,
            t.profit ,t.benchmarkrate from v_pa_ontheway t
		    where  t.accountid = :accountid and t.prodcode = :prodcode
        """)
        resultProxy = db2.get_engine().execute(stmt,accountid=accountid,prodcode=prodcode)
        rowFactory = pyDbRowFactory.DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "PaAccountProd")
        results=rowFactory.fetchAllRowObjects()
        return results

    elif lb == "1":  # 持有
        sql="""
        select t.prodcode,t.fundname,t.applyamount,t.balance,t.accountid,t.producttype,t.profit,t.benchmarkrate from v_pa_hold t
        where  t.accountid = "{accountid}" and t.prodcode = "{prodcode}"
        """.format(accountid=accountid,prodcode=prodcode)

        # cur = db.cursor()
        # cur.execute(sql)
        # results = cur.fetchall()
        # return DictObj(results)

        resultProxy = db2.get_engine().execute(sql)
        rowFactory = pyDbRowFactory.DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "PaAccountProd")
        results = rowFactory.fetchAllRowObjects()
        return results

    elif lb == "2":  # 历史
        sql="""
        select t.prodcode,t.fundname,t.applyamount,t.balance,t.accountid,t.producttype,t.profit,t.benchmarkrate from v_pa_history t 
         where  t.accountid = '{accountid}' and t.prodcode = '{prodcode}' 
        """.format(accountid=accountid,prodcode=prodcode)
        # cur=db.cursor()
        # cur.execute(sql)
        # results=cur.fetchall()
        # return results

        resultProxy = db2.get_engine().execute(sql)
        rowFactory = pyDbRowFactory.DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "PaAccountProd")
        results = rowFactory.fetchAllRowObjects()
        return results


def queryProductAssetDetail(lb,accountid):
    '''
    资产明细
    :param lb: 
    :param accountid: 
    :return: ProductAssetDetail
    '''
    if lb == "0":#在途
        # sql="""
        #     select t.apkind,t.ordertraceno,t.accountid,t.prodcode,t.fundname,t.bankcardno,t.apply_amount,t.confirm_amount,t.DATETIME,t.lastfour_bankcard,t.confirm_share
        #     ,t.apply_status,t.producttype,t.bank_name
        #     from v_pa_onthewaydetail t
        #      where  1=1
        #      and t.accountid = '{accountid}'
        #      order by t.DATETIME desc
        # """.format(accountid=accountid)
        # cur = db.cursor()
        # cur.execute(sql)
        # results = cur.fetchall()
        # return results

        stmt = db2.text("""
            select t.apkind,t.ordertraceno,t.accountid,t.prodcode,t.fundname,t.bankcardno,t.apply_amount,t.confirm_amount,t.DATETIME,t.lastfour_bankcard,t.confirm_share
            ,t.apply_status,t.producttype,t.bank_name
            from v_pa_onthewaydetail t 
             where  1=1   
             and t.accountid = :accountid
             order by t.DATETIME desc
        """)
        resultProxy = db2.get_engine().execute(stmt,accountid=accountid)
        rowFactory = pyDbRowFactory.DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "ProductAssetDetail")
        results = rowFactory.fetchAllRowObjects()
        return results

    elif lb == "1":#持有
        # sql = """
        # select t.apkind,t.ordertraceno,t.accountid,t.prodcode,t.fundname,t.bankcardno,t.apply_amount,t.confirm_amount,t.DATETIME,t.lastfour_bankcard,t.confirm_share
		# ,t.apply_status,t.producttype,t.bank_name
 		# from v_pa_holddetail t
 		# where  1=1
		# and t.accountid = '{accountid}'
		# order by t.DATETIME desc
        # """.format(accountid=accountid)
        # cur = db.cursor()
        # cur.execute(sql)
        # results = cur.fetchall()
        # return results

        stmt = db2.text("""
                    select t.apkind,t.ordertraceno,t.accountid,t.prodcode,t.fundname,t.bankcardno,t.apply_amount,t.confirm_amount,t.DATETIME,t.lastfour_bankcard,t.confirm_share
                    ,t.apply_status,t.producttype,t.bank_name
                    from v_pa_holddetail t 
                    where  1=1   
                    and t.accountid = :accountid
                    order by t.DATETIME desc
                """)
        resultProxy = db2.get_engine().execute(stmt, accountid=accountid)
        rowFactory = pyDbRowFactory.DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "ProductAssetDetail")
        results = rowFactory.fetchAllRowObjects()
        return results


    elif lb == "2":#历史
        # sql= """
        # select t.apkind,t.ordertraceno,t.accountid,t.prodcode,t.fundname,t.bankcardno,t.apply_amount,t.confirm_amount,t.datetime,t.lastfour_bankcard,t.confirm_share
		# ,t.apply_status,t.producttype,t.bank_name
 		# from v_pa_historydetail  t
 		# where  1=1
		# and t.accountid ='{accountid}'
		# order by t.DATETIME desc
        # """.format(accountid=accountid)
        # cur = db.cursor()
        # cur.execute(sql)
        # results = cur.fetchall()
        # return results

        stmt = db2.text("""
                         select t.apkind,t.ordertraceno,t.accountid,t.prodcode,t.fundname,t.bankcardno,t.apply_amount,t.confirm_amount,t.datetime,t.lastfour_bankcard,t.confirm_share
                        ,t.apply_status,t.producttype,t.bank_name
                        from v_pa_historydetail  t 
                        where  1=1   
                        and t.accountid = :accountid
                        order by t.DATETIME desc
                        """)
        resultProxy = db2.get_engine().execute(stmt, accountid=accountid)
        rowFactory = pyDbRowFactory.DbRowFactory.fromSqlAlchemyResultProxy(resultProxy, "ProductAssetDetail")
        results = rowFactory.fetchAllRowObjects()
        return results


def shareByBank(prodcode,accountid):
    '''查询银行卡下的份额'''
    sql="""
    select t.prodcode,t.fundname,t.applyamount,t.balance,t.accountid,t.bank_card_no,t.bank_name,t.lastfour_bankcard,t.producttype,t.profit
      from v_pa_holdbalance t where t.prodcode = '{prodcode}' and t.accountid= '{accountid}'
    """.format(prodcode=prodcode,accountid=accountid)
    cur = db.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    for obj in results:
        _obj=DictObj(obj)
        balance=DictObj(channelBalance(accountid,_obj.bank_card_no,_obj.prodcode))
        obj['usable_share']=balance.usable_share
    return results


def channelBalance(cljj_user_id,bank_card_no,fund_code):
    '''查询用户银行卡对应份额'''
    sql="""
    select cljj_user_id, partner_user_id, bank_id, bank_name, bank_card_no, fund_code,
    fund_nav, nav_date, market_value, holding_cost, taken_profit, flow_profit, balance,
    melon_method, usable_share, freezer_share, underway_amount, undistributed_income,
    datetime, custno, channel_id, fast_share, remfastshare, autoinvert, balancetype, prodtp
     from api_channel_balance
     WHERE  cljj_user_id = '{cljj_user_id}'  and bank_card_no = '{bank_card_no}' and fund_code = '{fund_code}'
    """.format(cljj_user_id=cljj_user_id,bank_card_no=bank_card_no,fund_code=fund_code)
    cur = db.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    return result

#############################################################################################################


import json
import decimal,datetime

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o,"%Y-%m-%d %H:%M:%S")
        super(MyJSONEncoder, self).default(o)


#视图，使用Table  ,表使用Model
#没有主键只能使用Table
v_pa_ontheway = db2.Table('v_pa_ontheway',
    db2.Column('prodcode'),
    db2.Column('fundname'),
    db2.Column('applyamount'),
    db2.Column('balance'),
    db2.Column('accountid'),
    db2.Column('producttype'),
    db2.Column('profit'),
    db2.Column('benchmarkrate'),)

v_pa_hold = db2.Table('v_pa_hold',
    db2.Column('prodcode'),
    db2.Column('fundname'),
    db2.Column('applyamount'),
    db2.Column('balance'),
    db2.Column('accountid'),
    db2.Column('producttype'),
    db2.Column('profit'),
    db2.Column('benchmarkrate'),)

v_pa_history=db2.Table('v_pa_history',
    db2.Column('prodcode'),
    db2.Column('fundname'),
    db2.Column('applyamount'),
    db2.Column('balance'),
    db2.Column('accountid'),
    db2.Column('producttype'),
    db2.Column('profit'),
    db2.Column('benchmarkrate'),)



v_pa_onthewaydetail=db2.Table('v_pa_onthewaydetail',
db2.Column("apkind"),
db2.Column("ordertraceno"),
db2.Column("accountid"),
db2.Column("prodcode"),
db2.Column("fundname"),
db2.Column("bankcardno"),
db2.Column("apply_amount"),
db2.Column("confirm_amount"),
db2.Column("datetime"),
db2.Column("lastfour_bankcard"),
db2.Column("confirm_share"),
db2.Column("apply_status"),
db2.Column("producttype"),
db2.Column("bank_name"),
                              )
v_pa_holddetail=db2.Table('v_pa_holddetail',
db2.Column("apkind"),
db2.Column("ordertraceno"),
db2.Column("accountid"),
db2.Column("prodcode"),
db2.Column("fundname"),
db2.Column("bankcardno"),
db2.Column("apply_amount"),
db2.Column("confirm_amount"),
db2.Column("datetime"),
db2.Column("lastfour_bankcard"),
db2.Column("confirm_share"),
db2.Column("apply_status"),
db2.Column("producttype"),
db2.Column("bank_name"),
                              )

v_pa_historydetail=db2.Table('v_pa_historydetail',
db2.Column("apkind"),
db2.Column("ordertraceno"),
db2.Column("accountid"),
db2.Column("prodcode"),
db2.Column("fundname"),
db2.Column("bankcardno"),
db2.Column("apply_amount"),
db2.Column("confirm_amount"),
db2.Column("datetime"),
db2.Column("lastfour_bankcard"),
db2.Column("confirm_share"),
db2.Column("apply_status"),
db2.Column("producttype"),
db2.Column("bank_name"),
                              )



v_pa_holdbalance = db2.Table('v_pa_holdbalance',
db2.Column("prodcode"),
db2.Column("fundname"),
db2.Column("applyamount"),
db2.Column("balance"),
db2.Column("accountid"),
db2.Column("bank_card_no"),
db2.Column("bank_name"),
db2.Column("lastfour_bankcard"),
db2.Column("producttype"),
db2.Column("profit"),
)


api_channel_balance = db2.Table('api_channel_balance',
db2.Column('cljj_user_id'),
db2.Column('partner_user_id'),
db2.Column('bank_id'),
db2.Column('bank_name'),
db2.Column('bank_card_no'),
db2.Column('fund_code'),
db2.Column('fund_nav'),
db2.Column('nav_date'),
db2.Column('market_value'),
db2.Column('holding_cost'),
db2.Column('taken_profit'),
db2.Column('flow_profit'),
db2.Column('balance'),
db2.Column('melon_method'),
db2.Column('usable_share'),
db2.Column('freezer_share'),
db2.Column('underway_amount'),
db2.Column('undistributed_income'),
db2.Column('datetime'),
db2.Column('custno'),
db2.Column('channel_id'),
db2.Column('fast_share'),
db2.Column('remfastshare'),
db2.Column('autoinvert'),
db2.Column('balancetype'),
db2.Column('prodtp'),
)


def queryProductAsset2(lb, accountid, prodcode):
    '''
    资产查询  ,数据在视图中
    :param lb: 类别
    :param accountid: 账户
    :param prodcode:  产品
    :return: list[dict]
    '''
    assert isinstance(lb,str)
    assert isinstance(accountid,str)
    assert isinstance(prodcode,str)
    result = None
    if lb == "0":# 在途
        result=db2.session.query(v_pa_ontheway)\
            .filter(db2.text(" accountid = :accountid and  prodcode = :prodcode "))\
            .params(accountid=accountid,prodcode=prodcode).all()
    elif lb == "1":# 持有
        result = db2.session.query(v_pa_hold).filter(
            db2.text(" accountid = :accountid and  prodcode = :prodcode "))\
            .params(accountid=accountid,prodcode=prodcode).all()
    elif lb == "2":# 历史
        result = db2.session.query(v_pa_history).filter(
            db2.text(" accountid = :accountid and  prodcode = :prodcode "))\
            .params(accountid=accountid,prodcode=prodcode).all()

    # result = json.dumps(result, cls=MyJSONEncoder)
    from sqlalchemy.util._collections import _LW
    if result :assert isinstance(result[0],_LW)
    #list[sqlalchemy.util._collections.result] 转变成 list[dict]
    data = [dict(zip(data.keys(), data)) for data in result]
    return data


def queryProductAssetDetail2(lb,accountid):
    '''
    交易记录
    :param lb:
    :param accountid:
    :return: list[dict]
    '''
    assert isinstance(lb, str)
    assert isinstance(accountid, str)
    result = None
    if lb == "0": #在途
        result = db2.session.query(v_pa_onthewaydetail).filter(
            db2.text(" accountid = :accountid ")).params(accountid=accountid).all()
    elif lb == "1":#持有
        result = db2.session.query(v_pa_holddetail).filter(
            db2.text(" accountid = :accountid ")).params(accountid=accountid).all()
    elif lb == "2":#历史
        result = db2.session.query(v_pa_historydetail).filter(
            db2.text(" accountid = :accountid ")).params(accountid=accountid).all()

    # result = json.dumps(result, cls=MyJSONEncoder)
    data = [dict(zip(data.keys(), data)) for data in result]
    return data


def shareByBank2(prodcode,accountid):
    '''
    查询银行卡下的份额
    :param prodcode:
    :param accountid:
    :return: list[dict]
    '''
    assert isinstance(accountid, str)
    assert isinstance(prodcode, str)
    result = db2.session.query(v_pa_holdbalance).filter(
        db2.text(" prodcode = :prodcode and accountid = :accountid ")).params(prodcode=prodcode,accountid=accountid).all()
    data = [dict(zip(data.keys(), data)) for data in result]
    return data

def channelBalance2(cljj_user_id,bank_card_no,fund_code):
    '''
    查询用户银行卡对应份额
    :param cljj_user_id:
    :param bank_card_no:
    :param fund_code:
    :return: dict
    '''
    assert isinstance(cljj_user_id, str)
    assert isinstance(bank_card_no, str)
    assert isinstance(fund_code, str)
    result = db2.session.query(api_channel_balance).filter(
        db2.text(" cljj_user_id = :cljj_user_id and bank_card_no = :bank_card_no and fund_code = :fund_code ")).params(
        cljj_user_id=cljj_user_id,
        bank_card_no=bank_card_no,
        fund_code=fund_code).first()
    #sqlalchemy.util._collections.result  转变成字典
    result = dict(zip(result.keys(), result))
    return result





class Bookingredeem(db2.Model):
    '''
    预约赎回关联表
    继承Model
    '''
    __tablename__= "api_bookingredeem"
    bookingid = db2.Column(db2.Integer,unique=True,primary_key=True)
    cljj_user_id = db2.Column(db2.Integer)
    prodcode = db2.Column(db2.String(8))
    bookingdate = db2.Column(db2.String(10))
    bookingstate = db2.Column(db2.String(1))
    # ifhandle =  db2.Column(db2.String(1))
    datadate =  db2.Column()


class channelRelationship(db2.Model):
    '''
    关联表
    继承 Model
    '''
    __tablename__="api_channel_relationship"
    partner_user_id = db2.Column(db2.String,primary_key=True)
    cljj_user_id=db2.Column(db2.String)
    channel_id= db2.Column(db2.String)
    risk=db2.Column(db2.String)


def recordBookingredeem(bookingid):
    '''
    预约赎回设置
    :param cljj_user_id:
    :param prodcode:
    :return: Bookingredeem
    '''
    bookingredeem = db2.session.query(Bookingredeem).filter_by(bookingid=bookingid).first()

    if not bookingredeem: #添加
        br=Bookingredeem(cljj_user_id=bookingredeem.cljj_user_id,
                         prodcode=bookingredeem.prodcode,
                         bookingdate=datetime.datetime.strftime("%Y-%m-%d %H:%M:%S")
                      ,bookingstate="1",datadate=datetime.datetime.now())
        db2.session.add(br)
        db2.session.commit()
    else: #更新
        bookingredeem.bookingstate = "1" if bookingredeem.bookingstate == "0" else 0
        bookingredeem.datadate=datetime.datetime.now()
        db2.session.commit()

    return bookingredeem




#
# def timerRun():
#
#     bookingrds=db2.session.query(Bookingredeem).filter(db2.text(" bookingstate = '1' and  ifhandle = '0' " )).all()
#     if bookingrds:
#         for br in bookingrds:
#             relationship = db2.session.query(channelRelationship).filter_by(cljj_user_id=br.cljj_user_id).first()
#             if relationship:
#                 datas=db2.session.query(api_channel_balance).filter(db2.text(" cljj_user_id = :cljj_user_id and  fund_code = :fund_code and  usable_share >0  ")).params(cljj_user_id=br.cljj_user_id,fund_code=br.prodcode).all()
#                 if datas:
#                     reedem_success_results=[] #赎回成功结果
#                     reedem_fail_results=[] #赎回失败结果
#                     for d in datas:
#                         remote_reedem=requests.post("http://192.168.1.198:8088/partner/tradeHandler.go",data={
#                             "sign":"1B18BE5D8BDF97CF62F5D60811E07B95",
#                             "timestamp":"2018-12-25+14%3A51%3A10",
#                             "v":"1.1",
#                             "from_channel":"3000",
#                             "data":"%257B%2522cljj_user_id%2522%253A%2522ff95336dd20b8ae17a319a8ab5bea280%2522%252C%2522partner_user_id%2522%253A%2522881513952414101101%2522%252C%2522fund_code%2522%253A%2522952001%2522%252C%2522bank_card_no%2522%253A%2522469968%2522%252C%2522apply_share%2522%253A%25221%2522%252C%2522balancetype%2522%253A%252200%2522%257D",
#                             "method":"cljj.trade.redeem",
#                             "app_key":"pingantest",
#                         })
#                         retdata=remote_reedem.json()
#                         if retdata["err_code"] == "5992":
#                             reedem_success_results.append({"cljj_user_id":br.cljj_user_id , "prodcode":br.prodcode,"bank_card_no":d.bank_card_no,"usable_share":d.usable_share,"info":"赎回成功"})
#                         else:
#                             reedem_fail_results.append({"cljj_user_id":br.cljj_user_id , "prodcode":br.prodcode,"bank_card_no":d.bank_card_no,"usable_share":d.usable_share,"info":"赎回失败"})
#
#                     print(reedem_success_results)
#
#                     if len(datas) == len(reedem_success_results):
#                         bookingredeem = db2.session.query(Bookingredeem).filter_by(cljj_user_id=br.cljj_user_id,
#                                                                                    prodcode=br.prodcode).first()
#                         bookingredeem.ifhandle = '1'
#                         db2.session.commit()
#
#                     else:
#                         print("用户{cljj_user_id}拥有的产品{prodcode}没有全部赎回" % {"cljj_user_id":br.cljj_user_id,"prodcode":br.prodcode})
#
#                 else:
#                     print("用户{cljj_user_id}拥有的产品{prodcode}没有可用赎回的份额" % {"cljj_user_id":br.cljj_user_id,"prodcode":br.prodcode} )
#
#             else:
#                 print("用户不存在，不进行赎回，请确认该用户是否已经注销了？")
#     else:
#         print("没有预约赎回的用户")
#
#
#
# def timerRun2():
#     reedem_success_results = []  # 赎回成功结果
#     reedem_fail_results = []  # 赎回失败结果
#
#     redeem_all=canredeem()
#     if not redeem_all :
#         print("没有可赎回的数据")
#     elif redeem_all:
#         for rd in redeem_all:
#             banks=rd["banks"]
#             for bank in banks:
#
#                 recode_result={"cljj_user_id": rd["cljj_user_id"], "prodcode": rd["fund_code"], "bank_card_no": bank["bank_card_no"],
#                  "usable_share": bank["usable_share"], "info": None}
#
#                 remote_data=redeem(rd["cljj_user_id"],rd["fund_code"],bank["bank_card_no"],bank["usable_share"])
#
#                 if remote_data["err_code"] == "5992":
#                     recode_result["info"]="赎回成功"
#                     reedem_success_results.append(recode_result)
#                 else:
#                     recode_result["info"] = "赎回失败"
#                     reedem_fail_results.append(recode_result)
#
#     print("赎回成功：",reedem_success_results)
#     print("赎回失败：",reedem_fail_results)


def canredeem():
    '''可以赎回的数据'''
    redeem_allresult = []
    bookingrds = db2.session.query(Bookingredeem).filter(db2.text(" bookingstate = '1' and  ifhandle = '0' ")).all()
    if bookingrds:
        for br in bookingrds:
            accountshares={"cljj_user_id":None,"fund_code":None,"banks":[]}
            relationship = db2.session.query(channelRelationship).filter_by(cljj_user_id=br.cljj_user_id).first()
            if not relationship:
                raise RuntimeError("用户不存在")

            accountshares["cljj_user_id"]=br.cljj_user_id
            accountshares["fund_code"] = br.prodcode

            datas = db2.session.query(api_channel_balance).filter(db2.text(
                " cljj_user_id = :cljj_user_id and  fund_code = :fund_code and  usable_share >0  ")).params(
                cljj_user_id=br.cljj_user_id, fund_code=br.prodcode).all()
            if datas:
                for bank in datas:
                    _bank={"bank_card_no":bank.bank_card_no,"usable_share":bank.usable_share}
                    accountshares["banks"].append(_bank)

            redeem_allresult.append(accountshares)

    return redeem_allresult



def redeem(cljj_user_id,fund_code,bank_card_no,usable_share):
    '''
    调用赎回接口
    :param cljj_user_id:
    :param fund_code:
    :param bank_card_no:
    :param usable_share:
    :return:
    '''
    remote_reedem = requests.post("http://192.168.1.198:8088/partner/tradeHandler.go", data={
        "sign": "1B18BE5D8BDF97CF62F5D60811E07B95",
        "timestamp": "2018-12-25+14%3A51%3A10",
        "v": "1.1",
        "from_channel": "3000",
        "data": "%257B%2522cljj_user_id%2522%253A%2522ff95336dd20b8ae17a319a8ab5bea280%2522%252C%2522partner_user_id%2522%253A%2522881513952414101101%2522%252C%2522fund_code%2522%253A%2522952001%2522%252C%2522bank_card_no%2522%253A%2522469968%2522%252C%2522apply_share%2522%253A%25221%2522%252C%2522balancetype%2522%253A%252200%2522%257D",
        "method": "cljj.trade.redeem",
        "app_key": "pingantest",
    })
    retdata = remote_reedem.json()
    return retdata




if "__main__" == __name__:
    # data=recordBookingredeem("218")
    # print(data)
    # timerRun2()

    # datas2 = queryProductAsset2("0", "ff95336dd20b8ae17a319a8ab5bea280", "952001")
    # print(datas2)

    data = queryProductAssetDetail("0", "ff95336dd20b8ae17a319a8ab5bea280")
    for d in data :
        assert isinstance(d ,ProductAssetDetail)
        print(d.prodcode)
    # print(data)
    pass