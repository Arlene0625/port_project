# -*- coding: utf-8 -*-
# Author : monster
'''1，测试用例设计，需要包括测试用例说明，接口路径，测试数据，期望结果
2，格式可以参考附件中Excel
3，搭建好自己的项目框架，将之前已经学过的内容，尝试自己写一遍。
其中：requests封装类，需要实现的功能是一个函数就可以负责模拟全部请求方法的调用。
Excel读取类，实现读和写
配置文件读取类，实现加载配置文件项'''
import requests
from Interface_Project_201812.common.Load_Conf import Load_Conf
from Interface_Project_201812.common import File_Path
import os
class Forward_Loan:
    def __init__(self,Url,Param,Method,cookies=None):#Regname=None
        try:
            if Method == 'get':
                self.return_res = requests.get(Url, Param, cookies=cookies)
            elif Method == 'post':
                self.return_res = requests.post(Url, Param, cookies=cookies)
            # print(self.return_res.cookies)
        except Exception as e:
            raise e
    def get_text(self):
        return self.return_res.text
    def get_status_code(self):
        return self.return_res.status_code
    def get_json(self):
        return self.return_res.json()
    def get_cookies(self):
        return self.return_res.cookies
# if __name__ == '__main__':
#     F=Forward_Loan(Url='http://test.lemonban.com/futureloan/mvc/api/member/login',Param={"mobilephone":18999999854,"pwd":"1234567890"},Method='get')
#     print(F.get_text())
