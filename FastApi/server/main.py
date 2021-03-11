#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    desc: 数据api
    author: liukun
    date: 2020-12-08
'''

import traceback
try:
    import sys
    from __init__ import _project_root
    sys.path.append(_project_root)
except Exception as e:
    traceback.print_exc()
from typing import Dict
import uvicorn
from server import curd, datacenter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
import os

from fastapi import FastAPI, BackgroundTasks,Body, Depends
from fastapi import File, UploadFile, status

from fastapi.responses import FileResponse, Response, StreamingResponse

from pydantic import BaseModel
from basic import schemas
from typing import List
from learning import rule
from typing import Any

app = FastAPI()

@app.post("/do/classify/", response_model=Dict)
def ruing_alone_classify_task(data: Dict):
    """
    运行简单文本的分类,并返回分类结果

    Args：
        {"batch_id": 0,"text":""}

    Returns:
        {"name":"","batch_id":"",category_mapping_id:}
    """
    try:
        batch_id = data.get("batch_id")
        text = data.get("text")
        if not isinstance(batch_id, str):
            batch_id = str(batch_id)
        category_mapping_info = datacenter.get_category_mapping_info()
        rule_model = [rule.RuleModel(category, model_info) for category, model_info in
                    datacenter.get_rule_model_group(batch_id).items()]
        rule_groups = rule.RuleModelGroups(rule_model)
        tasker = rule.RulePredictTasker(rule_groups, category_mapping_info)
        category = tasker.alone_run(text)
        category_mapping_id = curd.get_category_mapping_id(batch_id,category)
        result = {
            "name":category,
            "batch_id":batch_id,
            "category_mapping_id":category_mapping_id
        }
        return result
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "classify error"})
        

@app.get("/pagesize/get/list", response_model=List[int])
def get_user_list():
    """
    [获得pagesize 列表]

    Returns:
        [List]: [可以选择的页面]
    """
    pagesize_list = [
        5,
        10,
        20,
        30,
    ]
    return pagesize_list


@app.get("/user/get/list", response_model=List[schemas.UserEntity])
def get_user_list():
    """[获得所有的用户列表]

    Returns:
        [type]: [用户的列表信息]
    """
    user_list = []
    user_list.append(
        schemas.UserEntity(name="jack", oid=1)
    )
    user_list.append(
        schemas.UserEntity(name="niuqun", oid=2)
    )
    return user_list


@app.get("/category/get/list", response_model=List[schemas.CategoryEntity])
def get_category_list():
    """[获得所有分类的类别列表]

    Returns:
        [type]: [分类类别的列表信息]
    """
    category_list = curd.get_category_list()
    return category_list


@app.get("/validationdata/get/list", response_model=List[schemas.ValidationDataEntity])
def get_Validation_list(page_size=50, category="预测的类别"):
    """
    [
        获得要校验的数据列表
    ]
    Returns:
        [type]: [用户的列表信息]
    """
    data_list = []
    print(page_size)
    db_data_list = curd.get_not_sure_data(
        page_no=0, page_size=page_size, category=category)
    print(db_data_list)
    return db_data_list


@app.post("/validationdata/post/result", status_code=status.HTTP_200_OK)
def deal_Validation_list(data: Dict):
    """

    """
    def quick_dict(data, key_name):
        data_info = {}
        for data_id in data[key_name]:
            data_info[data_id] = data[str(data_id)]
        return data_info
    # {'581': '其他', '16234': '预测类型', 'right': [14760, 14931], 'wrong': [436], 'other': [581, 16234]}
    # 第一步设置正确的数据。
    # 第二步，设置wrong的数据。
    # 第三步other的数据。
    # 先update 本地的数据表，把finshed设置为1.
    print(data)
    right_data_info = quick_dict(data, 'right')
    curd.set_right_data(right_data_info)
    wrong_data_info = quick_dict(data, 'wrong')
    curd.set_wrong_data(wrong_data_info)
    other_data_info = quick_dict(data, 'other')
    curd.set_other_data(other_data_info)
    print(right_data_info, wrong_data_info, other_data_info)

    print(data)


@app.post("/regular_info/list/", response_model=List[Dict])
def get_regular_list(data: Dict):
    """
    根据batch_id and category_id和 返回此批次的规则模型组

    Args:
        {"batch_id": 0,"category_id": 4}
    """
    batch_id = data.get("batch_id")
    category_id = data.get("category_id", None)
    if not isinstance(batch_id, str):
        batch_id = str(batch_id)
    try:
        regular_info_list = curd.get_regular_list(batch_id, category_id)
        return regular_info_list
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})


@app.post("/regular_info/add/", status_code=status.HTTP_200_OK)
def add_regular_info(data: Dict):
    """
    插入一条规则信息

    Args:
        {"batch_id": "0","category_id": "4", "content": "(代码){1,}.*?(简称){1,}.*?(公告){1,}", "regular_type":"pos"}
    """
    #{"batch_id": "0","category_id": "4", "content": "(代码){1,}.*?(简称){1,}.*?(公告){1,}", "regular_type":"pos"}
    #{"batch_id": "0","category_id": "1", "content": "业绩预告期间", "regular_type":"pos"}
    #{"batch_id": "0","category_id": "2", "content": "预计的?业绩|经营业绩", "regular_type":"pos"}
    print(data)
    batch_id = data.get("batch_id", "0")
    category_id = data.get("category_id", "null")
    content = data.get("content", "null")
    regular_type = data.get("regular_type", "null")
    if content == 'null' or regular_type == 'null' or category_id == "null":
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message":"Please fill out regular content or regular type or category_id"})
    try:
        curd.add_regular_info(batch_id, category_id, content, regular_type)
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})


@app.delete("/regular_info/delete/", status_code=status.HTTP_200_OK)
def delete_regular(data: Dict):
    """
    删除一条规则信息
    """
    print(data)
    regular_id = data.get("regular_id")
    if not isinstance(regular_id, int):
        regular_id = int(regular_id)
    try:
        result = curd.delete_regular(regular_id)
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"massage": "没有找到需要删除的regular"})
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})


@app.post("/regular_info/update/", status_code=status.HTTP_200_OK)
def update_regular_info(data: Dict):
    """
    修改一条规则信息

    Args:
        {"regular_id": 1, "content": "1111","regular_type": "pos"}
    """
    print(data)
    regular_id = data.get("regular_id")
    content = data.get("content")
    regular_type = data.get("regular_type")
    try:
        result = curd.update_regular_info(regular_id, content, regular_type)
        if not result:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "regular_id not fount in db"})
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})


@app.post("/batch_info/detail/", response_model=List[Dict])
def get_batch_info(data: Dict):
    """
    根据batch_id 获取到batch_info

    Returns:
        [{batch_info}]
    """
    batch_id = data.get("batch_id")
    if not isinstance(batch_id, int):
        batch_id = int(batch_id)
    batch_info = curd.get_batch_info(batch_id)
    return batch_info


@app.get("/batch_info/list/", response_model=List[Dict])
def get_batch_info_list():
    """
    根据batch_id 获取到batch_info_list

    Returns:
        [{batch_info}]
    """
    batch_info_list = curd.get_batch_list()
    return batch_info_list


@app.post("/batch_info/add/", status_code=status.HTTP_200_OK)
def add_batch_info(data: Dict):
    """
    添加一条batch信息
    """
    print(data)
    batch_name = data.get("name")
    batch_desc = data.get("desc", 'null')
    if not isinstance(batch_name, str):
        batch_name = str(batch_name)
    if not isinstance(batch_desc, str):
        batch_desc = str(batch_name)
    curd.add_batch_info(batch_name, batch_desc)


@app.delete("/batch_info/delete/", status_code=status.HTTP_200_OK)
def delete_batch(data: Dict):
    batch_id = data.get("batch_id")
    curd.delete_batch(batch_id)


@app.post("/batch_info/update/", status_code=status.HTTP_200_OK)
def update_batch_info(data: Dict):
    """
    更新batch信息

    Args：
        {"name":"", "batch_id":1, desc:""}
    """
    print(data)
    batch_name = data.get("name")
    batch_id = data.get("batch_id")
    batch_desc = data.get("desc", "null")
    if isinstance(batch_id, int):
        batch_id = int(batch_id)
    result = curd.update_batch_info(batch_id, batch_name, batch_desc)
    if not result:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/category_info/add/", status_code=status.HTTP_200_OK)
def add_category(data: Dict):
    """
    添加一条类别信息

    Args：
        { "name": "业绩预告","desc":"这只是一个测试的类别", "batch_id": 2,"category_mapping_id":3}
        目前判定的是desc会出现为空的情况
    """
    print(data)
    batch_id = data.get("batch_id")
    category = data.get("name")
    category_mapping_id = data.get("category_mapping_id")
    category_desc = data.get("desc", None)
    if not isinstance(batch_id, str):
        batch_id = str(batch_id)
    if not isinstance(category, str):
        category = str(category)
    if not isinstance(category_mapping_id, int):
        category_mapping_id = int(category_mapping_id)
    try:
        curd.add_category(batch_id, category, category_mapping_id, category_desc)
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"massage": "An error occurred while interacting with the database"})


@app.delete("/category_info/delete/", status_code=status.HTTP_200_OK)
def delete_category(data: Dict):
    """
    删除一条类别信息
    """
    category_id = data.get("category_id")
    if not isinstance(category_id, int):
        category_id = int(category_id)
    result = curd.delete_category(category_id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"massage": "category_id not fount in db"})


@app.post("/category_info/list/", response_model=List)
def get_category_list(data: Dict):
    """
    查看batch_id下所有的category_info

    """
    print(data)
    batch_id = data.get("batch_id")
    if not isinstance(batch_id, str):
        batch_id = str(batch_id)
    category_list = curd.get_category_info_list(batch_id)
    return category_list


@app.post("/category_info/update/", status_code=status.HTTP_200_OK)
def update_category(data: Dict):
    """
    更新一条category数据

    Returns:
        正常执行 return：200
        不存在更新的数据 return：404
        执行数据库操作报错 return: 500
    """
    print(data)
    category_id = data.get("category_id")
    batch_id = data.get("batch_id")
    category = data.get("name")
    category_desc = data.get("desc", None)
    category_mapping_id = data.get("category_mapping_id")
    if not isinstance(category_id, int):
        category_id = int(category_id)
    if not isinstance(batch_id, str):
        batch_id = str(batch_id)
    try:
        result = curd.update_category(batch_id, category_mapping_id, category, category_desc, category_id)
        if not result:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "category_id not fount in db"})
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})

@app.post("/dataset_info/add/", status_code=status.HTTP_200_OK)
def add_dataset(data: schemas.CreateDatasetInfoEntity):
    """
    添加一条数据集信息

    Args：
        { 
            "name": "数据集的名称",
            "desc":"数据集合的备注"
        }
        目前判定的是desc会出现为空的情况
    """
    print(data)
    name=data.name
    desc=data.desc
    try:
        result=curd.add_dataset_info(name=name,desc=desc)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"row_num": result})
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})

@app.post("/dataset_info/update/", status_code=status.HTTP_200_OK)
def update_dataset(data:schemas.DatasetInfoEntity):
    """
    
    [
        更新数据集信息
    ]

    Args:
        data (schemas.DatasetInfoEntity): [description]

    Returns:
        [int ]: [ ]
    """
    try:
        result=curd.update_dataset_info(data)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"row_num": result})
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})


@app.delete("/dataset_info/delete/{dataset_id}/",status_code=status.HTTP_200_OK)
def delete_dataset_info(dataset_id:int):
    try:
        result=curd.delete_dataset_info(dataset_id=dataset_id)
        return  JSONResponse(status_code=status.HTTP_200_OK, content={"row_num": result})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})
 

@app.get("/dataset_info/detail/{dataset_id}/",status_code=status.HTTP_200_OK, response_model=schemas.DatasetInfoEntity )
def get_dataset_info(dataset_id:int):
    """
    [
        获取数据集信息
    ]

    Args:
        dataset_id (int): [description]

    Returns:
        [type]: [description]
    """
    try:
        result=curd.get_dataset_info(dataset_id)
        return result
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})


@app.get("/dataset_info/list/",status_code=status.HTTP_200_OK, response_model=List[schemas.DatasetInfoEntity] )
def get_dataset_info():
    """
    [
        获取数据集信息
    ]

    Args:
        dataset_id (int): [description]

    Returns:
        [type]: [description]
    """
    try:
        result_list=curd.list_dataset_info()
        return result_list
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})
   


@app.post("/text_info/add/", status_code=status.HTTP_200_OK)
def batch_add_text_info(data:Dict):
    """
    向一个数据集合中增加一批语料数据

    Args：
        { 
            "dataset_id": "int , 数据集的id",
            "text_list":"文本数据列表 [ "我的盘古啊","我的太阳啊"]"
        }
        目前判定的是desc会出现为空的情况
    """
    #print(data)
    try:    
        dataset_id=data.get("dataset_id")
        text_list=data.get("text_list")
        result=curd.batch_add_origin_text_info(dataset_id=dataset_id,text_list=text_list)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"row_num": result})
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})

@app.post("/text_info/list/", status_code=status.HTTP_200_OK)
def list_text_info(data:Dict):
    """
    按照页面返回数据.

    Args：
        { 
            "dataset_id": "int , 数据集的id",
            "page_size":"页面包含数据的个数",
            "page_index": "第几个页面"
        }
        
    Return:
     [
         [oid,text,dataset_id]
     ]
    """
    print(data)
    try:    
        dataset_id=data.get("dataset_id")
        page_size=data.get("page_size",50)
        page_index=data.get("page_index",0)
        result=curd.list_origin_text_info(dataset_id,page_index,page_size)
        return JSONResponse(status_code=status.HTTP_200_OK, content= result)
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})

@app.post("/text_info/update/",status_code=status.HTTP_200_OK)
def update_text_info(data:schemas.TextInfoEntity):
    print(data)
    try:
        result=curd.update_origin_text_info(oid=data.oid,text=data.text)
        return JSONResponse(status_code=status.HTTP_200_OK, content= result)
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})
    pass 

@app.delete("/text_info/delete/",status_code=status.HTTP_200_OK)
def delete_text_info(data:schemas.DeleteInfoEntity):
    print(data)
    try:
        result=curd.delete_origin_text_info(oid=data.oid)
        return JSONResponse(status_code=status.HTTP_200_OK, content= result)
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "An error occurred while interacting with the database"})
    pass 

@app.post("/create/rule/predict/task", status_code=status.HTTP_200_OK)
def create_rule_predict_task(data:schemas.RulePredictingTask):
    """
    [
        创建一个预测的任务
    ]

    Args:
        data (schemas.RulePredictingTask): [description]
    """
    from tasks.predictions import ruleTask
    result=curd.add_rule_predict_task(data.dataset_id,data.batch_id)
    BackgroundTasks.add_task()






if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
