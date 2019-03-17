# -*- coding: utf-8 -*-
# Author : monster
#登陆接口
import unittest
import json
from Interface_Project_201812.common.Forward_loan_request import Forward_Loan
from Interface_Project_201812.common.Read_Excel import Read_Excel
from Interface_Project_201812.common import File_Path
from Interface_Project_201812.common.Load_Conf import Load_Conf
from ddt import ddt,data,unpack,file_data #file_data是读取文件数据，data是读取单个/多个数据
from Interface_Project_201812.common.get_mobilephone_re import Replace_Phone
from Interface_Project_201812.common.mylogger import MyLogger
get_excel=Read_Excel(File_Path.excel_path)
cases=get_excel.read_excel('user-login')
Cookies=None
@ddt
class Test_Forward_loan_request(unittest.TestCase):
    def setUp(self):
        MyLogger.info('-----登陆接口测试开始-----')

    @data(*cases)#将excel拆分为一条一条的用例
    def test_forward_loan(self,item):
        global Cookies
        MyLogger.info('用例标题：{}'.format(item.title))
        url = Load_Conf().load_conf('api','url_prefix')#获取配置文件的url
        Url = url+item.url#拼接配置文件的url和excel表的url
        MyLogger.info('url地址：{}'.format( Url))
        MyLogger.info(item.case_id)
        if item.case_id=='test_2_001': #将第一条登录用例的请求参数进行替换
            ph=item.request_data
            item.request_data =Replace_Phone().replace_phone(ph)
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)#json.loads（）将字符串格式转化为字典
        else:
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)
        MyLogger.debug('响应正文：{}'.format(result_res.get_text()))
        if result_res.get_cookies():
            Cookies=result_res.get_cookies()
        try:
            self.assertEqual(item.expected,int(result_res.get_json()['code']))
            test_result = 'Pass'
        except AssertionError as e:
            test_result = 'Fail'
            MyLogger.debug('断言错误显示为：{}'.format(e))
            # raise e  #raise e是抛出异常，终止程序，所以raise上面的print可以正常执行，但是result参数就传不出来了，会被截掉
        finally:
            MyLogger.info('本次用例执行的结果是：{}'.format(test_result))
        # print(test_result)
        # get_excel.write_actual(sheet_name='user-login', case_id=item.case_id, actual=result_res.get_text(),
        #                            result=test_result)  #关闭Excel才能对其执行写入操作！！
    def tearDown(self):
        MyLogger.info('--------------------------测试结束---------------------------')



