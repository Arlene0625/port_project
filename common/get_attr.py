# -*- coding: utf-8 -*-
# Author : monster
#反射
class Attr:
    mobilephone=22
    pwd=None
    def __init__(self,a,b):
        self.a=a
        self.b=b

if __name__ == '__main__':
    get_phone=getattr(Attr,'mobilephone') #获取变量
    print(get_phone)
    set_phone=setattr(Attr,'mobilephone',13800000000) #增加/设置变量 的值
    set_phone2=getattr(Attr,'mobilephone')
    print(set_phone2)
    if hasattr(Attr,'mobilephone'): #判断是否存在
        del_phone=delattr(Attr,'mobilephone') #删除变量
        print(del_phone)


    attr=Attr(5,0)
    phone=getattr(attr,'a') #实例后调用
    print(phone)