import pymysql


class MysqlUtil:

    user = 'root'
    pwd = 'HNIEACMore'
    localhost = '10.0.38.112'

    def __init__(self):
        try:
            #  打开数据库连接
            self.connect = pymysql.connect(host=self.localhost, user=self.user,
                                           password=self.pwd, database='daka', charset='utf8')
            #  获取游标
            self.cursor = self.connect.cursor()
        except Exception as e:
            print(e)

    def queryAllUserEmail(self):
        sql = "SELECT `users`.email FROM `users` WHERE `status`=1 AND `users`.email != '' AND `users`.user_id NOT IN (SELECT result.user_id FROM result WHERE TO_DAYS(result.time) = TO_DAYS(now()) AND STRCMP(SUBSTRING(result.result, 33, 4),'True')=0)"
        users = []
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for row in result:
                email = row[0]
                users.append({
                    'email': email
                })
        except Exception as e:
            print(e)
            return None
        return users

    def closeMysql(self):
        try:
            #  关闭数据库连接
            self.connect.close()
        except Exception as e:
            print(e)
            return False
        return True
