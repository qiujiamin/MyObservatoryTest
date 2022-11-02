import platform

from tools.runUtil import  cmd_run
from tools.yamlUtil import open_yaml, get_test_runPath

# 获取配置文件位置
test_runPath = get_test_runPath()

# 运行案例
if __name__ == '__main__':
    print(platform.system())
    cmd_run()
