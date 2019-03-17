# encoding: utf-8 
import re
from Interface_Project_201812.common.Load_Conf import Load_Conf

class LoKey:
    con=Load_Conf()
    login_phone=con.load_conf('recharge', 'login_phone')
    login_pwd=con.load_conf('recharge', 'login_pwd')
    borrow_phone = con.load_conf('borrow', 'borrow_phone')
    borrow_pwd = con.load_conf('borrow', 'borrow_pwd')
    borrow_id = con.load_conf('borrow', 'borrow_id')

class Replace_Phone:
    @staticmethod
    def replace_phone(ph):
            p='\$\{(.*?)\}'
            while re.search(p,ph): #循环替换
                k = re.search(p, ph)#在请求参数中查找变量
                key = k.group(1)#取第一个分组里面的字符，传给下面的user
                data = getattr(LoKey, key)
                ph = re.sub(pattern=p, repl=data, string=ph, count=1)  #
            return ph #str类型

if __name__ == '__main__':
    ph ='{"mobilephone":"${borrow_phone}","pwd":"${borrow_pwd}"}'
    ph2 = '{"mobilephone":"${login_phone}","pwd":"${login_pwd}"}'
    ph3='{"memberId":"${borrow_id}","amount"="2000","title"="借钱租房","loanRate"="18","loanTerm"=6,"loanDateType"=4,"repaymemtWay"=11,"biddingDays"=2}'
    res=Replace_Phone.replace_phone(ph)
    res2= Replace_Phone.replace_phone(ph2)
    res3 = Replace_Phone.replace_phone(ph3)
    print(type(res),res)
    print(type(res2), res2)
    print(type(res3), res3)
