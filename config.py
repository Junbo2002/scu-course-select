# -*- coding: UTF-8 -*-
import datetime as date
import hashlib

select_captcha_url = "http://202.115.47.141/student/courseSelect/selectCourse/getYzmPic"
select_result_url = "http://202.115.47.141/student/courseSelect/selectResult/query"
redis_key_url = 'http://202.115.47.141/student/courseSelect/selectCourses/waitingfor'
login_token_url = 'http://202.115.47.141/login'  # 登录页面新加的token
captcha_url = "http://202.115.47.141//img/captcha.jpg"  # 验证码地址
index_url = "http://202.115.47.141//"  # 主页地址
login_url = "http://202.115.47.141//j_spring_security_check"  # 登录接口
course_select_url = "http://202.115.47.141//student/courseSelect/courseSelect/index"  # tokenValue界面
select_url = "http://202.115.47.141//student/courseSelect/selectCourse/checkInputCodeAndSubmit"  # 选课接口
courseList_url = "http://202.115.47.141//student/courseSelect/freeCourse/courseList"  # 选课剩余查询地址
already_select_course_url = "http://202.115.47.141//student/courseSelect/thisSemesterCurriculum/callback"  # 已选课程查询地址
queryTeacherJL_url = "http://202.115.47.141//student/courseSelect/queryTeacherJL"
selectcourse_xueqi = "2022-2023-1-1" # 学期
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': '202.115.47.141/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3782.0 Safari/537.36 Edg/76.0.152.0'
}

with open("config.txt", "r", encoding='utf-8') as f:
    info = f.readlines()
j_username = info[0].strip('\n')
o_password = info[1].strip('\n')
j_password = hashlib.md5(o_password.encode()).hexdigest()
fajhh = info[2].strip('\n')
courseNames = info[3].strip('\n').split(';')
# 课程号
courseNums = info[4].strip('\n').split(';')
# 课序号
coursekxhNums = info[5].strip('\n').split(';')


def secondAppend(time_str, s):
    cnt = time_str.count(':')
    if cnt == 1:  # %H:%M
        time_str += ":"+str(s)  # %H:%M:%S
    if cnt > 2:
        raise "时间格式为: %H:%M 或者 %H:%M:%S"
    return time_str


def check():
    if not (len(j_username) == 13 and j_username.isdigit()):
        raise RuntimeError("学号格式错误（学号为13位数字）")
    if not fajhh.isdigit():
        raise RuntimeError("方案计划号错误：为纯数字")


# 检查格式
# 起止时间
try:
    selectTime = info[6].strip('\n').split(' ')
    # print(selectTime)
    selectTime[0] = secondAppend(selectTime[0], 0)
    selectTime[1] = secondAppend(selectTime[1], 59)
    # print(selectTime)

except Exception:
    print("请检查config.txt中是否在第六行以“9:30 21:59”添加了起止时间，中间以空格分隔")

try:
    check()
except RuntimeError as e:
    print("config.txt格式错误：" + str(e))

