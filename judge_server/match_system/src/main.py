#! /usr/bin/env python

import glob
import json
import sys
import os
from os import path
sys.path.insert(0, glob.glob('../../')[0])

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from match_server.match_server import Match

from queue import Queue
from time import sleep
from threading import Thread
from dbUtil.MysqlUtil import MysqlUtil
from submitOtherOj.acwing.Acwing import Acwing
from submitOtherOj.acwing.AcwingLogin import AcwingLogin
from submitOtherOj.acwing.AcwingGetInfo import AcwingGetInfo
from submitOtherOj.csg.csgSubmit import csgSubmit
from submitOtherOj.csg.csgLogin import csgLogin
from submitOtherOj.csg.csgGetInfo import csgGetInfo
from submitOtherOj.codeforces.cflogin import cflogin
from submitOtherOj.codeforces.cfgetMessage import cfgetMessage
from submitOtherOj.codeforces.cfgetResult import cfgetResult
from submitOtherOj.codeforces.cfsubmit import cfsubmit


queue = Queue()  # 消息队列
ojs = {}
ojStatus = {}  # 每个oj可用的账号数


class Player:
    def __init__(self, sid, tid):
        db = MysqlUtil()
        self.sid = sid
        self.tid = tid
        self.lang = db.getLanguage(sid)
        self.code = db.getCode(sid)
        self.userid = db.getUser(sid)
        res = db.getSpj(tid)
        self.to_id = res['to_id']
        self.spj = res['source']
        self.cf_id = res['cf_id']
        self.langs = ["c", "cpp", '', 'java', '', '', "py"]
        self.language = self.langs[self.lang]
        db.closeMysql()

        if self.spj == "acwing":
            lang = ""
            if self.lang == 0:
                lang = "C"
            elif self.lang == 1:
                lang = "C++"
            elif self.lang == 3:
                lang = "Java"
            elif self.lang == 6:
                lang = "Python3"
            self.lang = lang
        elif self.spj == "codeforces":
            lang = ""
            if self.lang == 0:
                lang = "43"  # GNU GCC C11 5.1.0
            elif self.lang == 1:
                lang = "54"  # GNU G++17 7.3.0
            elif self.lang == 3:
                lang = "36"  # Java 1.8.0_241
            elif self.lang == 6:
                lang = "31"  # Python 3.8.10
            self.lang = lang

    def makeacfile(self):
        filepath = "/home/judge/data/" + str(self.tid) + "/ac/" + str(self.sid) + "." + self.language
        if not os.path.exists("/home/judge/data/" + str(self.tid)):
            cmd = "mkdir /home/judge/data/" + str(self.tid)
            os.system(cmd)
        if not os.path.exists("/home/judge/data/" + str(self.tid) + "/ac"):
            cmd = "mkdir /home/judge/data/" + str(self.tid) + "/ac"
            os.system(cmd)
        cmd = "touch " + filepath
        os.system(cmd)
        with open(filepath, 'w') as file_object:
            file_object.write(self.code)

    def getsim(self, selfsid):
        url = "/home/judge/data/" + str(self.tid) + "/ac/"
        filename = str(self.sid) + "." + self.language
        cmd = ""
        sim = 0
        sim_id = '0'
        if self.language == "py":
            return None
        if self.language == 'c':
            cmd = "sim_c -t 50 -p -o " + str(self.sid) + ".txt -T " + url + filename
        elif self.language == 'cpp':
            cmd = "sim_c++ -t 50 -p -o " + str(self.sid) + ".txt -T " + url + filename
        elif self.language == 'java':
            cmd = "sim_java -t 50 -p -o " + str(self.sid) + ".txt -T " + url + filename
        for file in os.listdir(url):
            if file == filename or int(file[:file.find('.')]) > int(self.sid) or int(file[:file.find('.')]) in selfsid:
                continue
            if (self.language == 'c' or self.language == 'cpp') and 'c' not in file:
                continue
            if self.language == 'java' and 'java' not in file:
                continue
            os.system(cmd + ' ' + path.join(url, file))
            with open(str(self.sid) + ".txt", 'r') as f:
                for line in f:
                    if '%' in line:
                        p = line.find('%')
                        s = int(line[p - 3:p - 1])
                        print(line)
                        if line[p - 4] == '1':
                            s = 100
                        sim = max(sim, s)
                        sim_id = file[:file.find('.')]
        if os.path.exists(str(self.sid) + ".txt"):
            cmd = "rm " + str(self.sid) + ".txt"
            os.system(cmd)
        return {'sim': sim, 'sim_id': sim_id}

    def sim(self):
        db1 = MysqlUtil()
        selfsid = db1.getselfsid(self.tid, self.userid)
        res = self.getsim(selfsid)
        print(res)
        if res is not None and res['sim_id'] != '0' and res['sim'] > 50:
            db1.addSim(self.sid, res['sim_id'], res['sim'])
        db1.closeMysql()

        self.makeacfile()


class Pool:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def check_match(self, player):
        if ojStatus[player.spj] >= 1:  # 检查当前是否有空闲账号
            return True
        else:
            return False

    def match(self):
        while len(self.players) >= 1:
            for i in range(len(self.players)):
                if self.check_match(self.players[i]):
                    ojs[self.players[i].spj] = sorted(ojs[self.players[i].spj], key=lambda p: p['submitNum'])
                    ojStatus[self.players[i].spj] -= 1
                    Thread(target=submit, args=(self.players[i],), daemon=True).start()
                    ojStatus[self.players[i].spj] += 1
                    self.players = self.players[:i] + self.players[i + 1:]
                    break

    def increase_waiting_time(self):
        for player in self.players:
            player.waiting_time += 1


def get_player_from_queue():  # 返回空表示队列里没有元素
    try:
        return queue.get_nowait()
    except:
        return None


def worker():
    pool = Pool()
    while True:
        player = get_player_from_queue()
        if player is not None:
            pool.add_player(player)
        else:
            pool.match()
            sleep(1)


def submit(player):
    if player.spj == "acwing":
        for oj in ojs['acwing']:
            if oj['status'] == 0:
                oj['status'] = 1
                db = MysqlUtil()
                res = 6
                resq = None
                flag = False
                for i in range(10):
                    db.updateSolutionResult(player.sid, 21)
                    resq = Acwing(player.code, player.lang, player.to_id, oj['cookie']).run()
                    res = resq['status']
                    if res is not None:
                        break
                    oj['cookie'] = AcwingLogin(oj['username'], oj['password'])
                    db.updateOJCookie(oj['id'], oj['cookie'])
                    if i >= 9:
                        flag = True
                if flag:
                    oj['status'] = 1
                    continue

                oj['submitNum'] += 1
                if res == "ACCEPTED":
                    result = 4
                elif res == "TIME_LIMIT_EXCEEDED":
                    result = 7
                elif res == "COMPILE_ERROR":
                    result = 11
                elif res == "PRESENTATION_ERROR":
                    result = 5
                elif res == "MEMORY_LIMIT_EXCEEDED":
                    result = 8
                elif res == "FLOAT_POINT_EXCEPTION":
                    result = 10
                elif res == "RUNTIME_ERROR":
                    result = 10
                elif res == "SEGMENTATION_FAULT":
                    result = 10
                elif res == "OUTPUT_LIMIT_EXCEEDED":
                    result = 9
                else:
                    result = 6

                if result != 11:
                    flag = False
                    info = None
                    for i in range(0, 10):
                        try:
                            info = AcwingGetInfo(player.to_id, oj['cookie'])
                            flag = info['result']
                        except Exception as e:
                            pass
                        if flag is True:
                            db.updateSolution(id=player.sid, pass_rate=info['rate'], time=info['time'],
                                              space=info['space'])
                            break
                        sleep(1)
                db.updateSolutionResult(player.sid, str(result))
                db.addInfo(player.sid, resq['info'])
                db.updateSolutionJudge(player.sid, "acwing" + str(oj['id']))
                if result == 4:
                    db.updateProblemAC(player.tid)
                    Thread(target=player.sim, daemon=True).start()
                db.updateProblem(player.tid)
                db.updateUserSolution(player.userid)
                db.updateUserSubmit(player.userid)
                db.closeMysql()
                oj['status'] = 0
                break
    elif player.spj == "csg":
        for oj in ojs['csg']:
            if oj['status'] == 0:
                oj['status'] = 1
                db = MysqlUtil()
                res = 0
                flag = False
                for i in range(10):
                    db.updateSolutionResult(player.sid, 21)
                    res = csgSubmit(player.to_id, player.code, player.lang, oj['cookie'])
                    if res is not None:
                        break
                    csgLogin(oj['username'], oj['password'], oj['cookie'])
                    db.updateOJCookie(oj['id'], oj['cookie'])
                    if i >= 9:
                        flag = True
                if flag:
                    oj['status'] = 1
                    continue
                oj['submitNum'] += 1

                result = 0
                info = None
                while result < 4:
                    flag = False
                    for i in range(0, 10):
                        try:
                            info = csgGetInfo(res, oj['cookie'])
                            result = info['result']
                            flag = info['res']
                        except Exception as e:
                            pass
                        if flag is True:
                            break
                        sleep(1)
                print(player.userid)

                db.updateSolution(id=player.sid, pass_rate=info['rate'], time=info['time'], space=info['memory'])
                db.updateSolutionResult(player.sid, info['result'])
                if result == 4:
                    db.updateProblemAC(player.tid)
                    Thread(target=player.sim, daemon=True).start()
                db.updateSolutionJudge(player.sid, "CSG" + str(oj['id']))
                db.updateProblem(player.tid)
                db.updateUserSolution(player.userid)
                db.updateUserSubmit(player.userid)
                db.closeMysql()
                oj['status'] = 0
                break
    elif player.spj == "codeforces":
        for oj in ojs['codeforces']:
            if oj['status'] == 0:
                oj['status'] = 1
                db = MysqlUtil()
                res = 0
                flag = False
                submissionId = ""
                for i in range(10):
                    db.updateSolutionResult(player.sid, 21)
                    res = cfsubmit(player.to_id, player.cf_id, player.lang, player.code, oj['cookie'], oj['username'])
                    if res['result'] == "true":
                        submissionId = res['submissionId']
                        break
                    print(res['msg'])
                    if res['msg'] == 'You have submitted exactly the same code before':
                        db.updateSolutionResult(player.sid, "22")
                        db.updateSolutionJudge(player.sid, "codeforces" + str(oj['id']))
                        db.updateProblem(player.tid)
                        db.updateUserSubmit(player.userid)
                        db.closeMysql()
                        oj['status'] = 0
                        oj['submitNum'] += 1
                        ojStatus[player.spj] += 1
                        return
                    if res['msg'] == 'unlogin':
                        resp = None
                        for i in range(10):
                            resp = cflogin(oj['username'], oj['password'], oj['id'])
                            if resp['result'] == 'true':
                                break
                        oj['cookie'] = resp
                        db.updateOJCookie(oj['id'], json.dumps(resp))
                        sleep(2)
                    if res['msg'] == "Source should satisfy regex [^{}]*public\s+(final)?\s*class\s+(\w+).*":
                        db.updateSolutionResult(player.sid, "11")
                        db.updateSolutionJudge(player.sid, "codeforces" + str(oj['id']))
                        db.updateProblem(player.tid)
                        db.updateUserSubmit(player.userid)
                        db.closeMysql()
                        oj['status'] = 0
                        oj['submitNum'] += 1
                        ojStatus[player.spj] += 1
                        return
                    sleep(3)
                    if i >= 9:
                        flag = True
                if flag:
                    oj['status'] = 1
                    continue
                oj['submitNum'] += 1

                flag = False
                resp = None
                for i in range(0, 10):
                    try:
                        resp = cfgetResult(submissionId, oj['cookie'])
                        flag = resp['result']
                    except Exception as e:
                        pass
                    if flag == 'true':
                        break
                    sleep(3)
                verdict = resp['verdict']
                info = resp['info']

                result = 6
                if "Accepted" in verdict:
                    result = 4
                elif "Time limit exceeded" in verdict:
                    result = 7
                elif "Compilation error" in verdict:
                    result = 11
                elif "Presentation error" in verdict:
                    result = 5
                elif "Memory limit exceeded" in verdict:
                    result = 8
                elif "Runtime error" in verdict:
                    result = 10
                elif "Wrong answer" in verdict:
                    result = 6
                # elif res == "SEGMENTATION_FAULT":
                #     result = 10
                # elif res == "OUTPUT_LIMIT_EXCEEDED":
                #     result = 9
                db.updateSolutionResult(player.sid, str(result))
                db.addInfo(player.sid, info)
                db.updateSolutionJudge(player.sid, "codeforces" + str(oj['id']))
                if result == 4:
                    db.updateProblemAC(player.tid)
                    Thread(target=player.sim, daemon=True).start()
                db.updateProblem(player.tid)
                db.updateUserSolution(player.userid)
                db.updateUserSubmit(player.userid)

                flag = False
                info = None
                for i in range(0, 10):
                    try:
                        info = cfgetMessage(submissionId, oj['cookie'])
                        flag = info['result']
                    except Exception as e:
                        print(e)
                        pass
                    if flag == "true":
                        break
                    sleep(1)
                db.updateCFSolution(id=player.sid, time=info['time'], space=info['space'])
                db.closeMysql()
                oj['status'] = 0
                break


class MatchHandler:
    def add_player(self, sid, tid):
        player = Player(sid, tid)
        queue.put(player)
        return 0


if __name__ == '__main__':
    handler = MatchHandler()
    processor = Match.Processor(handler)
    transport = TSocket.TServerSocket(host='0.0.0.0', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # You could do one of these for a multithreaded server
    server = TServer.TThreadedServer(
        processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    # 初始化oj状态数组
    db = MysqlUtil()
    ojs = db.getOjUser()
    db.closeMysql()
    for oj in ojs:
        ojStatus[oj] = len(ojs[oj])

    Thread(target=worker, daemon=True).start()  # daemon=True 杀掉主线程该进程也会被杀掉

    print('Starting the server...')
    server.serve()
    print('done.')
