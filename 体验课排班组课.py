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
GroupClassAndLessonBean {
beginTime (string, optional): 课节开始时间 2010-10-10 23:00:00 ,
date (string, optional): 上课日期 2018-03-09 ,
dayBucket (string, optional): 天周期（如 周一/周三）,体验课可为空字符串 = ['D_1_4', 'D_2_5', 'D_3_6'],
endTime (string, optional): 课节结束时间 ,
headMaster (integer, optional): 班主任 ,
lessonId (integer, optional): lessonID ,
teacherId (integer, optional): 外教ID ,
timeBucket (string, optional): 时间段(如 7：00--8：00) = ['T_18_18', 'T_18_19', 'T_19_20', 'T_20_21']
}'''


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



#创建体验课班级
# http://t5-api.pipifish.com/op-api/classin/createdGroupClass

def Created_groupclass(url,headMaster,teacherId,token):
    try:
        # 获取当前时间
        time = datetime.now()

        t1 = time + timedelta(minutes=5)
        beginTime = t1.strftime("%Y-%m-%d %H:%M:%S")

        date = datetime.now().strftime("%Y-%m-%d")

        t3 = time + timedelta(minutes=10)
        endTime = t3.strftime("%Y-%m-%d %H:%M:%S")

        #创建体验课班级
        groupclass_url = url + '/op-api/classin/createdGroupClass'
        body = {
            "beginTime": beginTime,
            "date": date,
            "dayBucket": "D_1_4",
            "endTime": endTime,
            "headMaster": headMaster,
            "lessonId": 1,
            "teacherId": teacherId,
            "timeBucket": "T_18_18"
               }
        headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'token': token
                  }
        text = requests.post(groupclass_url,data=json.dumps(body),headers=headers).text
        # print(text)
        # data = re.findall(r'"data":"(.*)"，"msg"',text)[0]
        # print(data)

        # str 转换为dict
        jsonData = json.loads(text)
        data = jsonData['data']
        if jsonData["msg"] == "success":
            print('体验课班级创建成功！')
        return data
    except Exception as e:
        print('创建体验课班级失败！\n错误日志：%s'%e)



# 插班
# http://t5-api.pipifish.com/op-api/classin/groupClasAddStudent?groupClassId=812&mobile=10055555605
def AddStudent(url,data,token,mobile):
    try:
        classin_url = url + '/op-api/classin/groupClasAddStudent?groupClassId=%s&mobile=%s'%(data,mobile)
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/json;charset=UTF-8',
            'token': token
        }
        text = requests.post(classin_url,headers=headers).text
        # print(text)
        jsondata = json.loads(text)
        if jsondata["msg"]=='success':
            print('体验课班级学生插班成功!班级id:%s'%data)
    except Exception as e:
        print('体验课班级学生插班失败！\n错误日志：%s'%e)





if __name__ == '__main__':

    url = 'http://t5-api.pipifish.com'
    mobile = 10055555605
    headMaster = 2644
    # lessonId = 1
    teacherId = 508

    token = login(url)
    data = Created_groupclass(url,headMaster,teacherId,token)
    AddStudent(url,data,token,mobile)


