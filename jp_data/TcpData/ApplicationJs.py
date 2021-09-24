# -*- coding: utf-8 -*-
import datetime
import json
import time
import traceback
from tkinter import *
import urllib
#提交时的响应事件
from tkinter.ttk import Combobox
from urllib.parse import urlparse
import tkinter

import requests

from TcpData.MyPyMysql import MyPyMysql
from TcpData.StunumInfo import StunumInfo
from Tools.TimeTools import get_time_delta, strTimeToDatetime, datetime_2string, generate_timestamp, getPreMintime, \
    string_2datetime, strA_2strB

#日志照片编号

photos = []

#事件
def btn_setSQL(e):
    ip = e_ip.get()
    port = int(e_port.get())
    username = e_name.get()
    password = e_pwd.get()
    db = e_sql.get()
    #插入数据的条数
    try:
        st = MyPyMysql(ip, port, username, password, db,get_stunum())  # 实例化类，传入必要参数
        # st = MyPyMysql('192.168.1.186', 3306, 'root', '123456', 'jp_test',get_stunum())  # 实例化类，传入必要参数
        #插入数据的条数
        result = st.counts
        global photos
        photos = st.imgs
    except Exception as e:
        #将结果输出(更新)到文本域
        text_result.delete(0.0, END)
        text_result.insert(1.0, traceback.format_exc())
    else:
        #将结果输出(更新)到文本域
        text_result.delete(0.0, END)
        text_result.insert(1.0, result)
        text_result.insert(2.0, photos)

#日志请求
def btn_submitOp(e):

    #拼接url
    url = get_postUrl("classrecord")


    #拼接json
    stu = get_stunum()
    stu = stu.__dict__
    stu ["recnum"] =  str(e_recnum.get())
    stu ["duration"] = e_duration.get()
    del stu['time']
    re_data = {"mileage": 80,
               "total": 10,
               "part1": 1,
               "part2": 2,
               "part3": 3,
               "part4": 4,
               "platformvalidtime": 100
               }
    stu.update(re_data)
    if stu["subjcode"][0] == 2 or stu["subjcode"][0] == 4:
        del stu['carnum']
        del stu['simunum']
    if stu["subjcode"][0] == 3:
        del stu['carnum']
    if len(photos) == 0:
        btn_setSQL(e)
    if len(photos) == 1:
        stu["photo1"] = stu["photo3"] = stu["photo2"] = str(photos[0])
    if len(photos) != 1 and len(photos) != 0:
        stu["photo1"] = stu["simunum"]+str(photos[0])
        stu["photo3"] = stu["simunum"]+str(photos[-1])
        stu["photo2"] = stu["simunum"]+str(photos[1])
    data=json.dumps(stu,ensure_ascii=False,indent=2)
    send_post(url,data)

#阶段请求
def btn_submitTra(e):

    #拼接url
    url = get_postUrl("stagetrainningtime")
    tra_record_list = {}
    inscode = entry_inscode.get()
    subject = cvJ.get()
    stunum = entry_stunum.get()

    tra_record_list["inscode"] = str(inscode)
    tra_record_list["subject"] = str(subject)
    tra_record_list["stunum"] = str(stunum)
    re_data = {"duration": 201,
               "examresult": "70",
               "mileage": 80,
               "pdfid": 9,
               "esignature":"esignature",
               "totaltime": 200,
               "vehicletime": 40,
               "classtime": 30,
               "simulatortime": 20,
               "networktime": 10,
               "rectype": 4,
               "commitFlag": "2",
               "recarray": [{
                   "rnum": "123456789012345600005"
               }]
               }
    tra_record_list.update(re_data)
    data=json.dumps(tra_record_list,ensure_ascii=False,indent=2)
    send_post(url,data)

#结业请求
def btn_submitGra(e):
    graduation_list = {}
    #拼接url
    url = get_postUrl("graduation")
    autinscode = entry_inscode.get()
    stunum = entry_stunum.get()
    graduation_list["gracertnum"] = str(stunum)
    graduation_list["stunum"] = str(stunum)
    graduation_list["autinscode"] = str(autinscode)
    re_data = {"grantdate":"20200110","pdfid":3,"esignature":"esignature"}
    graduation_list.update(re_data)
    data=json.dumps(graduation_list,ensure_ascii=False,indent=2)
    send_post(url,data)

def get_stunum():
    inscode = entry_inscode.get()
    stunum = entry_stunum.get()
    starttime = e_startDay.get()
    endtime = e_endDay.get()
    coachnum = entry_coachnum.get()
    carnum = entry_carnum.get()
    simunum = entry_devnum.get()
    subjcode = cv.get()
    time = e_time.get()
    latitude = e_lat.get()
    longitude = e_longitude.get()
    platnum = e_platnum.get()
    is_theory_image = 0
    #非实车是否有分钟学时及过程照片，buss_theory_image，
    if cv_devlevel.get() == "非实车有":
        is_theory_image = 1
    return  StunumInfo(inscode,stunum,starttime,endtime,coachnum,carnum,simunum,subjcode,time,latitude,longitude,platnum,is_theory_image)

#拼接url
def get_postUrl(part):
    url = "?v=1.0.0.e1&ts=1477034912021&sign=6117D6F0C2A2237AE80FB0A8BA090D3CB39BDB81C10587FD443E9F1C818D0ACF7B85EA24D935D005081D4F1F10E4B7D3F1ED49F827E743F69ADE9A6F582C910AC577D81C1176AF318A0AFAF2C858095AF675D6D5836D7D0A881DC5A45C8367D70D9DB38C18BD6CA81E99B469EB40CA91D5A4AF9BB257590FCAFF643F58E95A8BD5C1EACD497D28E0CEC45E195B5BC15B1F30E553C206FC30C732F904BBF7B8F56BF31DA429E85595E90182B8B8AC072DE0A9ABCE4B6DB174D0FC7AF6CA631CF968983A89C565E626FD5F653B0E491CA11439422BA82C5020FD21381F9334E74FE1B2C867476BBEC0E32C03D31CE488EA28D484DE1DC608E6EDBA11C856A861BA&user="
    e_dzurl_data = str(e_dzurl.get())+ part
    e_user_data = str(e_user.get())
    return e_dzurl_data + url + e_user_data

#发送post请求
def send_post(url,data):
    headers = {'content-type': 'application/json'}
    try:
        r = requests.post(url=url.encode("utf-8"),data=data,timeout=60,headers = headers)
        r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    except requests.RequestException as e:
        text_result.delete(0.0, END)
        text_result.insert(1.0, e)
    else:
        #将结果输出(更新)到文本域
        result =r.text +"\n" + url + "\n"+data+"\n"
        text_result.delete(0.0, END)
        text_result.insert(1.0, result)
#####创建窗口#####
win = Tk()
win.title("通用请求")
win.geometry('800x500')

#####创建控件#####
#第一行 inscode
lbl_inscode = Label(win, text="inscode：")
lbl_stunum = Label(win, text="stunum：")
lbl_coachnum = Label(win, text="coachnum：")
lbl_carnum = Label(win, text="carnum：")

entry_inscode = Entry(win, width=18)
entry_stunum = Entry(win, width=18)
entry_coachnum = Entry(win, width=18)
entry_carnum = Entry(win, width=18)

lbl_inscode.grid(row=0, column=0, sticky=W, pady=5, padx=5)
entry_inscode.grid(row=0, column=1, sticky=W)
lbl_stunum.grid(row=0, column=2, sticky=W, pady=5, padx=5)
entry_stunum.grid(row=0, column=3, sticky=W)
lbl_coachnum.grid(row=0, column=4, sticky=W, pady=5, padx=5)
entry_coachnum.grid(row=0, column=5, sticky=W)
lbl_carnum.grid(row=0, column=6, sticky=W, pady=5, padx=5)
entry_carnum.grid(row=0, column=7, sticky=W)


#第2行 日期控件

e_startDay = tkinter.Variable()
e_endDay = tkinter.Variable()
lbl_startDay = Label(win, text="starttime：")
lbl_endDay = Label(win, text="endtime：")
entry_startDay = Entry(win,textvariable=e_startDay, width=18)
entry_endDay = Entry(win,textvariable=e_endDay, width=18)
lbl_startDay.grid(row=1, column=0, sticky=W, pady=5, padx=5)
entry_startDay.grid(row=1, column=1, sticky=W)
lbl_endDay.grid(row=1, column=2, sticky=W, pady=5, padx=5)
entry_endDay.grid(row=1, column=3, sticky=W)
dt = datetime.datetime.now()
e_endDayT = datetime_2string(dt=dt,fmt='%Y%m%d%H%M%S')
e_startDayT = getPreMintime(dt,60)
e_startDay.set(strA_2strB(e_startDayT))
e_endDay.set(e_endDayT)

e_duration = tkinter.Variable()
lbl_duration = Label(win, text="duration：")
entry_duration = Entry(win,textvariable=e_duration,width=18)
lbl_duration.grid(row=1, column=4, sticky=W, pady=5, padx=5)
entry_duration.grid(row=1, column=5, sticky=W)
e_duration.set("60")

lbl_devnum = Label(win, text="simunum：")
entry_devnum = Entry(win, width=18)
lbl_devnum.grid(row=1, column=6, sticky=W, pady=5, padx=5)
entry_devnum.grid(row=1, column=7, sticky=W)


#第3行 下拉选择框
lbl_subjcode = Label(win, text="subjcode：")
# 绑定变量
cv = tkinter.StringVar()

com = Combobox(win, textvariable=cv)
# 设置下拉数据
com["value"] = ("2211360000","4211360000","3212360000","1212360000","3213360000","1213360000","2214360000","4214360000")

# 设置默认值
com.current(0)
# 绑定事件
def func(event):
    # print(com.get())
    print(cv.get())
com.bind("<<ComboboxSelected>>", func)
lbl_subjcode.grid(row=2, column=0, sticky=W, pady=5, padx=5)
com.grid(row=2, column=1, sticky=W)
#图片间隔时间
e_time = tkinter.Variable()
lbl_time = Label(win, text="照片间隔：")
entry_time = Entry(win,textvariable=e_time, width=18)
lbl_time.grid(row=2, column=2, sticky=W, pady=5, padx=5)
entry_time.grid(row=2, column=3, sticky=W)
e_time.set("15")

#纬度
e_lat = tkinter.Variable()
lbl_lat = Label(win, text="lat：")
entry_lat = Entry(win,textvariable=e_lat, width=18)
lbl_lat.grid(row=2, column=4, sticky=W, pady=5, padx=5)
entry_lat.grid(row=2, column=5, sticky=W)
e_lat.set("28.264879")

#经度
e_longitude = tkinter.Variable()
lbl_longitude = Label(win, text="longitude：")
entry_longitude = Entry(win,textvariable=e_longitude, width=18)
lbl_longitude.grid(row=2, column=6, sticky=W, pady=5, padx=5)
entry_longitude.grid(row=2, column=7, sticky=W)
e_longitude.set("117.170653")


#第4行 user
lbl_user = Label(win, text="user：")
lbl_user.grid(row=3, column=0, sticky=W, pady=5, padx=5)
# 绑定变量
e_user = tkinter.Variable()
entry_user = Entry(win, textvariable=e_user,width=18)
entry_user.grid(row=3, column=1, sticky=W)
e_user.set("1598BAE7757")

#第4行 platnum
lbl_platnum = Label(win, text="platnum：")
lbl_platnum.grid(row=3, column=2, sticky=W, pady=5, padx=5)
# 绑定变量
e_platnum = tkinter.Variable()
entry_platnum = Entry(win, textvariable=e_platnum,width=18)
entry_platnum.grid(row=3, column=3, sticky=W)
e_platnum.set("A0002")

#第四行 DBip
lbl_ip= Label(win, text="DBip：")
lbl_ip.grid(row=3, column=4, sticky=W, pady=5, padx=5)
# 绑定变量
e_ip = tkinter.Variable()
entry_ip = Entry(win, textvariable=e_ip,width=18)
entry_ip.grid(row=3, column=5, sticky=W)
e_ip.set("47.92.75.224")

#第4行 port
lbl_port = Label(win, text="DBport：")
lbl_port.grid(row=3, column=6, sticky=W, pady=5, padx=5)
# 绑定变量
e_port = tkinter.Variable()
entry_port = Entry(win, textvariable=e_port,width=18)
entry_port.grid(row=3, column=7, sticky=W)
e_port.set("3306")

#第5行 数据库
lbl_para = Label(win, text="数据库：")
lbl_para.grid(row=4, column=0, sticky=W, pady=5, padx=5)
# 绑定变量
e_sql = tkinter.Variable()
entry_para = Entry(win, textvariable=e_sql,width=18)
entry_para.grid(row=4, column=1, sticky=W)
e_sql.set("jp_neimengnew2_test")

#第四行 用户名
lbl_name = Label(win, text="用户名：")
lbl_name.grid(row=4, column=2, sticky=W, pady=5, padx=5)
# 绑定变量
e_name = tkinter.Variable()
entry_name = Entry(win, textvariable=e_name,width=18)
entry_name.grid(row=4, column=3, sticky=W)
e_name.set("root")

#第四行 密码
lbl_pwd = Label(win, text="密码：")
lbl_pwd.grid(row=4, column=4, sticky=W, pady=5, padx=5)
# 绑定变量
e_pwd = tkinter.Variable()
entry_pwd = Entry(win, textvariable=e_pwd,width=18)
entry_pwd.grid(row=4, column=5, sticky=W)
e_pwd.set("Data#Gjxx2021")


#阶段选择
cv_devlevel = tkinter.StringVar()
devlevel = Combobox(win, textvariable=cv_devlevel,width = 5)
# 设置下拉数据
devlevel["value"] = ("非实车无","非实车有")
# 设置默认值
devlevel.current(0)
# 绑定事件
def funcDevlevel(event):
    print(cv_devlevel.get())
devlevel.bind("<<ComboboxSelected>>", funcDevlevel)
devlevel.grid(row=4, column=6, sticky=W)


#第6行 构造过程图片，分钟学时
btn_sql = Button(win, text="构造数据",bg = "PaleGreen")
btn_sql.bind('<Button-1>', btn_setSQL)
btn_sql.grid(row=4, column=7, sticky=W, padx=5,pady=5)




#第6行 地址
e_dzurl = tkinter.Variable()
lbl_dzurl = Label(win, text="请求：")
lbl_dzurl.grid(row=5, column=0, sticky=W, pady=5, padx=5)
entry_url = Entry(win, width=50,textvariable=e_dzurl)
entry_url.grid(row=5, column=1,columnspan=4, sticky=W)
e_dzurl.set("http://localhost/gjxx-interface-web/")

# 绑定变量
e_recnum = tkinter.Variable()
entry_recnum = Entry(win, textvariable=e_recnum,width=18)
entry_recnum.grid(row=5, column=5, sticky=W)
e_recnum.set(34001)

btn_rec_period = Button(win, text="日志请求",bg = "PaleGreen")
btn_rec_period.bind('<Button-1>', btn_submitOp,)
btn_rec_period.grid(row=5, column=7, sticky=W, padx=5,pady=5)


#阶段选择
cvJ = tkinter.StringVar()
comJ = Combobox(win, textvariable=cvJ,width = 5)
# 设置下拉数据
comJ["value"] = ("1","2","3","4")
# 设置默认值
comJ.current(0)
# 绑定事件
def funcJ(event):
    # print(com.get())
    print(cvJ.get())
comJ.bind("<<ComboboxSelected>>", funcJ)
comJ.grid(row=6, column=6, sticky=W)

btn_tra_record = Button(win, text="阶段请求",bg = "PaleGreen")
btn_tra_record.bind('<Button-1>', btn_submitTra)
btn_tra_record.grid(row=6, column=7, sticky=W, padx=5,pady=5)

btn_graduation = Button(win, text="结业请求",bg = "PaleGreen")
btn_graduation.bind('<Button-1>', btn_submitGra)
btn_graduation.grid(row=7, column=7, sticky=W, padx=5,pady=5)

#第6行 密码
lbl_recnum = Label(win, text="recnum：")
lbl_recnum.grid(row=5, column=4, sticky=W, pady=5, padx=5)


#第五行 返回结果
text_result = Text(win, width=100, height=25)
text_result.grid(row=6,rowspan=4, column=0, columnspan=6, sticky=W, padx=10)

# #第六行 其它
Label(win, text="-- by lele").grid(row=6, column=7, sticky=SE, padx=10, pady=10)

win.mainloop()

