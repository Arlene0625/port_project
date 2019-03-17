# -*- coding: utf-8 -*-
# @Time    : 2019/1/6 0006 下午 1:54
# @Author  : monster
# @Email   : 1300147905@qq.com
# @File    : mock_test.py
'''return_value:定义mock方法的返回值，可以是一个值，也可以是一种方法或实例
side_effect:他会覆盖return_value，用来抛出异常或者动态改变返回值，且side_effect是一个可迭代对象，有序调用'''
'''断言方法：
1.assert_called:至少被调用一次
2.assert_called_once:只被调用一次
3.assert_called_with:被调用使用正确的参数
4.assert_called_once_with:使用参数且被调用一次
5.assert_any_call:曾经被调用过
6.assert_has_calls:多次被调用
7.assert_not_called:从未被调用
'''
'''统计
called：是否被调用，返回true或false
call_count:被调用的次数
call_args:获取最近调用时的所有参数
call_args_list:获取最近调用时的所有参数列表
method_calls:当前mock对象调用了哪些方法
'''
import unittest
from unittest import mock
from mockmode.pyment import Pyment
class TestMock(unittest.TestCase):
    def setUp(self):
        self.pyment=Pyment()
    def test_success(self):
        # 模拟pyment的RequestInter返回值为200
        self.pyment.RequestInter=mock.Mock(return_value=200)#mock模拟一个方法，这个方法的名字是RequestInter
        res=self.pyment.DoPay('000000',2000)
        self.assertEqual('success',res,'支付操作成功')
        self.pyment.RequestInter.assert_called_once_with('000000',2000) #传入正确参数且调用一次
    def test_fail(self):
        self.pyment.RequestInter=mock.Mock(return_value=500)#模拟pyment的RequestInter返回值为500
        res=self.pyment.DoPay('000000',5000)
        self.assertEqual('fail',res,'支付操作失败')
    def test_timeout_success(self):
        self.pyment.RequestInter=mock.Mock(side_effect=(TimeoutError,200))#模拟pyment的RequestInter返回超时
        res=self.pyment.DoPay('000000',7000)
        self.assertEqual('success',res,'支付操作成功')
        a=self.pyment.RequestInter.method_calls
        print(a)
    def test_timeout_fail(self):
        self.pyment.RequestInter=mock.Mock(side_effect=(TimeoutError,500))#模拟pyment的RequestInter返回值为200
        res=self.pyment.DoPay('000000',9000)
        self.assertEqual('fail',res,'支付操作失败')
    def tearDown(self):
        pass