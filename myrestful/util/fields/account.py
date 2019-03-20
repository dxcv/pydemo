# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 9:43
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : account.py


from flask_restful import fields

prodbank_fields = {}
prodbank_fields['bank_name'] = fields.String(attribute='bank_name')
prodbank_fields['applyamount'] = fields.Float(attribute='applyamount')
prodbank_fields['lastfour_bankcard'] = fields.String(attribute='lastfour_bankcard')
prodbank_fields['profit'] = fields.Float(attribute='profit')
prodbank_fields['prodcode'] = fields.String(attribute='prodcode')
prodbank_fields['bank_card_no'] = fields.Integer(attribute='bank_card_no')
prodbank_fields['producttype'] = fields.String(attribute='producttype')
prodbank_fields['usable_share'] = fields.Float(attribute='usable_share')
prodbank_fields['balance'] = fields.Float(attribute='balance')
prodbank_fields['fundname'] = fields.String(attribute='fundname')
prodbank_fields['accountid'] = fields.String(attribute='accountid')

traderecord={
    "apply_status":fields.String,
    "bank_name":fields.String,
    "bankcardno":fields.String,
    "lastfour_bankcard":fields.String,
    "prodcode":fields.String,
    "ordertraceno":fields.String,
    "datetime":fields.DateTime,
    "apply_amount":fields.Float,
    "confirm_amount":fields.Float,
    "producttype":fields.String,
    "apkind":fields.String,
    "fundname":fields.String,
    "confirm_share":fields.Float,
    "accountid":fields.String

}

account_trade_fields = {
    'profit':fields.Float,
    'balance':fields.Float,
    'applyamount':fields.Float,
    'prodbanklist':fields.List(fields.Nested(prodbank_fields)),
    'traderecord':fields.List(fields.Nested(traderecord)),
}

# cljj_user_id = db2.Column(db2.Integer, unique=True, primary_key=True)
# prodcode = db2.Column(db2.String(8), unique=True)
# bookingdate = db2.Column(db2.String(10))
# bookingstate = db2.Column(db2.String(1))
# ifhandle = db2.Column(db2.String(1))
# datadate = db2.Column()

record_bookingredeem_fields = {
    'cljj_user_id':fields.String,
    'prodcode':fields.String,
    'bookingdate':fields.DateTime,
    'bookingstate':fields.String,
    'ifhandle':fields.String,
    'datadate':fields.DateTime,
}


# for get /accounts/<account_id>
account_detail_fields = {
    'id': fields.String,
    'username': fields.String,
    'nickname': fields.String,
    'role': fields.String,
    'description': fields.String,
    'created': fields.DateTime,
}

# for get /accounts
account_simple_fields = {
    'id': fields.String,
    'nickname': fields.String,
    'role': fields.String,
}

accounts_fields = {
    'accounts': fields.List(fields.Nested(account_simple_fields))
}