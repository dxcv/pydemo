# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 11:14
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : logfilter.py


#!/bin/python
# -*- encoding:utf-8 -*-

import sys
import logging
import json
import types

class ContextFilter(logging.Filter):
    """
    这是一个控制日志记录的过滤器。
    """
    def filter(self, record):
        try:
            filter_key = record.EXTRA
            if isinstance(filter_key,types.ListType) :
                msg = record.message
                for key in filter_key:
                    if key.lower() in msg or key.upper() in msg :
                        info=json.loads(msg)
                        info[key.lower()]="xx"
                        record.message = json.dumps(info)
                        # print(record.message)
                        logging.info(record.message)
        except AttributeError as e:
            return False

        return True




import logging.handlers
from pythonjsonlogger import jsonlogger
import datetime

class JsonFormatter(jsonlogger.JsonFormatter, object):
    def __init__(self,
                 fmt="%(asctime) %(name) %(processName) %(filename)  %(funcName) %(levelname) %(lineno) %(module) %(threadName) %(message)",
                 datefmt="%Y-%m-%dT%H:%M:%SZ%z",
                 style='%',
                 extra={}, *args, **kwargs):
        self._extra = extra
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, datefmt=datefmt, *args, **kwargs)

    def process_log_record(self, log_record):
        # Enforce the presence of a timestamp
        if "asctime" in log_record:
            log_record["timestamp"] = log_record["asctime"]
        else:
            log_record["timestamp"] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ%z")

        if self._extra is not None:
            for key, value in self._extra.items():
                log_record[key] = value
        return super(JsonFormatter, self).process_log_record(log_record)


if __name__ == '__main__':
    # 创建日志对象
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


    file_handler = logging.FileHandler("./log.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)s [%(filename)s %(lineno)d] %(message)s"))

    logger.addHandler(file_handler)

    # 添加日志处理器，输出日志到控制台
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(asctime)-15s %(levelname)s [%(filename)s %(lineno)d] %(message)s"))
    console_handler.addFilter(ContextFilter())
    logger.addHandler(console_handler)


    # 记录日志
    # logger.debug('debug message')
    # logger.info('info message')

    rsp=json.dumps({"name":"xuliangjun","mobile":"15216888888"})
    logger.warning(rsp, extra={"EXTRA":["mobile"]})
    logger.error('error message1', extra={"EXTRA":["mobile"]})
    logger.error('error message2', extra={"EXTRA":["mobile"]})