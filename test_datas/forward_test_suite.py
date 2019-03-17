# -*- coding: utf-8 -*-
# Author : monster
'''1，设计一个run_test 模块完成收集用例--执行用例--回写测试结果
2，封装配置文件读取类，根据环境设计配置文件，实现多套环境灵活切换
3，复习unittest,ddt'''
import HTMLTestRunnerNew
import unittest

from Interface_Project_201812.common import File_Path

#第一种方法：单个执行测试模块
# suite1=unittest.TestSuite()
# loader=unittest.TestLoader()
# suite1.addTest(loader.loadTestsFromTestCase(Test_Forward_loan_request))

#第二种方法：discover模糊匹配查找所有test开头的接口用例
discover=unittest.defaultTestLoader.discover(File_Path.test_dir,pattern="test*.py",top_level_dir=None)#如果test存在common下面的子目录，就用top_level_dir
with open(File_Path.report_path,'wb+') as file:
    runner=HTMLTestRunnerNew.HTMLTestRunner(file,verbosity=2,title='前程贷项目的接口请求测试报告',
                                            description='接口请求的第一部分：注册')
    runner.run(discover)

