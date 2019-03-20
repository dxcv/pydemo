#!/usr/bin/env python
# encoding: utf-8

"""
    File name: account.py
    Function Des: ...
    ~~~~~~~~~~
    
    author: Jerry <cuteuy@gmail.com> <http://www.skyduy.com>
    
"""
from flask_restful import reqparse

# ------------ register parser ------------

register_parser = reqparse.RequestParser(bundle_errors=True)

register_parser.add_argument(
    'lb', dest='lb',
    type=str, location='args',
    required=True, help='{error_msg}',
)

register_parser.add_argument(
    'accountid', dest='accountid',
    type=unicode, location='args',
    required=True, help='{error_msg}',
)

register_parser.add_argument(
    'prodcode', dest='prodcode',
    type=str, location='args',
    required=True, help='{error_msg}',
)


# ------------ 预约赎回控制 ------------
record_bookingredeem_parser=reqparse.RequestParser(bundle_errors=True)
record_bookingredeem_parser.add_argument(
    'cljj_user_id', dest='cljj_user_id',
    type=str, location='args',
    required=True, help='{error_msg}',
)
record_bookingredeem_parser.add_argument(
    'prodcode', dest='prodcode',
    type=str, location='args',
    required=True, help='{error_msg}',
)


# ------------ account update parser ------------
account_update_parser = reqparse.RequestParser()

account_update_parser.add_argument(
    'nickname', dest='nickname',
    type=unicode, location='form',
    required=True, help='This is new nickname',
)

account_update_parser.add_argument(
    'des', dest='des',
    type=unicode, location='form',
    required=False, help='The user\'s new description',
)

account_update_parser.add_argument(
    'old_password', dest='old_password',
    type=str, location='form',
    required=False, help='This is old password',
)

account_update_parser.add_argument(
    'new_password', dest='new_password',
    type=str, location='form',
    required=False, help='This is new password',
)

account_update_parser.add_argument(
    'confirm', dest='confirm',
    type=str, location='form',
    required=False, help='This is new password\'s confirm',
)
