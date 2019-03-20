# -*- coding: utf-8 -*-
# @Time    : 2019/1/15 14:00
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : orderreedm.py

#预约赎回
from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

flask=Flask(__name__)
flask.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://clpa:Clpa123$%^@101.91.212.146:3306/clpa?charset=utf8"
flask.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
flask.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(flask)


#http://101.91.212.146:19006/redis/getRedisByKey?key=brokerinfo_CC0003

def getRedisByKey():
    r = requests.get("http://101.91.212.146:19006/redis/getRedisByKey",params={"key":"brokerinfo_CC0004"})
    print (r.content)

def LoadBrokerInfo():
    '''加载缓存'''
    # r = requests.get("http://127.0.0.1:9006/redis/LoadBrokerInfo")
    r = requests.get("http://101.91.212.146:9006/redis/LoadBrokerInfo")
    print (r.content)


def query_v_pa_holdbalance(prodcode,accountid,bank_card_no):
    '''查询份额'''
    data = db.get_engine().execute(db.text('''
                          select t.prodcode,t.fundname,t.applyamount,t.balance,t.accountid,
                          t.bank_card_no,t.bank_name,t.lastfour_bankcard,t.producttype,t.profit 
                          from v_pa_holdbalance t
                           where t.prodcode = :prodcode  and t.accountid = :accountid
                        and t.bank_card_no = :bank_card_no
                            '''), prodcode=prodcode ,accountid =accountid,bank_card_no=bank_card_no
    ).first()

    result = dict(zip(data.keys(), data))
    # print(result)
    rt={"prodcode":result["prodcode"],"accountid":result["accountid"],"bank_card_no":result["bank_card_no"]}
    return rt

def query_api_channel_balance(prodcode,accountid,bank_card_no):
    '''查询份额'''
    data = db.get_engine().execute(db.text(''' select cljj_user_id, partner_user_id, bank_id, bank_name, bank_card_no, fund_code, 
    fund_nav, nav_date, market_value, holding_cost, taken_profit, flow_profit, balance, 
    melon_method, usable_share, freezer_share, underway_amount, undistributed_income, 
    datetime, custno, channel_id, fast_share, remfastshare, autoinvert, balancetype, prodtp
     from api_channel_balance
     WHERE  cljj_user_id = :cljj_user_id  and bank_card_no = :bank_card_no and fund_code = :fund_code  '''),
                                   fund_code=prodcode ,cljj_user_id =accountid,bank_card_no=bank_card_no
    ).first()

    result = dict(zip(data.keys(), data))
    # print(result)
    usable_share=result["usable_share"]
    return usable_share

def data():
    '''测试数据'''
    prodcode = 'CC0003'
    accountid = 'ff95336dd20b8ae17a319a8ab5bea280'
    bank_card_no = '469968'
    data = query_v_pa_holdbalance(prodcode, accountid, bank_card_no)
    usable_share =query_api_channel_balance(prodcode, accountid, bank_card_no)
    data["usable_share"] = usable_share
    return data


def selectTradeDetail3():
    '''交易记录'''
    # r = requests.get("https://pa.erichfund.com/order/selectTradeDetail3",
    #                  params={"lb": "1",
    #                          "accountid": "0f0a9abaa85a5a1d4a706c4866c1757c",
    #                          "prodcode": "B1A01U", },verify=False)
    url1= 'http://127.0.0.1:9006/order/selectTradeDetail3'
    url2 = 'http://101.91.212.146:9006/order/selectTradeDetail3'
    r = requests.get(url1,
                     params={"lb": "1",
                             "accountid": "ff95336dd20b8ae157abbe5844255bd4",
                             "prodcode": "BC28D1", }, verify=False)

    print (r.content)



def remainBookingredeemShare():
    '''查询预约赎回剩余份额'''
    #http://101.91.212.146:19006/
    r = requests.get("http://101.91.212.146:19006/order/remainBookingredeemShare",
                     params={"cljjUserId":"ff95336dd20b8ae1adaf2f515613900f",
                             "prodcode": "CC0003",
                             "bankCardNo": "476880",})
    print (r.content)


def insertBookingredeemState():
    '''添加预约赎回'''
    r=requests.post(url="http://127.0.0.1:9006/order/insertBookingredeemState",data= json.dumps(
        {"bookingid":None,
        "cljjUserId":"ff95336dd20b8ae1adaf2f515613900f",
         "prodcode":"CC0003","bankCardNo":"476880",
         "redeemBalance":1,"bookingdate":None,
         "startdate":None,"enddate":None,
         "bookingstate":None,"datadate":None,
         "revoketime":None,"appno":None,"redeem_state":None}) ,headers={'content-type': 'application/json'} )
    print (r.content)


def queryApiBookingredeems():
    '''查询预约赎回列表'''
    r = requests.get("http://127.0.0.1:9006/order/queryApiBookingredeems",
                     params={"cljjUserId": "ff95336dd20b8ae17a319a8ab5bea280",
                             "prodcode": "CC0003",
                             "bankCardNo": "469968", })
    print (r.content)

def updateApiBookingredeemShare():
    '''修改预约赎回份额'''
    r = requests.get("http://127.0.0.1:9006/order/updateApiBookingredeemShare",
                     params={"bookingid": "7",
                             "redeemBalance": "1036996.00",
                            })
    print (r.content)

def updateApiBookingredeemState():
    '''撤销状态'''
    r = requests.get("http://127.0.0.1:9006/order/updateApiBookingredeemState",
                     params={"bookingid": "7",

                             })
    print (r.content)


def instructToTrade():
    '''赎回指令进行赎回'''
    r = requests.post("http://127.0.0.1:9006/order/instructToTrade",data= json.dumps({
        "cljjUserId":"ff95336dd20b8ae17a319a8ab5bea280",
        "prodcode": "CC0003",
        "bankCardNo": "469968",
        "redeemBalance": "1037000",

    }) ,headers={'content-type': 'application/json'} )
    print (r.content)

def allBookingRedeemInstructToTrade():
    '''定时执行赎回'''
    r = requests.get("http://101.91.212.146:19006/order/allBookingRedeemInstructToTrade")
    print (r.content)


def redeemInfo():
    r=requests.get(url="http://127.0.0.1:9006/order/redeemInfo",
                    params={"accountid":"ff95336dd20b8ae157abbe5844255bd4","bank_card_no":"44255bd4","prodcode":"BC28D1"}
                   )
    print(r.content)

    
def getProductSummaryInfo():
    '''查询产品列表
    secretKey=a0886410ff964188b6ac12578de0fa22
    appKey=pinganyiqianbao
    '''
    r = requests.get(url="http://127.0.0.1:9006/h5/getProductSummaryInfo",
                     params={"timestamp": datetime.datetime.now(), #当前操作时间与服务器时间相差10分钟
                             "sign": "2C5D435D97DC07B743E85AF50E895783", #secretKey “app_key”  appkey “timestamp” timestamp  secretKey
                             "app_key": "pinganyiqianbao",
                             "prodCodes": "CCC568"} ,
    verify = False)
    print(r.content)


def ymProductDetail():
    r = requests.get(url="https://test2-m.stg.yqb.com/lc/ymProductDetail",
                     params={"productId": 'SF2887',
                             "proClassifyCode": "2C5D435D97DC07B743E85AF50E895783",
                             "shelfId": "2915",
                             "prodCodes": "CCC568",
                             "proStyleCode":"02_5s_1",
                             "prodSupplier":"02"},
                     verify=False)
    print(r.content)


def assetLists():
    r = requests.get(url="http://127.0.0.1:9006/h5/assetLists",
                     params={"timestamp": datetime.datetime.now(),  # 当前操作时间与服务器时间相差10分钟
                             "sign": "2C5D435D97DC07B743E85AF50E895783",
                             # secretKey “app_key”  appkey “timestamp” timestamp  secretKey
                             "app_key": "pinganuat",
                             "prodType": "5",
                             "brokerUserId":"881510952413101101",
                             "assetStatus":"2",
                             "pageSize":"10",
                             "pageNo":"1"},
                     verify=False)
    print(r.content)


def getProductInfo():
    url1="http://127.0.0.1:9006/h5/getProductInfo"
    url2 = "http://101.91.212.146:9006/h5/getProductInfo"
    r = requests.get(url=url2,
                     params={"timestamp": datetime.datetime.now(),  # 当前操作时间与服务器时间相差10分钟
                             "sign": "2C5D435D97DC07B743E85AF50E895783",
                             # secretKey “app_key”  appkey “timestamp” timestamp  secretKey
                             "app_key": "pinganuat",
                             "prodCode": "BC28D1",
                             },
                     verify=False)
    print(r.content)


#brokerUserId：881918852511101101，selectTradeDetail3prodType：5，assetStatus1
def assetLists():
    #30650b80c07e4c0393ffd8511121b822app_keypinganyiqianbaotimestamp155065375222930650b80c07e4c0393ffd8511121b822
    #pa.erichfund.com
    # pinganyiqianbao  pinganuat
    #http://127.0.0.1:9006/h5/assetLists
    r = requests.get(url="http://ty.erichfund.com:19006/h5/assetLists",
                     params={"timestamp": datetime.datetime.now(),
                             "sign": "30650b80c07e4c0393ffd8511121b822",
                             "app_key": "pinganuat",
                             "prodType": "5",
                             "brokerUserId": "881918852511101101",
                             "assetStatus": "1",
                             "pageSize": "10",
                             "pageNo": "1"},
                     verify=False)
    print(r.content)



def createSign():
    '''提供给平安接口 授权码转accessToken'''
    r = requests.get("http://101.91.212.146:19006/order/createSign",
                     params={"authCode":"75ed5899d7a7973f46c05b8c27d449ad470f40378c8ecee3109ca35c8b80535a"}, verify=False)
    print (r.content)


import time


if "__main__" == __name__:



    # data=testdata()
    # print(data)
    '''
    {'usable_share': Decimal('1037000.0000'), 
    'bank_card_no': u'469968', 'prodcode': u'CC0003', 'accountid': u'ff95336dd20b8ae17a319a8ab5bea280'}
    '''
    # getRedisByKey()
    #添加份额
    # insertBookingredeemState()
    #修改份额
    # updateApiBookingredeemShare()
    #撤销赎回
    # updateApiBookingredeemState()
    #查询预约赎回列表
    # queryApiBookingredeems()

    # selectTradeDetail3()

    #可用份额
    # redeemInfo()


    # allBookingRedeemInstructToTrade()
    # redeemInfo()

    # LoadBrokerInfo()

    # getRedisByKey()

    # getProductSummaryInfo()

    # ymProductDetail()

    # assetLists()

    # remainBookingredeemShare()
    # date1 = time.time()
    # assetLists()
    # print(time.time() - date1)

    # assetLists()

    # getProductInfo()

    redeemInfo()