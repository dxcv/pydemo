# -*- coding: utf-8 -*-
# @Time    : 2019/1/17 16:21
# @Author  : dodo8619
# @Email   : lj16888619@gmail.com
# @File    : mainModule.py

import logging
import subModule

logger = logging.getLogger("mainModule")
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console)

logger.info("creating an instance of subModule.subModuleClass")
a = subModule.SubModuleClass()
logger.info("calling subModule.subModuleClass.doSomething")
a.doSomething()
logger.info("done with  subModule.subModuleClass.doSomething")
logger.info("calling subModule.some_function")
subModule.som_function()
logger.info("done with subModule.some_function")