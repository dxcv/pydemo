# -*- coding: utf-8 -*-
# @Time    : 2019/1/17 16:34
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : yamllog.py

#https://www.cnblogs.com/qianyuliang/p/7234217.html  参考文章

'''
   logging
      ------ level
      ------ handler
                ------ level
                ------ format
                ------ filter
'''

'''
按照模块生成日志文件；
系统所有错误日志统一收集；
'''

import json
import yaml
import logging.config
import os

def setup_logging_json(default_path = "jsonlog.json",default_level = logging.INFO,env_key = "LOG_CFG"):
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,"r") as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level = default_level)


def setup_logging_yaml(default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging_json()


def common():
    '''公共'''
    logger = logging.getLogger()
    logger.info("common param:")
    try:
        int("ss")
    except:
        logger.error("system error", exc_info=1) #exc_info=1  打印具体异常
    logger.info("common response:")

def account():
    '''账户'''
    logger = logging.getLogger(name="accout")
    logger.info("accout param:")

    rsp = json.dumps({"name": "xuliangjun", "mobile": "15216888888"})
    logger.info(rsp, extra={"EXTRA": ["mobile"]})

    logger.info("accout response: ")

def trade():
    '''交易'''
    logger = logging.getLogger(name="trade")
    logger.info("trade param:")
    try:
        int("ss")
    except:
        logger.error("system error", exc_info=1) #exc_info=1  打印具体异常
    logger.info("trade response: ")





if __name__ == "__main__":
    common()
    account()
    trade()