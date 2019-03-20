# -*- coding: utf-8 -*-
# @Time    : 2019/1/17 16:21
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : subModule.py

import logging

module_logger = logging.getLogger("mainModule.sub")


class SubModuleClass(object):
    def __init__(self):
        self.logger = logging.getLogger("mainModule.sub.module")
        self.logger.info("creating an instance in SubModuleClass")

    def doSomething(self):
        self.logger.info("do something in SubModule")
        a = []
        a.append(1)
        self.logger.debug("list a = " + str(a))
        self.logger.info("finish something in SubModuleClass")


def som_function():
    module_logger.info("call function some_function")