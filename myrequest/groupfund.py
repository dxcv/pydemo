
# -*- coding:utf-8 -*-

import requests

url = 'http://127.0.0.1:9006'
url2 = 'http://101.91.212.146:9006'

def chechRisk():
    '''
    检查风险登记
    :return:
    '''
    ret =requests.get(url= 'https://teststable-m.stg.yqb.com/lc/checkYMQualiﬁcation',
                 params={'prdRiskLevel':"1",
                         "productId":"000001",
                         "prodSupplier":"02",
                         "merchantId":"900000169148",
                         "successUrl":"http://www.baidu.com" }, verify=False)

    print(ret.content)

import json
def getProtocol():
    '''
    获取协议号
    :return:
    '''
    ret = requests.post(url='https://test2-mapi.stg.1qianbao.com/ffastpay',
                  data={"platMerchantId":["900000169150"],
                        "identityType":["I"],"transType":["057"],
                        "signMethod":["SHA-256"],"reqType":["M"],
                        "fundSaleCode":["306"],"charset":["UTF-8"],
                        "identityNumber":["110101199003074899"],
                        "realName":["彭麻麻"],"uId":["1234567890xxx"],"merchantId":["900000169150"],
                        "signature":["c53f6cefb96b2de9a6e26947ee2bb0de57028cea9660f320e14fada51ffc5f4c"],
                        "version":["1.0.0"]},verify=False)


    print(ret.content)



def qs_order():
    ret = requests.post(url='https://test2-mapi.stg.1qianbao.com/ffastpay',
                        data=json.dumps({"accessToken":"8f3a15ef3cd886c76c259008af44abae4300dc1568df1e8375a52d522d3aa0ca",
                                         "uid":"881513952414101101","orderno":None,"ordertraceno":None,
                                         "prodcode":"952001","bankcardno":None,"applyamount":5000000,
                                         "paytype":None,"accountid":"ff95336dd20b8ae17a319a8ab5bea280",
                                         "orderstate":None,"paystate":None,"datetime":None}), verify=False)

    print(ret.content)




def getGroupFundInfo():
    '''
    查询组合信息
    :return:
    '''
    ret =requests.get(url= url2 + '/order/groupFundInfo',
                 params={'groupid':"000000000136"}, verify=False)

    print(ret.content)


def getHistoryGroupNav():
    '''
    查询组合净值走势
    :return:
    '''
    ret =requests.get(url=url2 +'/order/getHistoryGroupNav',
                 params={'groupid':"000000000136","datetype":"all"}, verify=False)

    print(ret.content)


def groupPlaceOrder ():
    ret = requests.post(url=url2+'/order/group/groupPlaceOrder',
                       json={"accessToken":"692ff4cd6a5cf4c9004ff070ccda3ac8d41aead974c30b2886519b57b3c71ccb",
                             'uid': "881918852511101101", "applyamount": "10000","fundCode":"000000000136"},
                        verify=False)

    print(ret.content)


if "__main__" == __name__ :
    getGroupFundInfo()