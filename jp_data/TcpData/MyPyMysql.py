#!/usr/bin/env python
import math
from traceback import format_exc

import pymysql
import gevent
import time

from TcpData.ClasshourImageSql import ClasshourImageSql
from Tools.TimeTools import get_time_delta


class MyPyMysql:
    def __init__(self, host, port, username, password, db, stunum, charset='utf8'):
        self.host = host          # mysql主机地址
        self.port = port          # mysql端口
        self.username = username  # mysql远程连接用户名
        self.password = password  # mysql远程连接密码
        self.db = db              # mysql使用的数据库名
        self.charset = charset
        self.stunum = stunum  # mysql使用的字符编码,默认为utf8
        self.pymysql_connect()    # __init__初始化之后，执行的函数


    def pymysql_connect(self):
        # pymysql连接mysql数据库
        # 需要的参数host,port,user,password,db,charset
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.username,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset
                                    )
        # 连接mysql后执行的函数
        self.asynchronous()
    #子线程执行
    def run(self, nmin, nmax):
        try:
            self._run()
        except Exception as e:
            self.exit_code = 1
            self.exception = e
            self.exc_traceback = format_exc()

    def _run(self):
        self.cur = self.conn.cursor()
        #执行的类容
        self.counts = ""
        #返回的照片编号
        self.imgs = []
        #获取学员头像
        fileSql = "SELECT photourl,photo FROM `buss_stu_info` WHERE stunum =" +self.stunum.stunum
        self.cur.execute(fileSql)
        rest = self.cur.fetchone()
        file = rest[0]

        #日期间的差值
        timeTwo = int(get_time_delta(self.stunum.starttime,self.stunum.endtime,"MINUTES"))
        #照片数量
        numTcps = math.ceil(timeTwo/int(self.stunum.time)) + 1

        if self.stunum.subjcode[0] == "1":
            #实车过程照片数据
            bussTcpImageSql = "INSERT INTO buss_tcp_image (platnum, stunum, terpicno, subjcode, filename, uptime, alarmflag, stateflag, lat, longitude, drivingspeed, positionspeed, direction, postime, score, upmode, camerach, size, reason, recognition, devnum, status) " \
                              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            (data_list,tcpImage_list) = ClasshourImageSql.getBussTcpImageSql(self.stunum,file,numTcps)
            # 执行多行插入，executemany(sql语句,数据(需一个元组类型))
            content1 = self.cur.executemany(bussTcpImageSql, data_list)
            if content1:
                self.imgs = tcpImage_list
                print('实车过程照片成功插入{}条数据'.format(content1))
                self.counts = self.counts + 'bussTcpImageSql成功插入{}条数据'.format(content1) + '\n'
            #插入分钟学时
            self.getTcpClasshour(file,timeTwo)
        elif self.stunum.is_theory_image == 1:
            #非实车过程照片数据
            bussTheoryImageSql = "INSERT INTO buss_theory_image (inscode, platnum, coachnum, stunum, terpicno, subjcode, filename, uptime, type, alarmflag, stateflag, lat, longitude, postime, recognition, reason, size, classid, camerach, upmode, score, devnum, status) " \
                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            (data_list,terpicno_list) = ClasshourImageSql.getBussTheoryImageSql(self.stunum,file,numTcps)
            # 执行多行插入，executemany(sql语句,数据(需一个元组类型))
            content = self.cur.executemany(bussTheoryImageSql, data_list)
            if content:
                self.imgs = terpicno_list
                print('非实车过程照片成功插入{}条数据'.format(content))
                self.counts = self.counts + 'bussTheoryImageSql成功插入{}条数据'.format(content)
            #插入分钟学时
            self.getTcpClasshour(file,timeTwo)
        else:
            self.imgs = [(rest[1])]
        self.conn.commit()

    def getTcpClasshour(self,file,timeTwo):
        '''
        实车过程分钟学时
        :param file: 学员头像url
        :param timeTwo: 分钟学时数量
        :return: 无
        '''

        bussTcpClasshourSql = "INSERT INTO buss_tcp_classhour (recnum, stunum, coachnum, classid, rectime, trainingcourse, recordflag, maxspeed, totalmileage, platnum, uptime, alarmflag, stateflag, lat, longitude, drivingspeed, positionspeed, direction, postime, createtime, mileage, rev, mobile) " \
                              "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        data_list2 = ClasshourImageSql.getBussTcpClasshourSql(self.stunum,file,int(timeTwo))
        # 执行多行插入，executemany(sql语句,数据(需一个元组类型))
        content2 = self.cur.executemany(bussTcpClasshourSql, data_list2)
        if content2:
            print('实车分钟学时成功插入{}条数据'.format(content2))
            self.counts = self.counts + 'bussTcpClasshourSql成功插入{}条数据'.format(content2)
    def asynchronous(self):
        self.exit_code = 0
        # g_l 任务列表
        # 定义了异步的函数: 这里用到了一个gevent.spawn方法
        #日期间的差值
        timeTwo = int(get_time_delta(self.stunum.starttime,self.stunum.endtime,"MINUTES"))
        #照片数量
        numTcps = math.ceil(timeTwo/int(self.stunum.time)) + 1
        max_line = numTcps
         # 定义每次最大插入行数(max_line=10000,即一次插入10000行)
        g_l = [gevent.spawn(self.run, i, i+max_line) for i in range(1, numTcps, max_line)]

        # gevent.joinall 等待所以操作都执行完毕
        gevent.joinall(g_l)
        self.cur.close()  # 关闭游标
        self.conn.close()  # 关闭pymysql连接
        if self.exit_code != 0:
            raise self.exception


if __name__ == '__main__':
    start_time = time.time()  # 计算程序开始时间
    # st = MyPyMysql('192.168.1.186', 3306, 'root', '123456', 'db20')  # 实例化类，传入必要参数
    # st = MyPyMysql('192.168.1.186', 3306, 'root', '123456', 'jp_test')  # 实例化类，传入必要参数
    print('程序耗时{:.2f}'.format(time.time() - start_time))  # 计算程序总耗时
