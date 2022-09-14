import requests
from requests.cookies import cookiejar_from_dict
import json

grades = [2019, 2020, 2021, 2022]

pageSize = 400
fajhh_url = 'http://202.115.47.141/student/comprehensiveQuery/search/trainProgram/load'
f = open("scheme.csv", "w", encoding='utf-8')

scheme_title = '年级,院系名称,院系号,专业名称,修读类型,方案名称,方案计划号,课程总门数,课程总学分,要求总学分,课程总学时,学制类型,学科目录,主要课程\n'

data = {
    "famc": "",
    "jhmc": "",
    "nj": "",
    "xw": "",
    "xzlx": "",
    "xdlx": "",
    "xsh": "",
    "pageNum": 1,
    "pageSize": pageSize
}


def get_fajhh(grade, session):
    print(f"正在爬取{grade}级数据")
    data["nj"] = grade
    scheme_info = session.post(url=fajhh_url, data=data).text
    scheme_info = json.loads(scheme_info)['data']['records']
    info = []
    for each_scheme_info in scheme_info:
        info.clear()
        # 单个培养方案数据
        info.append(each_scheme_info['NJ'])
        info.append(each_scheme_info['XSM'])
        info.append(each_scheme_info['XSH'])
        info.append(each_scheme_info['ZYM'])
        info.append(each_scheme_info['XDLXMC'])
        info.append(each_scheme_info['FAMC'])
        info.append(each_scheme_info['FAJHH'])
        info.append(each_scheme_info['KCZMS'])
        info.append(each_scheme_info['KCZXF'])
        info.append(each_scheme_info['YQZXF'])
        info.append(each_scheme_info['KCZXS'])
        info.append(each_scheme_info['XZLXMC'])
        info.append(each_scheme_info['XKMLM'])
        info.append(each_scheme_info['ZYKC'].replace("\n", "").replace(" ", ""))

        csv_info = ','.join(str(n) for n in info)
        csv_info += '\n'
        f.writelines(csv_info)

    # print(scheme_info)
    pass


if __name__ == '__main__':
    f.writelines(scheme_title)
    session = requests.session()
    stu_cookie = {"JSESSIONID": "cdaVFpysIGd5P-SnaQ5my", "selectionBar": "1293218"}
    session.cookies = cookiejar_from_dict(stu_cookie)
    for grade in grades:
        get_fajhh(grade, session)


