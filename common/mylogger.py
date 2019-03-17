# encoding: utf-8 
import logging
import time
import os
from Interface_Project_201812.common import File_Path

def get_today(): #time.localtime(time.time())获取当天格式化的时间
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

def get_logger_dir():#获取当天日志的存放路径
    logger_dir=os.path.join(File_Path.logs_path,get_today())#将配置文件的log路径和当地时间直接join成新路径
    if not os.path.isdir(logger_dir):#isdir判断拼接的新路径是否存在，不存在则makedirs创建该路径
        os.makedirs(logger_dir)
    return logger_dir


#定义一个日志收集器，所有的日志都存放在这里
mylogger=logging.getLogger('test-logging')
mylogger.setLevel('DEBUG')#设置日志级别

def get_handler(levels):
    if levels == 'error':
        mylogger.addHandler(MyLogger.error_handle)  # 将error日志存放
    else:
        mylogger.addHandler(MyLogger.info_handle)  # 存放info
    mylogger.addHandler(MyLogger.ch)

def move_handler(levels):
    if levels=='error':
        mylogger.removeHandler(MyLogger.error_handle)#将error日志移除
    else:
        mylogger.removeHandler(MyLogger.info_handle)#移除info
    mylogger.removeHandler(MyLogger.ch)


class MyLogger:
    logger_dir=get_logger_dir()
    # print(logger_dir)
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s- %(filename)s - %(message)s')#设置日志格式
    #DEBUG信息的输出在console
    ch=logging.StreamHandler()
    ch.setLevel('DEBUG')
    ch.setFormatter(formatter)

    #最终INFO信息的日志文件存放的地方
    log_txt=os.path.join(logger_dir,'logs.txt')#拼接存放log的路径
    # print(log_txt)
    info_handle=logging.FileHandler(filename=log_txt,encoding='utf-8')
    info_handle.setLevel('INFO')
    info_handle.setFormatter(formatter)

    # 最终ERROR信息的日志文件存放的地方
    error_txt = os.path.join(logger_dir, 'error.txt')  # 拼接存放log的路径
    error_handle = logging.FileHandler(error_txt, encoding='utf-8')
    error_handle.setLevel('ERROR')
    error_handle.setFormatter(formatter)

    @staticmethod
    def debug(msg):
        get_handler('debug')
        mylogger.debug(msg)
        move_handler('debug')

    @staticmethod
    def info(msg):
        get_handler('info')
        mylogger.debug(msg)
        move_handler('info')

    @staticmethod
    def error(msg):
        get_handler('error')
        mylogger.debug(msg)
        move_handler('error')


if __name__ == '__main__':
    MyLogger.info('我是info')
    MyLogger.debug('我是debug')
    MyLogger.error('我是error')