# -*- coding: utf-8 -*-
'''
    desc: 本项目涉及的所有的实体模型
    author: liukun
    date: 2020-12-08
'''
from typing import List,Any,Dict
from pydantic import BaseModel 
from enum import Enum
import json
import datetime

import time


class BasicQueryParameter(BaseModel):
    """
    [
        查询对象的信息,查询第多少页,每页多少条数据.
    ]

    Args:
        BaseModel ([type]): [description]
    """    
    page_size:int=100
    page_index:int=0

class FilterQueryParameter(BasicQueryParameter):
    """
    [
        查询对象的信息,查询第多少页,每页多少条数据.
    ]

    Args:
        BaseModel ([type]): [description]
    """    
    csi_oid:int



class CategoryEntity(BaseModel):
    """
    [分类的类别 ]

    Returns:
        [type]: [description]
    """
    name: str # 类别名称
    #enable: bool =False# 是否启用   #TODO: enable还是否使用，前端接口目前没有定义
    batch_id: str #关联的批量的数据
    desc: str
    category_id: int
    category_mapping_id: int

    def jsonify(self):    #TODO: 这里在哪里使用到，是否需要改动
        return {
            "name":self.name,
            #"enable":self.enable,
            "batch_id": self.batchid,
        }

class UserEntity(BaseModel):
    """[
        检验人员基本信息
    ]

    Args:
        BaseModel ([type]): [description]

    Returns:
        [type]: [description]
    """
    name: str # 校验人员名称
    oid: str #
    def jsonify(self):
        return {
            "name":self.name,
            "oid":self.oid,
        }
class ValidationDataEntity(BaseModel):
    """
    [
        需要验证的数据
    ]

    Args:
        BaseModel ([type]): [description]
    """
    data_oid:int 
    category_from: str
    text: str 
    category: str
    prob: float 
    accuray:float 


class RulePredictingTask(BaseModel):
    """
    基于规则预测任务
    """
    batch_id: int # 分类标准的id
    dataset_id: int # 数据集id

class CreateDatasetInfoEntity(BaseModel):
    """
    数据集信息
    """
    name: str # 数据集合名称
    desc: str="" #  数据集合描述

class DatasetInfoEntity(CreateDatasetInfoEntity):
    dataset_id: int # 数据集id.
    
class TextInfoEntity(BaseModel):
    oid: int # 文本的id
    text:str # 文本内容

class DeleteInfoEntity(BaseModel):
    oid: int # 文本的id

if __name__ == "__main__":
    category=CategoryEntity(
        name="jack",
        enable=False,
        batchid=3,
    )
    
    print(category.json())







