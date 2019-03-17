# -*- coding: utf-8 -*-
# Author : monster
#提现接口
'''
1.从数据库拿到该账号的总金额
2.判断要提现的金额是否<=总金额
3.提现成功后进行数据库校验，即数据库剩余金额=（总金额-提现金额）
'''
import unittest
import json
from Interface_Project_201812.common.get_mobilephone_re import Replace_Phone
from Interface_Project_201812.common.Forward_loan_request import Forward_Loan
from Interface_Project_201812.common.Read_Excel import Read_Excel
from Interface_Project_201812.common import File_Path
from Interface_Project_201812.common.Load_Conf import Load_Conf
from Interface_Project_201812.common.mysql_data import MySql_Data
from ddt import ddt,data,unpack,file_data #file_data是读取文件数据，data是读取单个/多个数据
get_excel=Read_Excel(File_Path.excel_path)
cases=get_excel.read_excel('user-withdraw')
Cookies=None
@ddt
class Test_recharge_request(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----提现接口开始测试-----')
        global mysql
        global total_amount
        global sql2
        sql2 = 'SELECT LeaveAmount FROM future.member WHERE MobilePhone="18999999854"'
        mysql=MySql_Data()
        total_amount = mysql.get_leaveamount(sql2) #从数据库拿到该账号的总金额

    @data(*cases)#将excel拆分为一条一条的用例
    def test_recharge(self,item):
        global Cookies
        print('用例标题：',item.title)
        url = Load_Conf().load_conf('api','url_prefix')#获取配置文件的url
        Url = url+item.url#拼接配置文件的url和excel表的url
        print('url地址：', Url)
        if item.case_id=='test_2_001':
            ph = item.request_data
            item.request_data = Replace_Phone().replace_phone(ph)
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)
        elif item.case_id=='test_4_001' or item.case_id=='test_4_002':
            ph = item.request_data
            item.request_data = Replace_Phone().replace_phone(ph)
            print(item.request_data)
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method, cookies=Cookies)
        else:
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)
        print('响应正文：',type(result_res.get_text()),result_res.get_text())
        # print(dict(result_res.get_text().msg))
        if result_res.get_cookies():
            Cookies=result_res.get_cookies()
        if json.loads(result_res.get_text())['msg']=='提现成功':
            new_amount = MySql_Data().get_leaveamount(sql2)#数据库查询提现后的金额
            print('数据库查找 提现后的金额为：',new_amount)
            print(type(json.loads(item.request_data)['amount']),json.loads(item.request_data)['amount'])
            recharge_amount = float(total_amount)-float(json.loads(item.request_data)['amount']) #获取提现后的金额
            print(recharge_amount)
            try:
                self.assertEqual(float(new_amount),recharge_amount) #判断数据库提现后的金额和流水记录后的金额是否一致
                print('数据库校验成功！')
            except AssertionError as e:
                print('校验失败，错误为：', e)
        try:
            self.assertEqual(item.expected,int(result_res.get_json()['code']))
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
        mysql.close()

