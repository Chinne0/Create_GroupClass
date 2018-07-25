#! /usr/bin/env python3
#-*-codig:utf-8-*-


import requests
import pymysql
import json
import re
import time
from datetime import datetime
from datetime import timedelta

'''
GroupClassBean {
dayBucket (string, optional): 天周期（如 周一/周三） = ['D_1_4', 'D_2_5', 'D_3_6'],
defaultTeacher (integer, optional): 班级课程默认外教老师Id ,
headMaster (integer, optional): 班主任 ,
studentBeans (Array[integer], optional): 学生ID ,
timeBucket (string, optional): 时间段(如 7：00--8：00) = ['T_18_18', 'T_18_19', 'T_19_20', 'T_20_21']
    }
'''


# 获取bms登录token
def login(url):
    try:
        t = time.time()
        url = url + '/auth-api/v1/api/auth/code/signIn?timer='+str(int(t))
        body = {"username": "123@qq.com",
                "password": "111111",
                "code":"111111"
                }
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=UTF-8'
                  }
        text = requests.post(url,data=json.dumps(body),headers=headers).text
        # token = str(re.findall(r'"data":"(.*)","msg"',text)[0])
        # print(token)
        jsonData = json.loads(text)
        token = jsonData["data"]
        return token
    except Exception as e:
        print('获取token失败！\n错误日志：%s'%e)


# 链接数据库，通过手机号获取手机id
def kid_id(url,mobile):
    try:
        if 't4-api' in url:
            localhost = 'rm-2zed82843eq9whk09po.mysql.rds.aliyuncs.com'

        if 't5-api' in url:
            localhost = 'rm-2zep2iea456s3k84b2o.mysql.rds.aliyuncs.com'

        if 't6-api' in url:
            localhost = 'rm-2ze95m74lhm365dunko.mysql.rds.aliyuncs.com'

        if 't7-api' in url:
            localhost = 'rm-2ze4488ji8b71td0cqo.mysql.rds.aliyuncs.com'

        if 't8-api' in url:
            localhost = 'rm-2zewd442n629w0m8l0o.mysql.rds.aliyuncs.com'

        if 't9-api' in url:
            localhost = 'rm-2zetx1rj7s8mh5j1veo.mysql.rds.aliyuncs.com'

        if 't10-api' in url:
            localhost = 'rm-2zez7h872bw152jz9uo.mysql.rds.aliyuncs.com'


        # 连接数据库
        connect = pymysql.connect(
            host=localhost,
            port=3306,
            user='wuhaotech',
            password='wuhaokeJI123',
            db='db_account',
            charset='utf8')
        # 获取游标

        cur = connect.cursor()

        # 查询数据

        sql = "select id from db_user.tb_kids_info where uid in(select uid from db_account.tb_phone_auth where mobile = '%s')"%mobile
        cur.execute(sql)
        # 获取所有数据
        db_results = cur.fetchall()
        kid_id = db_results[0][0]
        # print(kid_id)
        return kid_id
    except Exception as e:
        print('获取学生id失败!\n错误日志：%s'%e)



#创建常规课班级
# http://t5-api.pipifish.com/op-api/classin/group/class
def groupclass(url,token,defaultTeacher,headMaster,kid_id):
    try:

        groupclass_url = url + '/op-api/classin/group/class'
        body = {
            "dayBucket": "D_1_4",
            "defaultTeacher": defaultTeacher,
            "headMaster": headMaster,
            "studentBeans": [kid_id],
            "timeBucket": "T_18_18"
                  }
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=UTF-8',
            'token': token
                   }
        text = requests.post(groupclass_url,data=json.dumps(body),headers=headers).text
        # print(text)
        # data = str(re.findall(r'"data":"(.*)","msg"',text)[0])
        # print(data)

        # str转换为dict
        jsonData = json.loads(text)
        data = jsonData["data"]
        if jsonData["msg"]=="success":
            print('常规课班级创建成功！')
        return data
    except Exception as e:
        print('创建班级失败！错误日志：%s'%e)




#开课
# http://t5-api.pipifish.com/op-api/classin/open?groupClassId=2010
def open_classin(url,data,token):
    try:
        classin_url = url + '/op-api/classin/open?groupClassId=%s'%data
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=UTF-8',
            'token': token
                  }
        text = requests.post(classin_url,headers=headers).text
        # print(text)
        jsondata = json.loads(text)
        if jsondata["msg"]=="success":
            print('常规课班级开课成功！')
    except Exception as e:
        print(e)





#排常规课
def lession(url,data,lessonId,teacherId,token):
    try:
        #获取当前时间(日期格式)
        time = datetime.now()

        t1 = time + timedelta(minutes=5)
        beginTime = t1.strftime("%Y-%m-%d %H:%M:%S")
        #
        date = datetime.now().strftime("%Y-%m-%d")

        t3 = time + timedelta(minutes=10)
        endTime = t3.strftime("%Y-%m-%d %H:%M:%S")

        lession_url = url + '/op-api/classin/group/lessson'
        body = {
            "beginTime": beginTime,
            "date": date,
            "endTime": endTime,
            "groupClassId": data,
            "lessonId": lessonId,
            "teacherId": teacherId,
            "timeBucket": "T_18_18"
                }
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=UTF-8',
            'token': token
                  }
        text = requests.post(lession_url, data=json.dumps(body), headers=headers).text
        jsondata = json.loads(text)
        # print(jsondata["msg"])
        if jsondata["msg"]=='success':
            print('常规课班级排课成功！班级id:%s'%data)
    except Exception as e:
        print('常规课班级排课失败！\n错误日志%s'%e)





if __name__ == '__main__':

    url = 'http://t5-api.pipifish.com'
    # dict = {"mobile":10055555605,"defaultTeacher":508,"headMaster":2644,"lessonId":10,"teacherId":508}
    mobile = 10055555605
    defaultTeacher = 508
    headMaster = 2644
    lessonId = 10
    teacherId = 508

    token = login(url)
    kid_id = kid_id(url, mobile)
    data = groupclass(url,token,defaultTeacher,headMaster,kid_id)
    open_classin(url,data,token)
    lession(url,data,lessonId,teacherId,token)


