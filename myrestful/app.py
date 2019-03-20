# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 15:23
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : app.py

from flask import Flask, Blueprint

# import pymysql
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


flaskapp = Flask(__name__)
api_blueprint = Blueprint("api",__name__)
api = Api(api_blueprint)

from config import default
flaskapp.config.from_object(default)

# flaskapp.config["SQLALCHEMY_DATABASE_URI"]= 'mysql://cljj_base_event:cljj_base_event@192.168.1.99:3306/cljj_base_event'
# flaskapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db2=SQLAlchemy(flaskapp)
#
# db = pymysql.connect(host="192.168.1.99",
#                      user="cljj_base_event", password="cljj_base_event",
#                      db="cljj_base_event", port=3306, cursorclass=pymysql.cursors.DictCursor)

flaskapp.register_blueprint(api_blueprint, url_prefix='/api')

from myrestful.resources.benchmark import BenchMark,RecordBr
api.add_resource(BenchMark, '/benchMark')
api.add_resource(RecordBr, '/recordBr')
