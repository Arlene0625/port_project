# -*- coding: utf-8 -*-
# Author : monster
#获取用户列表
'''登录账号后获取用户列表'''
import unittest
import json
from Interface_Project_201812.common.get_mobilephone_re import Replace_Phone
from Interface_Project_201812.common.Forward_loan_request import Forward_Loan
from Interface_Project_201812.common.Read_Excel import Read_Excel
from Interface_Project_201812.common import File_Path
from Interface_Project_201812.common.Load_Conf import Load_Conf
from ddt import ddt,data,unpack,file_data #file_data是读取文件数据，data是读取单个/多个数据
get_excel=Read_Excel(File_Path.excel_path)
cases=get_excel.read_excel('user-list')
Cookies=None
@ddt
class Test_recharge_request(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----获取用户列表接口开始测试-----')

    @data(*cases)#将excel拆分为一条一条的用例
    def test_recharge(self,item):
        global Cookies
        print('用例标题：',item.title)
        url = Load_Conf().load_conf('api','url_prefix')#获取配置文件的url
        Url = url+item.url#拼接配置文件的url和excel表的url
        print('url地址：', Url)
        if item.case_id=='test_2_001' or item.case_id=='test_5_001':
            ph = item.request_data
            item.request_data = Replace_Phone().replace_phone(ph)
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)#eval去掉参数前后的引号
        else:
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)  # eval去掉参数前后的引号
        print('响应正文：',type(result_res.get_text()))
        if result_res.get_cookies():
            Cookies=result_res.get_cookies()
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

    @classmethod
    def tearDownClass(cls):
        print('--------------------------测试结束---------------------------')
