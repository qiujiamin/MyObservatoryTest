import os
import sys
from typing import List
from loguru import logger
from tools.yamlUtil import open_yaml, get_test_runPath
import platform

# 获取配置文件位置
test_runPath = get_test_runPath()

def cmd_run():
    try:
        env = os.environ["env"]
    except KeyError:
        env = 'localhost'
    # Jenkins运行获取Jenkins转入参数
    if env == 'jenkins':
        # 获取参数
        try:
            allure = None
            tmp_testcases = sys.argv[1].split("=")[1]
            print(f"tmp_testcases>>>:{tmp_testcases}")
            tmp_marks = sys.argv[2].split("=")[1]
            tmp_rerun_fail = sys.argv[3].split("=")[1]
            tmp_ignores = sys.argv[4].split("=")[1]

            # 造数平台用
            if os.environ.get("jenkins_phone"):
                os.environ["jenkins_phone"] = os.environ.get("jenkins_phone")
            if sys.argv[5]:
                jenkins_env: List = sys.argv[5].split("=")[1].split(",")
                logger.debug(f'jenkins_env的值:{jenkins_env}')
            # 设置Jenkins环境变量
            if len(jenkins_env) > 0:
                for env in jenkins_env:
                    kv: List = env.split(":")
                    logger.debug(f'设置环境变量:os.environ[{kv[0]}] = {kv[1]}')
                    os.environ[kv[0]] = kv[1]
        except IndexError:
            tmp_marks = ""
            tmp_rerun_fail = ""

        # 将 tmp_testcases转化成list
        testcases = tmp_testcases.split(",")

        # 将 tmp_marks转化成list
        marks = tmp_marks.split(",")

        # 将 ignores转化成list
        ignores = tmp_ignores.split(",")

        # 判断是否失败重跑
        if tmp_rerun_fail == "True":
            rerun_fail = "--lf"
        elif tmp_rerun_fail == "False":
            rerun_fail = ""
        else:
            rerun_fail = ""

        # pip_install = "pip3 install -r requirements.txt"

    # 本地运行获取配置文件里需要运行的案例
    elif env == 'localhost':
        conftest = open_yaml(test_runPath)
        testcases = conftest["testcase"] if conftest["testcase"] is not None else ""
        marks = conftest["mark"] if conftest["mark"] is not None else ""
        rerun_fail = "--lf" if conftest["rerun_fail"] else ""
        allure = conftest["allure"]
        ignores = conftest["ignore"]
        # pip_install = "pip install -r requirements.txt"

    # Jenkins 和 localhost数据汇总处
    # 处理testcase包含多条案例
    tmp_testcase = ''
    for testcase in testcases:
        tmp_testcase += f"{testcase}  "

    # 不运行的案例
    tmp_ignore = ''
    for ignore in ignores:
        tmp_ignore += f"--ignore={ignore} "

    # 处理多个marks
    tmp_marks = ''
    for mark in marks:
        tmp_marks += f"{mark} or "
    if len(tmp_marks[:-4]) == 0:
        tmp_marks = r"not jenkinsPaidOrder"
    else:
        tmp_marks = tmp_marks[:-4]
        tmp_marks = tmp_marks + " and not jenkinsPaidOrder"

    # 最终执行的命令
    if platform.system() in ["Windows","Darwin"]:
        test_path = fr'pytest -vs  {tmp_testcase} {tmp_ignore} -m "{tmp_marks} " --clean-alluredir --alluredir result {rerun_fail}'

    elif platform.system() == "Linux":
        test_path = fr'python3 -m pytest -vs {tmp_testcase}  {tmp_ignore} -m "{tmp_marks} " --clean-alluredir --alluredir result {rerun_fail}'

    print(f"执行: {test_path}")

    # 执行命令pytest 命令
    os.system(test_path)

    # 是否需要生成报告
    if env == 'localhost' and allure:
        os.system("allure generate result/ -o allure-report/ --clean")
        os.system("allure open -h 127.0.0.1 -p 8884 allure-report/")

