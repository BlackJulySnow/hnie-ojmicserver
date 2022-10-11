import time
import pymysql
import json


class MysqlUtil:

    user = 'inputdata'
    pwd = 'inputdata'
    localhost = '172.31.0.96'
    # localhost = "10.0.38.112"
    # user = "root"
    # pwd = "acmore"

    def __init__(self):
        try:
            #  打开数据库连接
            self.connect = pymysql.connect(host=self.localhost, user=self.user,
                                           password=self.pwd, database='jol', charset='utf8')
            #  获取游标
            self.cursor = self.connect.cursor()
        except Exception as e:
            print(e)

    def getSpj(self, tid):
        sql = "SELECT to_id, source, cf_id FROM `spj` WHERE problem_id=%s"
        args = [tid]
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            row = result[0]
            to_id = row[0]
            source = row[1]
            cf_id = row[2]
        except Exception as e:
            print(e)
            return None
        return {'to_id': to_id, "source": source, "cf_id": cf_id}

    def getCode(self, sid):
        sql = "SELECT source FROM `source_code` WHERE solution_id=%s"
        args = [sid]
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            row = result[0]
            code = row[0]
        except Exception as e:
            print(e)
            return None
        return code

    def getLanguage(self, sid):
        sql = "SELECT `language` FROM `solution` WHERE solution_id=%s"
        args = [sid]
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            row = result[0]
            language = row[0]
        except Exception as e:
            print(e)
            return None
        return language

    def getOjUser(self):
        sql = "SELECT oj,id,username,cookie,password FROM `otheroj` ORDER BY id"
        ojs = {}
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for row in result:
                if row[0] not in ojs:
                    ojs[row[0]] = []
                ojuser = {'id': row[1], 'username': row[2], 'cookie': row[3], 'status': 0, "password": row[4], 'submitNum': 0}
                if row[0] == "codeforces":
                    ojuser['cookie'] = json.loads(ojuser['cookie'])
                ojs[row[0]].append(ojuser)
        except Exception as e:
            print(e)
            return None
        return ojs

    def getUser(self, sid):
        sql = "SELECT user_id FROM `solution` WHERE solution_id=%s"
        args = [sid]
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            row = result[0]
            userid = row[0]
        except Exception as e:
            print(e)
            return None
        return userid

    def getselfsid(self, tid, userid):
        sql = 'SELECT solution_id FROM `solution` WHERE problem_id=%s and user_id=%s and result=4'
        args = [tid, userid]
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            resq = []
            for row in result:
                resq.append(row[0])
        except Exception as e:
            print(e)
            return None
        return resq

    def addInfo(self, sid, info):
        sql = "SELECT COUNT(*) FROM `runtimeinfo` WHERE solution_id=%s"
        args = [sid]
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            count = result[0][0]
        except Exception as e:
            print(e)
            return None
        if count == 0:
            sql = "INSERT INTO `runtimeinfo`(`solution_id`,`error`) VALUES(%s,%s)"
            args = [sid, info]
            try:
                self.cursor.execute(sql, args)
                self.connect.commit()
            except Exception as e:
                print(e)
                return False
        else:
            sql = "UPDATE runtimeinfo set error=%s WHERE solution_id=%s"
            args = [info, sid]
            try:
                self.cursor.execute(sql, args)
                self.connect.commit()
            except Exception as e:
                print(e)
                return False
        return True

    def addSim(self, sid, sim_id, sim):
        sql = "SELECT COUNT(*) FROM `sim` WHERE s_id=%s"
        args = [sid]
        try:
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            count = result[0][0]
        except Exception as e:
            print(e)
            return None
        if count == 0:
            sql = "INSERT INTO `sim`(`s_id`,`sim_s_id`,`sim`) VALUES(%s,%s,%s)"
            args = [sid, sim_id, sim]
            try:
                self.cursor.execute(sql, args)
                self.connect.commit()
            except Exception as e:
                print(e)
                return False
        else:
            sql = "UPDATE sim set sim_s_id=%s, sim=%s WHERE s_id=%s"
            args = [sim_id, sim, sid]
            try:
                self.cursor.execute(sql, args)
                self.connect.commit()
            except Exception as e:
                print(e)
                return False
        return True

    def updateOJCookie(self, oid, cookie):
        sql = "UPDATE otheroj set cookie=%s, login_time=NOW() WHERE id=%s"
        args = [cookie, oid]
        try:
            self.cursor.execute(sql, args)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserSolution(self, userid):
        num_sql = "SELECT problem_id FROM `solution` WHERE user_id=%s AND result= 4 GROUP BY problem_id"
        pro_sql = "UPDATE users set solved=%s WHERE user_id=%s"
        args = [userid]
        try:
            self.cursor.execute(num_sql, args)
            result = self.cursor.fetchall()
            num = len(result)
            args1 = [num, userid]
            self.cursor.execute(pro_sql, args1)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateUserSubmit(self, userid):
        num_sql = "SELECT count(*) as num FROM `solution` WHERE `user_id`=%s and problem_id>0"
        pro_sql = "UPDATE users set submit=%s WHERE user_id=%s"
        args = [userid]
        try:
            self.cursor.execute(num_sql, args)
            result = self.cursor.fetchall()
            num = result[0][0]
            args1 = [num, userid]
            self.cursor.execute(pro_sql, args1)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateSolutionResult(self, sid, result):
        sql = "UPDATE solution set result=%s, judgetime=NOW() WHERE solution_id=%s"
        args = [result, sid]
        try:
            self.cursor.execute(sql, args)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateSolutionJudge(self, sid, judge):
        sql = "UPDATE solution set judger=%s WHERE solution_id=%s"
        args = [judge, sid]
        try:
            self.cursor.execute(sql, args)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateProblem(self, tid):
        num_sql = "SELECT COUNT(*) as num FROM `solution` WHERE problem_id=%s"
        pro_sql = "UPDATE problem set submit=%s WHERE problem_id=%s"
        args = [tid]
        try:
            self.cursor.execute(num_sql, args)
            result = self.cursor.fetchall()
            num = result[0][0]
            args1 = [num, tid]
            self.cursor.execute(pro_sql, args1)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateProblemAC(self, tid):
        num_sql = "SELECT COUNT(*) as num FROM `solution` WHERE problem_id=%s AND result=4"
        pro_sql = "UPDATE problem set accepted=%s WHERE problem_id=%s"
        args = [tid]
        try:
            self.cursor.execute(num_sql, args)
            result = self.cursor.fetchall()
            num = result[0][0]
            args1 = [num, tid]
            self.cursor.execute(pro_sql, args1)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateSolution(self, id, pass_rate, time, space):
        sql = "UPDATE solution set time=%s, memory=%s, pass_rate=%s WHERE solution_id=%s"
        args = [time, space, pass_rate, id]
        try:
            self.cursor.execute(sql, args)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def updateCFSolution(self, id, time, space):
        sql = "UPDATE solution set time=%s, memory=%s WHERE solution_id=%s"
        args = [time, space, id]
        try:
            self.cursor.execute(sql, args)
            self.connect.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def closeMysql(self):
        try:
            #  关闭数据库连接
            self.connect.close()
        except Exception as e:
            print(e)
            return False
        return True
