# -*- coding:utf-8 -*-

import yaml
import logging.config
import os

class MyLog(object):

    def __init__(self,name=None):
        self.name = name
        MyLog.setup_logging(default_path='./log.yaml')


    @staticmethod
    def setup_logging(default_path='log.yaml', default_level=logging.INFO):
        """
        Setup logging configuration
        """
        if os.path.exists("mylog"):
            pass
        else:
            os.mkdir('mylog')
        path = default_path
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = yaml.load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
            print('the input path doesn\'t exist')



    def getLog(self):
        logger = logging.getLogger(self.name)
        return logger




if "__main__" == __name__ :
    logger = MyLog().getLog()
    logger.info("test")

