# -*- encoding: utf-8 -*- 编码

# 日志模块
import logging

# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s	%(filename)s:%(lineno)d:%(funcName)s	%(process)d:%(thread)d	%(levelname)s	%(message)s',
                filename='logs/muu_recomm.log',
                filemode='a')
#    datefmt='%a %Y-%m-%d %H:%M:%S',
                

# 创建一个logger    
logger = logging.getLogger()  

#logger.setLevel(logging.DEBUG)  

logger.debug('module log __init__')



