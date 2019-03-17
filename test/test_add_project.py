# encoding: utf-8
#新增项目接口
'''
1.借款人先登录，登录成功后将cookies返回给全局
2.从数据库获取借款人的memberid，放在setupclass中
2.借款人用memberid进行新增项目
'''
import unittest
import json
from Interface_Project_201812.common.get_mobilephone_re import *
from Interface_Project_201812.common.Forward_loan_request import Forward_Loan
from Interface_Project_201812.common.Read_Excel import Read_Excel
from Interface_Project_201812.common import File_Path
from Interface_Project_201812.common.Load_Conf import Load_Conf
from Interface_Project_201812.common.mysql_data import MySql_Data
from ddt import ddt,data,unpack,file_data #file_data是读取文件数据，data是读取单个/多个数据
get_excel=Read_Excel(File_Path.excel_path)
cases=get_excel.read_excel('project-add')
Cookies=None
@ddt
class Test_recharge_request(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----新增项目接口开始测试-----')
        global mysql
        global mysql_memberid
        global sql2
        # sql2 = 'SELECT ID from future.member where MobilePhone={}'.format(LoKey.borrow_phone)
        mysql=MySql_Data()
        # mysql_memberid = mysql.get_mobilephone(sql2)

    @data(*cases)#将excel拆分为一条一条的用例
    def test_recharge(self,item):
        global Cookies
        print('用例标题：',item.title)
        url = Load_Conf().load_conf('api','url_prefix')#获取配置文件的url
        Url = url+item.url#拼接配置文件的url和excel表的url
        print('url地址：', Url)
        # print(item.request_data)
        if item.case_id=='test_2_001':
            ph = item.request_data
            item.request_data = Replace_Phone().replace_phone(ph)
            print(type(json.loads(item.request_data)['mobilephone'])) #打印替换后的借款人请求数据
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)
        # elif item.case_id!='test_7_002' or item.case_id!='test_7_010' or item.case_id!='test_7_011':
        elif json.loads(item.request_data)['memberId']=='${borrow_id}':
            ph = item.request_data
            item.request_data = Replace_Phone().replace_phone(ph)
            print(item.request_data)#打印替换后memberid的请求数据
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method, cookies=Cookies)
        else:
            result_res = Forward_Loan(Url=Url, Param=json.loads(item.request_data), Method=item.method,cookies=Cookies)
        print('响应正文：',type(result_res.get_text()),result_res.get_text())
        # print(dict(result_res.get_text().msg))
        if result_res.get_cookies():
            Cookies=result_res.get_cookies()
        if json.loads(result_res.get_text())['msg']=='加标成功':
            sql3='SELECT Title FROM future.loan WHERE MemberID={} ORDER BY CreateTime DESC LIMIT 1'.format(LoKey.borrow_id)
            sql_title = MySql_Data().get_loan_title(sql3)[0]#数据库查询加标成功后的title
            print('数据库查询加标成功后的title：',sql_title)
            print(type(json.loads(item.request_data)['title']),json.loads(item.request_data)['title'])
            excel_title=json.loads(item.request_data)['title']
            # recharge_amount = float(json.loads(item.request_data)['amount'])+float(mysql_amount)
            # print(recharge_amount)
            try:
                self.assertEqual(sql_title,excel_title) #判断新增的充值流水记录和excel表的是否一致
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

