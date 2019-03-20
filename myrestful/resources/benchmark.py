# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 15:28
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : benchmark.py

from flask_restful import Resource,marshal_with ,request

from myrestful.util.fields.account import account_trade_fields ,record_bookingredeem_fields
from myrestful.util.parses.account import register_parser,record_bookingredeem_parser

from myrestful.handler.accountAssert import selectTradeDetail4 , recordBr


import json
import decimal,datetime

class MyJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return datetime.datetime.strftime(o,"%Y-%m-%d %H:%M:%S")
        super(MyJSONEncoder, self).default(o)



class BenchMark(Resource):

    @marshal_with(account_trade_fields)
    def get(self):
        # flask_restful.abort(400, data= generate_response())
        account_args = register_parser.parse_args()
        print(request.args.get("lb"))
        try:
            # print(account_args.lb,account_args.accountid,account_args.prodcode)
            datas=selectTradeDetail4(account_args.lb,account_args.accountid,account_args.prodcode)
            # result = json.dumps(datas, cls=MyJSONEncoder)
            return datas
        except Exception as e:
            print(e)
        return None


class RecordBr(Resource):
    @marshal_with(record_bookingredeem_fields)
    def get(self):
        params=record_bookingredeem_parser.parse_args()
        data=recordBr(params.cljj_user_id,params.prodcode)
        return data