# -*- coding: utf-8 -*-
# Author : monster
import os

# base_path=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
base_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #abspath获取当前绝对路径，dirname获取当前目录
test_dir=base_path+'/test'
# print(base_path)
excel_path=base_path+'/test_cases/testdatas_monster_20181214.xlsx'
report_path=base_path+'/test_reports/forward_test_api.html'
logs_path=os.path.join(base_path,'my_logger')
conf_path=os.path.join(base_path,'conf')
# print(logs_path)