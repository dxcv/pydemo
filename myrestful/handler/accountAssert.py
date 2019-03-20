# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 19:26
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : accountAssert.py


from myrestful.util.Util import DictObj
from myrestful.models.clpa_db import queryProductAsset, queryProductAssetDetail,shareByBank,\
    queryProductAsset2, queryProductAssetDetail2,shareByBank2,channelBalance2,recordBookingredeem

import json
import decimal,datetime

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o,"%Y-%m-%d %H:%M:%S")
        super(MyJSONEncoder, self).default(o)

def selectTradeDetail3(lb,accountid,prodcode):

    pas=queryProductAsset(lb,accountid,prodcode)

    totalCount={"applyamount":0,"balance":0,"profit":0}
    dataresult={"traderecord":None,"prodbanklist":None}
    for p in pas:
        _p=DictObj(p)
        totalCount["applyamount"] = totalCount["applyamount"]+_p.applyamount
        totalCount["balance"] = totalCount["balance"] + _p.balance
        totalCount["profit"] = totalCount["profit"] + _p.profit

    pads=queryProductAssetDetail(lb,accountid)
    dataresult["traderecord"]=pads
    dataresult=dict(dataresult.items() + totalCount.items())

    if lb == "1":
        sharebank=shareByBank(prodcode,accountid)
        dataresult['prodbanklist']=sharebank

    return DictObj(dataresult)


def selectTradeDetail4(lb,accountid,prodcode):
    pas = queryProductAsset2(lb, accountid, prodcode)
    totalCount = {"applyamount": 0, "balance": 0, "profit": 0}
    dataresult = {"traderecord": None, "prodbanklist": None}
    for p in pas:
        totalCount["applyamount"] = totalCount["applyamount"] + p.applyamount
        totalCount["balance"] = totalCount["balance"] + p.balance
        totalCount["profit"] = totalCount["profit"] + p.profit

    pads = queryProductAssetDetail2(lb, accountid)
    pads_dict = [dict(zip(result.keys(), result)) for result in pads]
    dataresult["traderecord"] = pads_dict
    dataresult = dict(dataresult.items() + totalCount.items())

    if lb == "1":
        sharebank = shareByBank2(prodcode, accountid)
        sharebank_dict = []
        for share in sharebank:
            share_dict = dict(zip(share.keys(), share))
            channelbalance=channelBalance2(cljj_user_id=accountid,bank_card_no=share.bank_card_no,fund_code=share.prodcode)
            share_dict["usable_share"]=channelbalance.usable_share
            sharebank_dict.append(share_dict)

        dataresult['prodbanklist'] = sharebank_dict
    return dataresult

def recordBr(cljj_user_id,prodcode):
    data=recordBookingredeem(cljj_user_id,prodcode)
    return data


if "__main__" == __name__:
    result=selectTradeDetail4("1","ff95336dd20b8ae1f1a0dc930dd8d03d","900020")
    result=json.dumps(result,cls=MyJSONEncoder)
    print(result)