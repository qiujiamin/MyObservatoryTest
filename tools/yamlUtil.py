import os
import sys

import yaml

from pathlib import Path
import pytest
from httprunner.loader import locate_file

sys.path.insert(0, str(Path(__file__).parent.parent))

cur_path = os.path.dirname(os.path.realpath(__file__))
sql_file_path = os.path.dirname(cur_path) + "\\sqlmapper\\finc_sql.yml"


def open_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_configPath():
    try:
        run_env = os.environ["run_env"]
        if run_env == "test":
            config_Path = r"config/test_config.yaml"
        elif run_env == "dev":
            config_Path = r"xxx.yaml"
        elif run_env == "uat":
            config_Path = r"config/xxx.yaml"
    except KeyError:
        config_Path = r"config/test_config.yaml"
    finally:
        # 返回绝对路径
        return locate_file(str(Path(__file__).parent.parent), config_Path)


def get_sqlPath():
    return locate_file(str(Path(__file__).parent.parent), r"sqlmapper/sql.yaml")


def get_test_runPath():
    return locate_file(str(Path(__file__).parent.parent), r"config/main_run.yaml")


def get_test_headersPath():
    return locate_file(str(Path(__file__).parent.parent), r"data/heards/headers.yaml")


def get_yaml_data(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
    return content


def get_finc_sql(key):
    """获取社区sql语句"""
    try:
        yaml_data = open_yaml(sql_file_path)
        return yaml_data[key]
    except Exception as ex:
        pytest.skip(str(ex))


if __name__ == "__main__":
    # print(getCommunitySqlPath())
    print(get_finc_sql("topic_id"))
