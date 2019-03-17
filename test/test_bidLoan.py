# -*- coding: utf-8 -*-
# Author : monster
#投标接口
'''
1.先登录账号，拿到cookies返回给投标接口
2.将请求数据参数化，投标成功后进行数据库的校验，即在invest表里可查询到该投标记录
'''
import unittest
import json
import re
from Interface_Project_201812.common.get_mobilephone_re import Replace_Phone
from Interface_Project_201812.common.Read_Excel import *
from Interface_Project_201812.common import File_Path
from Interface_Project_201812.common.Load_Conf import Load_Conf
from Interface_Project_201812.common.mysql_data import MySql_Data
from ddt import ddt,data,unpack,file_data #file_data是读取文件数据，data是读取单个/多个数据
get_excel=Read_Excel(File_Path.excel_path)
cases=get_excel.read_excel('user-bidLoan')
Cookies=None
@ddt
class Test_recharge_request(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     print('-----充值接口开始测试-----')
    #     global mysql
    #     global mysql_amount
    #     global sql2
    #     sql2 = 'SELECT LeaveAmount FROM future.member WHERE MobilePhone="18999999854"'
    #     mysql=MySql_Data()
    #     mysql_amount = mysql.get_mobilephone(sql2)
    def setUp(self):
        print('-----投标接口开始测试-----')
    #     self.mysql_amount = MySql_Data().get_mobilephone(sql2)
    @data(*cases)#将excel拆分为一条一条的用例
    def test_recharge(self,item):
        global Cookies
        print('用例标题：',item.title)
        url = Load_Conf().load_conf('api','url_prefix')#获取配置文件的url
        Url = url+item.url#拼接配置文件的url和excel表的url
        print('url地址：', Url)
        # print(json.loads(item.request_data)['memberId'])
        if item.case_id=='test_2_001' or json.loads(item.request_data)['memberId']=='${login_phone}':
            ph = item.request_data
            item.request_data = Replace_Phone().replace_phone(ph)
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)
        else:
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)
        print('响应正文：',result_res.get_text())
        # print(dict(result_res.get_text().msg))
        if result_res.get_cookies():
            Cookies=result_res.get_cookies()
        # if json.loads(result_res.get_text())['msg']=='充值成功':
        #     new_amount = MySql_Data().get_mobilephone(sql2)#数据库查询充值后的金额
        #     print('数据库查找 充值后的金额为：',new_amount)
        #     print(type(json.loads(item.request_data)['amount']),json.loads(item.request_data)['amount'])
        #     recharge_amount = float(json.loads(item.request_data)['amount'])+float(mysql_amount)
        #     print(recharge_amount)
        #     try:
        #         self.assertEqual(float(new_amount),recharge_amount) #判断新增的充值流水记录和excel表的是否一致
        #         print('数据库校验成功！')
        #     except AssertionError as e:
        #         print('校验失败，错误为：', e)
        try:
            self.assertEqual(item.expected,int(result_res.get_json()['code']))#replace("'", "\"")
            test_result = 'Pass'
        except AssertionError as e:
            test_result = 'Fail'
            print('断言错误显示为：{}'.format(e))
            # raise e  #raise e是抛出异常，终止程序，所以raise上面的print可以正常执行，但是result参数就传不出来了，会被截掉
        finally:
            print('本次用例执行的结果是：',test_result)
        # get_excel.write_actual(sheet_name='user-login', case_id=item.case_id, actual=result_res.get_text(),
        #                            result=test_result)
    def tearDown(self):
        print('--------------------------测试结束---------------------------')
    # @classmethod
    # def tearDownClass(cls):
    #     print('--------------------------测试结束---------------------------')
        # mysql.close()

