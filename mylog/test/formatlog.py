# -*- coding: utf-8 -*-
# @Time    : 2019/1/18 14:54
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : formatlog.py


import logging.config

import structlog
from structlog import configure, processors, stdlib, threadlocal



import logging.handlers
from pythonjsonlogger import jsonlogger
import datetime

class JsonFormatter(jsonlogger.JsonFormatter):

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


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'class': 'JsonFormatter' ,
            'format': "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        }
    },
    'handlers': {
        'json': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
            "stream":"ext://sys.stdout"
        }
    },
    'loggers': {
        '': {
            'handlers': ['json'],
            'level': logging.INFO
        }
    }
})

configure(
    context_class=threadlocal.wrap_dict(dict),
    logger_factory=stdlib.LoggerFactory(),
    wrapper_class=stdlib.BoundLogger,
    processors=[
        stdlib.filter_by_level,
        stdlib.add_logger_name,
        stdlib.add_log_level,
        stdlib.PositionalArgumentsFormatter(),
        processors.TimeStamper(fmt="iso"),
        processors.StackInfoRenderer(),
        processors.format_exc_info,
        processors.UnicodeDecoder(),
        stdlib.render_to_log_kwargs]
)

# default_logger = logging.getLogger("LogDemo")
# default_logger.level = logging.INFO
# default_logger.debug("test debug msg")
# # 测试消息
# default_logger.info("test single msg")
# # 测试打印字典
# default_logger.info({"key1": "val1", "key2": "val2"})

# struct_logger = logging.getLogger("LogDemo")
# # 打印log方式一，参数为key=value形式, 此时第一个参数msg必填
# struct_logger.info("event")
# # 打印log方式二，参数为dict形式
# struct_logger.info({"key1": "1", "key2": "2"})



import logging
import json_log_formatter

# logging.Formatter("%(asctime)-15s %(levelname)s [%(filename)s %(lineno)d] %(message)s")
formatter = json_log_formatter.JSONFormatter()

json_handler = logging.FileHandler(filename='my-log.json')
json_handler.setFormatter(formatter)

logger = logging.getLogger('my_json')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)

logger.info(msg="xx")
