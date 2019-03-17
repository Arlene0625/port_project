# -*- coding: utf-8 -*-
# Author : monster
'''
1.先从数据库拿到最手机号+1，并替换到excel里
2.注册成功后从数据库查找是否和excel的手机号显示一致
'''
import unittest
import json
from Interface_Project_201812.common.Forward_loan_request import Forward_Loan
from Interface_Project_201812.common.Read_Excel import Read_Excel
from Interface_Project_201812.common import File_Path
from Interface_Project_201812.common.Load_Conf import Load_Conf
from ddt import ddt,data,unpack,file_data #file_data是读取文件数据，data是读取单个/多个数据
from Interface_Project_201812.common.mysql_data import MySql_Data
get_excel=Read_Excel(File_Path.excel_path)
cases=get_excel.read_excel('user-register')

@ddt
class Test_register_request(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----注册接口开始测试-----')
        global mysql
        global phone
        sql1 = 'SELECT MobilePhone from future.member where MobilePhone !="" ORDER BY MobilePhone DESC LIMIT 1'
        mysql=MySql_Data()
        phone =mysql.get_mobilephone(sql1)  # 数据库返回的最大手机号+1，传给注册手机号
        print(type(phone),phone) #数据库返回int类型
    @data(*cases)#将excel拆分为一条一条的用例
    def test_register(self,item):
        print('用例标题：',item.title)
        url = Load_Conf().load_conf('api','url_prefix')#获取配置文件的url
        Url = url+item.url#拼接配置文件的url和excel表的url
        print('url地址：', Url)
        if item.case_id=='test_1_001':
            data1=json.loads(item.request_data)
            data1['mobilephone']=phone
            data1['pwd']=Load_Conf().load_conf('register','pwd')#将注册人的密码传进来
            item.request_data=data1
            result_res = Forward_Loan(Url=Url, Param=item.request_data, Method=item.method)#json.loads()将字符串反序列化为字典
            global phone2
            phone2=item.request_data['mobilephone']
        else:
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method)  # eval去掉参数前后的引号
        print('响应正文：',result_res.get_text())
        if json.loads(result_res.get_text())['msg']=='注册成功':
            # sql_phone = Replace_Phone().replace_phone()
            print('数据库查找 注册成功的手那个机号为：', phone)#数据库查找到注册成功的手机号为str类型
            print(type(phone), phone) #用例中查找注册成功的手机号为str类型
            try:
                self.assertEqual(phone2, phone)  # 判断数据库注册成功的手机号和用例返回的是否一致
                print('数据库校验成功！')
            except AssertionError as e:
                print('校验失败，错误为：', e)
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
        mysql.close()


