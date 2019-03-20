# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 18:58
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : req.py


import requests
requests.packages.urllib3.disable_warnings()
import json



def test_messageRemind():
    '''提供给平安接口 消息推送'''
    data={
        "recastType":"",
        "redeemUnit":0,
        "totalAsset":"10",
        "orderNo":"000001",
        "totalProfit":"10",
        "sysId":"bb0ad789a09941e982277d559f3f92e4",
        "serviceCode":"R0883",
        "investAmt":110,
        "dispatchAmt":10003.24,
        "toAcctType":"10",
        "investTime":"2018-11-29",
        "userId":"881817654819101101",
        "msgRemindType":"1",
        "productName":"君得利一号",
        "bankCardId":"00003",
        "reqId":"aa363e0208c04ad99523ef1937dde359",
        "dispatchTimeLimit":3,
        "productCode":"952001",
        "investUnit":10000,
        "redeemAmt":10003.24,
        "expiredSign":"1",
        "expireDate":"2018-11-09",
        "prodSupplier":"04",
        "yesterdayProfit":"10"
    }

    r=requests.post("https://ty.erichfund.com:19006/order/messageRemind",headers={'content-type': 'application/json'},data=json.dumps(data), verify=False)
    print (r.content)


def test_createSign():
    '''提供给平安接口 授权码转accessToken'''
    r = requests.get("https://ty.erichfund.com:19006/order/createSign",
                     params={"authCode":"090e258ae90b22fd78862f92011fbedf48b3f54700917e2ff19fa4e4a6319184"}, verify=False)
    print (r.content)


def test_selectTradeDetail3():
    '''提供给长量接口 查询详情'''
    r = requests.get("https://ty.erichfund.com:19006/order/selectTradeDetail3",
                     params={"lb": "0","accountid":"ff95336dd20b8ae14f8a76e8f4773553","prodcode":"BC7D01"},
                     verify=False)
    print (r.content)

def test_queryProductTradeDetail():
    '''提供给长量接口 通过单号查询详情'''
    r = requests.get("https://ty.erichfund.com:19006/order/queryProductTradeDetail",
                     queryProductAssetparams={"ordertraceno": "1409180000270847"},
                     verify=False)
    print (r.content)


def test_selectIsFirstBuy():
    '''提供给长量接口 区分首投与追加购买'''
    r = requests.get("https://ty.erichfund.com:19006/order/selectIsFirstBuy",
                     params={"accountid": "ff95336dd20b8ae1f1a0dc930dd8d03d","prodcode":"BC7D01"},
                     verify=False)
    print (r.content)


def test_redeemSuccessInfo():
    '''提供给长量接口 赎回成功结果'''
    r = requests.get("https://ty.erichfund.com:19006/order/redeemSuccessInfo",
                     params={"verifyNo": "efe0465881a27bc3f1029dc8256dd2cb8d413c1e28dac65a"},
                     verify=False)
    print (r.content)


def test_redeemInfo():
    '''提供给长量接口 赎回展示信息'''
    r = requests.get("https://ty.erichfund.com:19006/order/redeemInfo",
                     params={"accountid": "1111","prodcode":"BC7D01","bank_card_no":"DX0001"},
                     verify=False)
    print (r.content)


def test_redeem():
    '''提供给长量接口 赎回下单'''
    r = requests.post("https://ty.erichfund.com:19006/order/redeem",
                      headers={'content-type': 'application/json'},
                      data= json.dumps({"apply_share": 1000,"accountid":"x111","prodcode":"DX0001","bank_card_no":"000001"}) ,
                     verify=False)
    print (r.content)



def test_email_send():
    r = requests.post("http://127.0.0.1:7002/email/send",
                      headers={'content-type': 'application/json'},
                      data=json.dumps(
                          {"address":"gushiqiang@changmaotech.com",
                           "subject":"每日份额变动推送异常邮件",
                           "content":"每日份额变动推送异常,异常原因:For input string: \"sos\"",
                           "bizId":"1544427627986",
                           "eventCode":"TRADE.BIZ"}))
    print (r.content)


if __name__ == "__main__" :
    # test_email_send()
    test_createSign()