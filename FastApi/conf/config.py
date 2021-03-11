#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    desc: 读取配置文件
    author: liukun
    date: 2020-05-01
'''

# 获取项目路径的标准代码
import sys
import os
# tips: 获取项目路径的标准代码
import traceback

try:
    from .__init__ import _project_root
    sys.path.append(_project_root)
except Exception as identifier:
    traceback.print_exc()

import errno
import  traceback
import copy
from yaml import load, dump
import yaml
import json
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_configer(config_abs_path):
    """
    [获得配置文件]

    Arguments:
        config_abs_path {[type]} -- [description]
    """
    yml_config={}
    with open(config_abs_path,"rb") as config_yml_file:
        try:
            yml_config=yaml.safe_load(config_yml_file)
            print(yml_config)
        except yaml.YAMLError as exc:
            print(exc)
            traceback.print_exc()
    return yml_config


class ClientConfiger:
    """
    [配置项管理器]
    """
    config_abs_path: str

    def __init__(self, _config_type, _config_abs_path):
        """[summary]

        Args:
            _config_abs_path ([string]): [文件的路径]

        Raises:
            FileNotFoundError: [_config_abs_path 找不到文件]
            FileExistsError: [_config_abs_path 不是文件]
        """
        self.config_type = _config_type
        if not os.path.exists(_config_abs_path):
            raise FileNotFoundError(_config_abs_path)
        if not os.path.isfile(_config_abs_path):
            raise FileExistsError()
        self.config_abs_path = _config_abs_path
        self.yaml_config = {}
        self.refresh_config()

    def refresh_config(self):
        try:
            with open(self.config_abs_path, "rb") as config_yml_file:
                yml_config = yaml.safe_load(config_yml_file)
                self.yaml_config = yml_config
                # print(yml_config)
        except yaml.YAMLError as exc:
            print(exc)
            traceback.print_exc()
        return self

    def get_remote_url(self, remote_url_name):
        url = self.yaml_config[self.config_type]["url"].get(remote_url_name)
        return "http://{host}:{port}{url}".format(host=self.yaml_config[self.config_type]["host"],
                                                  port=self.yaml_config[self.config_type]["port"], url=url)

    def get_config_value(self, config_key_name):
        return self.yaml_config[self.config_type].get(config_key_name)

    def __repr__(self):
        return json.dumps(self.yaml_config, ensure_ascii=False, indent=4)

mysqlConfiger = ClientConfiger("mysql_config", _project_root+"/conf/running-config.yml")

piplineConfiger =  ClientConfiger("pipline", _project_root+"/conf/machineLearning/pipline.yml")
predictionPiplineConfiger=ClientConfiger("pipline", _project_root+"/conf/machineLearning/prediction_pipline.yml")
if __name__ == "__main__":
    configer=ClientConfiger("mysql_config", _project_root+"/conf/running-config.yml")
    print(configer)