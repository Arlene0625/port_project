# encoding: utf-8
'''
1.连接数据库，创建游标，执行sql语句
2.查找最大手机号和用户的总金额
'''
import pymysql
from Interface_Project_201812.common.Load_Conf import Load_Conf

class MySql_Data:
    def __init__(self):
        conf=Load_Conf()
        host=conf.load_conf('mysql','host')
        user = conf.load_conf('mysql', 'user')
        password = conf.load_conf('mysql', 'password')
        port = conf.load_conf_int('mysql', 'port')
        try:
            self.my_sql=pymysql.connect(host=host, user=user, password=password,port=int(port))#cursorclass会返回字典形式  cursorclass=pymysql.cursors.DictCursor
            print('数据库连接成功！')
        except Exception as e:
            print('无法连接数据库，请检查！')
            raise e
    def get_mobilephone(self,sql1):
        cur=self.my_sql.cursor() #操作游标
        cur.execute(sql1)  #执行sql语句。    如果一次性要插入很多条数据的话，强烈推荐使用executemany
        return int(cur.fetchone()[0])+1
    def get_leaveamount(self,sql2):
        cur2=self.my_sql.cursor() #操作游标
        cur2.execute(sql2)  #执行sql语句。    如果一次性要插入很多条数据的话，强烈推荐使用executemany
        return cur2.fetchone() #接收一个返回结果
    def get_loan_title(self,sql3):
        cur3=self.my_sql.cursor() #操作游标
        cur3.execute(sql3)  #执行sql语句。    如果一次性要插入很多条数据的话，强烈推荐使用executemany
        return cur3.fetchone() #接收一个返回结果
    def close(self):
        self.my_sql.close()

if __name__ == '__main__':
    sql1='SELECT MobilePhone from future.member where MobilePhone !="" ORDER BY MobilePhone DESC LIMIT 1'
    sql2='SELECT LeaveAmount FROM future.member WHERE MobilePhone="18611223344"'
    sql3='SELECT Title FROM future.loan WHERE MemberID="1112648" ORDER BY CreateTime DESC LIMIT 1' #查询最新一条的loanid
    mysql_mobile=MySql_Data().get_mobilephone(sql1)#数据库返回的mysql_data为str类型
    mysql_amount = MySql_Data().get_leaveamount(sql2)
    mysql_title = MySql_Data().get_loan_title(sql3)
    print(type(mysql_amount),mysql_amount[0])
    print(type(mysql_mobile),mysql_mobile)
    # mysql_member_id=MySql_Data().get_loanid(sql3)
    print(type(mysql_title),mysql_title[0])