# -*- coding: utf-8 -*-
# Author : monster
import configparser
import os
from Interface_Project_201812.common import File_Path
class Load_Conf:
    #section,option
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(os.path.join(File_Path.conf_path,'switch.conf'), encoding='utf-8')
        if self.cf.getboolean('switch','on'):
            self.cf.read(os.path.join(File_Path.conf_path, 'formal.conf'), encoding='utf-8')
        else:
            self.cf.read(os.path.join(File_Path.conf_path, 'web_test.conf'), encoding='utf-8')
    def load_conf(self,a,b):
        return self.cf.get(a,b)#get返回str类型的值
    def load_conf_bool(self,a,b):
        return self.cf.getboolean(a,b)#get返回bool类型的值
    def load_conf_int(self,a,b):
        return self.cf.getint(a,b)#get返回int类型的值


if __name__ == '__main__':
    k=Load_Conf().load_conf('api','url_prefix')
    k2 = Load_Conf().load_conf('borrow', 'borrow_phone')

    print(k2)

