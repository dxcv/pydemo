# -*- coding:utf-8 -*-

from logtest import MyLog


def dodo():
    logger =MyLog().getLog()
    logger.info("test")

def bus():
    logger = MyLog("account").getLog()
    logger.info("account")

def bus_error():
    try:
        logger = MyLog("account").getLog()
        int("a")
    except Exception as e :
        logger.error("system error",exc_info=1)

if "__main__" == __name__ :
    bus_error()