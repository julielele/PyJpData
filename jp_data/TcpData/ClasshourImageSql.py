from decimal import Decimal

from Tools.TimeTools import strTimeToDatetime, generate_timestamp, getPosMintime, datetime_2string, string_2datetime


class ClasshourImageSql:
    #非实车过程照片数据
    def getBussTheoryImageSql(stunum,file,count):
        '''
       :param stunum 学员对象
       :param file 学员头像:
       :param count 照片数量:
       :return:
       '''
        # 定义总插入行数为一个空列表
        data_list = []
        terpicno_list = []
        startTime = datetime_2string(strTimeToDatetime(stunum.starttime),fmt='%Y-%m-%d %H:%M:%S')
        postime = startTime
        endTime = datetime_2string(strTimeToDatetime(stunum.endtime),fmt='%Y-%m-%d %H:%M:%S')
        for i in range(0, count):
            reason = 1
            if i == 0:
                reason = 2
            if i == count -1:
                reason = 3;
                postime = endTime;
            long = len(str(i))
            if long == 1:
                terpicno = str(generate_timestamp())[5:]+"0"+str(i)
            else:
                terpicno = str(generate_timestamp())[long+3:]+str(i)
            uptime = postime;
            # 添加所有任务到总的任务列表
            result = (str(stunum.inscode), str(stunum.platnum), str(stunum.coachnum), str(stunum.stunum), terpicno, str(stunum.subjcode), file, postime, '2', "1", '2', stunum.latitude, stunum.longitude, postime, '222222', reason, '1', '654321', '111111', '1', '0.0000', str(stunum.simunum), '1')
            postime = getPosMintime(string_2datetime(postime),int(stunum.time))
            data_list.append(result)
            terpicno_list.append(terpicno)
        return data_list,terpicno_list

    #实车过程照片数据

    def getBussTcpImageSql(stunum,file,count):
        '''
        :param stunum 学员对象
        :param file 学员头像:
        :param count 照片数量:
        :return: 插入数据列表与图片记录编号
        '''
        # 定义总插入行数为一个空列表
        data_list = []
        tcpImage_list = []
        startTime = datetime_2string(strTimeToDatetime(stunum.starttime),fmt='%Y-%m-%d %H:%M:%S')
        postime = startTime
        endTime = datetime_2string(strTimeToDatetime(stunum.endtime),fmt='%Y-%m-%d %H:%M:%S')
        for i in range(0, count):
            reason = 19
            if i == 0:
                reason = 17
            if i == count -1:
                reason = 18;
                postime = endTime;
            long = len(str(i))
            if long == 1:
                terpicno = str(generate_timestamp())[5:]+"0"+str(i)
            else:
                terpicno = str(generate_timestamp())[long+3:]+str(i)
            uptime = postime;
            # 添加所有任务到总的任务列表
            result = ('A0002', str(stunum.stunum), terpicno, str(stunum.subjcode), file, uptime, '0', '0', stunum.latitude, stunum.longitude, '670', '0.0', '171', postime, '0.7500', '129', '0', '2',reason, '0', str(stunum.simunum),'1')
            postime = getPosMintime(string_2datetime(postime),int(stunum.time))
            data_list.append(result)
            tcpImage_list.append(terpicno)
        return data_list,tcpImage_list

    def getBussTcpClasshourSql(stunum,file,count):
        '''
        实车分钟学时
        :param stunum 学员对象
        :param file 学员头像:
        :param count 照片数量:
        :return: 插入数据列表
        '''
        # 定义总插入行数为一个空列表
        data_list = []
        startTime = datetime_2string(strTimeToDatetime(stunum.starttime),fmt='%Y-%m-%d %H:%M:%S')
        postime =  startTime
        endTime = datetime_2string(strTimeToDatetime(stunum.endtime),fmt='%Y-%m-%d %H:%M:%S')
        latitude = stunum.latitude
        longitude = stunum.longitude
        yrev = 740
        nrev = 740
        ymaxspeed = 79
        nmaxspeed = 79
        ytotalmileage = 1
        ntotalmileage = 1
        for i in range(0, count):
            recnum = str(generate_timestamp())+str(i)
            postime =  getPosMintime(string_2datetime(postime),1)
            uptime = postime;
            # 添加所有任务到总的任务列表
            result = (recnum, str(stunum.stunum), str(stunum.coachnum), '29512529', uptime, str(stunum.subjcode), '0', str(nmaxspeed), str(ntotalmileage), str(stunum.platnum), uptime, '2147483648', '3',latitude, longitude, '77.0', '78.0', '261',postime, postime, '0.7', str(nrev), '64929030644')
            nrev = ClasshourImageSql.getData(nrev,yrev);
            nmaxspeed = ClasshourImageSql.getData(nmaxspeed,ymaxspeed);
            ntotalmileage = ClasshourImageSql.getData(ntotalmileage,ytotalmileage);
            latitude = str('%3f'%(Decimal(latitude) + Decimal(0.00001)))
            longitude = str('%3f'%(Decimal(longitude) + Decimal(0.00001)))
            data_list.append(result)
        return data_list


    def getData(ndata,ydata):
        '''
        分钟学时中不能一样的数据
        :param ndata: 原值
        :param ydata: 新值
        :return:
        '''
        if ndata == ydata:
            ndata = ndata + 1
        else:
            ndata = ydata
        return ndata
