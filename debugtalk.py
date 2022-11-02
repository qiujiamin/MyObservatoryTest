# import logging
from loguru import logger
import datetime
from tools.yamlUtil import *
from tools.csvUtil import CSVUtil

configPath = get_configPath()
cs = CSVUtil()

#  获取config配置
def get_config(key):
    return open_yaml(configPath)[key]
# 获取app服务器地址
def get_app_base_url():
    return str(get_config("app")["base_url"])
def get_todayhour():
    time = str(datetime.date.today()).replace("-","")+"10"
    return time

def writeToCSVData(path,*row):
    cs.writeCsv(path,*row)
# 返回x天后的日期，默认2天，eg：当天20220225 返回20220227
def get_day_strftime(days=2):
    t = datetime.datetime.now() + datetime.timedelta(hours=int(days) * 24)
    t1 = t.strftime("%Y%m%d%H")
    return t1

# 提取接口返回数据，内嵌列表，里层列表元素为日期每小时及湿度值
def th_GetJmepathData():
        try:
            from testcases.wed_test import TestCaseWedTest
            datalist = TestCaseWedTest().test_start().get_export_variables().get("dataList")
            print(datalist)
            return datalist
        except Exception:
            logger.error("异常，请检查")

def th_filterNWrite():
    datalist = th_GetJmepathData()
    aftertomorrow = str(get_day_strftime())
    writedataPath = r"data/result.csv"
    num_len = len(datalist)
    listwed=[]
    x = 0
    for i in range(num_len) :
        if datalist[i][1] ==None:
            datalist[i][1] = 0
            x += 1
        listwed.append(datalist[i][1])
        if  datalist[i][0] == aftertomorrow:
            # 写入当前时间点湿度
            current_humidity = str(datalist[i][1])+"%"
            current_day = aftertomorrow
    listwed.sort()
    min = str(listwed[x])+"%"
    max = str(listwed[-1])+"%"
    print(listwed)
    writeToCSVData(writedataPath,current_day,current_humidity,min,max)

if __name__ == '__main__':
    th_filterNWrite()
