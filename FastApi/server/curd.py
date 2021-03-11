# -*- coding: utf-8 -*-
'''
    desc: 数据库操作。
    author: liukun
    date: 2020-12-08
'''

from datetime import timedelta, datetime
import pathlib
import sys

_project_root = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(_project_root)
from basic import schemas
from server.database import XUncertainCategoryTable, XIsNotCategoryTable, XIsCategoryTable, OriginTextDataTable, \
    BatchRegularInfoTable, BatchCategoryInfoTable
from learning import rule
from server import database
from typing import List


def get_not_sure_data(page_no: int = 0, page_size: int = 20, category="预计的业绩"):
    """
    根据category查询page_no页，page_size数量的信息

    Args:
        page_no (int): 数据库查询到的页数
        page_size (int): 数据库查询每页的数量
        category (str): 类别

    Returns:
        [ ValidationDataEntity ]

    """
    page_no = int(page_no)
    page_size = int(page_size)
    with database.db_session() as db:
        query_result_list = db.query(XUncertainCategoryTable).filter(XUncertainCategoryTable.finished == 0,
                                                                          XUncertainCategoryTable.category == category).order_by(
                                                                          XUncertainCategoryTable.prob.desc()).limit(page_size).offset(page_size * page_no).all()
        ans_list = []
        for query_result in query_result_list:
            ans_list.append(
                schemas.ValidationDataEntity(
                    data_oid=query_result.data_oid,
                    category=query_result.category,
                    category_from=query_result.category_from,
                    prob=query_result.prob,
                    accuray=query_result.prob,
                    text=db.query(OriginTextDataTable.text).filter(
                        OriginTextDataTable.data_oid == query_result.data_oid).first()[0]
                )
            )
    return ans_list


def set_other_data(data_id_info={}):
    """
    根据data_id、beach_id 修改XUncertainCategoryTable 表中的内容，插入到XIsCategoryTable表中，如果存在修改category的值
    XIsCategoryTable中data_id 必须唯一

    Args:
        data_id_info (Dict): { data_id:category }    目前缺少beach_id

    Returns:

    """
    with database.db_session() as db:
        for k, v in data_id_info.items():
            db.query(XUncertainCategoryTable).filter(XUncertainCategoryTable.data_oid == k,
                                                          XUncertainCategoryTable.finished == 0).update(
                {XUncertainCategoryTable.finished: 1, XUncertainCategoryTable.judgment_type: 3,
                 XUncertainCategoryTable.judgment_category: v})
            query_result_list = db.query(XIsCategoryTable).filter(XIsCategoryTable.data_oid == k)
            if query_result_list.count() == 0:
                data = XIsCategoryTable(data_oid=k, category=v)
                db.add(data)
                db.commit()
            else:
                data = query_result_list.one()
                if data.category != v:
                    data.category = v
                    db.commit()
                else:
                    pass


def set_wrong_data(data_id_info={}):
    """
    根据data_id、beach_id修改XUncertainCategoryTable 表中的内容，插入到XIsNotCategoryTable表中，
    如果category相同则跳过处理,如果category不同，需要添加此条信息而不是更新

    Args:
        data_id_info (Dict): { data_id:category }   目前缺少beach_id，不能进行准确定位。暂时进行统一的增加处理
    
    Returns:

    """
    with database.db_session() as db:
        for k, v in data_id_info.items():
            db.query(XUncertainCategoryTable).filter(XUncertainCategoryTable.data_oid == k,
                                                          XUncertainCategoryTable.finished == 0).update(
                {XUncertainCategoryTable.finished: 1, XUncertainCategoryTable.judgment_type: 2})
            query_result_list = db.query(XIsNotCategoryTable).filter(XIsNotCategoryTable.data_oid == k)
            if query_result_list.count() == 0:
                data = XIsNotCategoryTable(data_oid=k, category=v)
                db.add(data)
                db.commit()
            else:
                for query_result in query_result_list:
                    if query_result.category == v:
                        return;
                data = XIsNotCategoryTable(data_oid=k, category=v)
                db.add(data)
                db.commit()


def set_right_data(data_id_info={}):
    """
    根据data_id、beach_id 修改XUncertainCategoryTable 表中的内容，插入到XIsCategoryTable表中，如果存在修改category的值
    XIsCategoryTable中data_id 必须唯一

    Args:
        data_id_info (Dict): { data_id:category }    目前缺少beach_id

    Returns:

    """
    with database.db_session() as db:
        for k, v in data_id_info.items():
            db.query(XUncertainCategoryTable).filter(XUncertainCategoryTable.data_oid == k).update(
                {XUncertainCategoryTable.finished: 1, XUncertainCategoryTable.judgment_type: 1,
                 XUncertainCategoryTable.judgment_category: v})
            query_result_list = db.query(XIsCategoryTable).filter(XIsCategoryTable.data_oid == k)
            if query_result_list.count() == 0:
                data = XIsCategoryTable(data_oid=k, category=v)
                db.add(data)
                db.commit()
            else:
                data = query_result_list.one()
                if data.category != v:
                    data.category = v
                    db.commit()
                else:
                    pass


def add_regular_info(batch_id: str, category_id: int, content: str, regular_type: str):
    """
    添加正则，若数据库不存在数据则添加，
    若数据库存在数据，content不相同则添加。
    若存在，content相同则跳过
    """
    with database.db_session() as db:
        query_result_list = db.query(BatchRegularInfoTable).filter(BatchRegularInfoTable.batch_id == batch_id,
                                                                        BatchRegularInfoTable.category_id == category_id,
                                                                        BatchRegularInfoTable.regular_type == regular_type,
                                                                        BatchRegularInfoTable.content == content)
        if query_result_list.count() == 0:
            data = BatchRegularInfoTable(batch_id=batch_id, category_id=category_id, content=content, regular_type=regular_type)
            db.add(data)
            db.commit()
            return True


def delete_regular(regular_id: int) -> bool:
    """
    通过匹配参数，删除一条规则信息
    """
    with database.db_session() as db:
        if db.query(BatchRegularInfoTable).filter(BatchRegularInfoTable.regular_id == regular_id).count() == 0:
            return False
        db.query(BatchRegularInfoTable).filter(BatchRegularInfoTable.regular_id == regular_id).delete()
        db.commit()
    return True


def get_regular_list(batch_id: str, category_id=None) -> list:
    """
    获取regular列表

    Returns:
        [{centent、regular_type、regular_id}]
    """
    regular_info_list = []
    with database.db_session() as db:
        if category_id:
            query_result_list = db.query(BatchRegularInfoTable).filter(BatchRegularInfoTable.batch_id == batch_id,
                                                                        BatchRegularInfoTable.category_id == category_id)
        else:
            query_result_list = db.query(BatchRegularInfoTable).filter(BatchRegularInfoTable.batch_id == batch_id)
        for query_result in query_result_list:
            info = {
                "category_id": query_result.category_id,
                "content": query_result.content,
                "regular_type": query_result.regular_type,
                "regular_id": query_result.regular_id,
                "category_name": db.query(BatchCategoryInfoTable).filter(BatchCategoryInfoTable.category_id == query_result.category_id).one().category
            }
            regular_info_list.append(info)
    return regular_info_list


def update_regular_info(regular_id: int, content: str, regular_type: str):
    """
    通过匹配参数，修改一条正则信息
    """
    with database.db_session() as db:
        if db.query(BatchRegularInfoTable).filter(BatchRegularInfoTable.regular_id == regular_id).count() == 0:
            return False
        query_result = db.query(BatchRegularInfoTable).filter(BatchRegularInfoTable.regular_id == regular_id).one()
        query_result.content = content
        query_result.regular_type = regular_type
        db.commit()
        return True


def get_category_list() -> list:
    """
    获取所有的category信息

    Returns:
        [ CategoryEntity ]
    """

    category_list = []
    with database.db_session() as db:
        query_result_list = db.query(BatchCategoryInfoTable).all()
        for query_result in query_result_list:
            category_list.append(
                schemas.CategoryEntity(
                    name=query_result.category,
                    batchid=query_result.batch_id
                )
            )
    return category_list


def get_batch_info(batch_id) -> list:
    """
    获取batch信息

    Returns:
        [{batch_info}]
    """
    batch_info = []
    with database.db_session() as db:
        query_result_list = db.query(database.BatchInfoTable).filter(database.BatchInfoTable.batch_id == batch_id)
        for query_result in query_result_list:
            info = {
                "name": query_result.batch_name,
                "batch_id": query_result.batch_id,
                "desc": query_result.batch_desc
            }
            batch_info.append(info)
    return batch_info


def get_batch_list() -> list:
    """
    获取batch信息

    Returns:
        [{batch_info}]
    """
    batch_info_list = []
    with database.db_session() as db:
        query_result_list = db.query(database.BatchInfoTable).all()
        for query_result in query_result_list:
            info = {
                "name": query_result.batch_name,
                "batch_id": query_result.batch_id,
                "desc": query_result.batch_desc
            }
            batch_info_list.append(info)
    return batch_info_list


def add_batch_info(batch_name, batch_desc):
    """
    添加batch，通过batch_name查询，若存在则查看desc是否相同，不相同则更改。若不存在则添加
    去除相同的逻辑
    """
    with database.db_session() as db:
        query_result_list = db.query(database.BatchInfoTable).filter(database.BatchInfoTable.batch_name == batch_name,
                                                                          database.BatchInfoTable.batch_desc == batch_desc)
        if query_result_list.count() == 0:
            data = database.BatchInfoTable(batch_name=batch_name, batch_desc=batch_desc)
            db.add(data)
            db.commit()
        else:
            pass


def delete_batch(batch_id):
    """
    删除一条batch信息
    """
    with database.db_session() as db:
        db.query(database.BatchInfoTable).filter(database.BatchInfoTable.batch_id == batch_id).delete()
        db.commit()



def update_batch_info(batch_id, batch_name, batch_desc):
    """
    根据batch_id 更改batch_info。如果不存在batch_id  return None
    """
    with database.db_session() as db:
        query_result_list = db.query(database.BatchInfoTable).filter(database.BatchInfoTable.batch_id == batch_id)
        if query_result_list.count() == 0:
            return False
        else:
            data = db.query(database.BatchInfoTable).filter(database.BatchInfoTable.batch_id == batch_id).one()
            data.batch_name = batch_name
            data.batch_desc = batch_desc
            db.add(data)
            db.commit()
            return True


def add_category(batch_id, category, category_mapping_id, category_desc):
    """
    添加一条类别信息
    """
    with database.db_session() as db:
        query_result_list = db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.batch_id == str(batch_id),
                                                                                  database.BatchCategoryInfoTable.category == category,
                                                                                  database.BatchCategoryInfoTable.category_mapping_id == category_mapping_id,
                                                                                  database.BatchCategoryInfoTable.category_desc == category_desc)
        if query_result_list.count() == 0:
            if not category_desc:
                data = database.BatchCategoryInfoTable(batch_id=batch_id, category=category, category_mapping_id=category_mapping_id)
            else:
                data = database.BatchCategoryInfoTable(batch_id=batch_id, category=category, category_mapping_id=category_mapping_id, category_desc=category_desc)
            db.add(data)
            db.commit()


def delete_category(category_id):
    """
    删除一条类别信息
    """
    with database.db_session() as db:
        if db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.category_id == category_id).count() == 0:
            return False
        db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.category_id == category_id).delete()
        db.commit()
        db.close()
        return True


def get_category_info_list(batch_id: str):
    """
    查看所有的category信息

    """
    category_info_list = []
    with database.db_session() as db:
        query_result_list = db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.batch_id == batch_id).order_by(database.BatchCategoryInfoTable.category_id)
        if query_result_list.count() == 0:
            return category_info_list
        for query_result in query_result_list:
            category_info_list.append(
                schemas.CategoryEntity(
                    name=query_result.category,
                    batch_id=query_result.batch_id,
                    desc=str(query_result.category_desc),   #TODO: 这里是否需要处理，目前是如果返回的为None则返回str类型
                    category_id=query_result.category_id,
                    category_mapping_id=query_result.category_mapping_id
                )
            )
    return category_info_list


def update_category(batch_id: str, category_mapping_id: int, category: str, category_desc: str, category_id: int):
    """
    更新一条category信息
    """
    with database.db_session() as db:
        query_result_list = db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.category_id == category_id)
        if query_result_list.count() == 0:
            return False
        else:
            data = db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.category_id == category_id).one()
            data.batch_id = batch_id
            data.category_mapping_id = category_mapping_id
            data.category = category
            data.category_desc = category_desc
            db.add(data)
            db.commit()
            return True


def get_category_mapping_id(batch_id: str, category: str):
    with database.db_session() as db:
        query_result_list = db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.batch_id == batch_id, database.BatchCategoryInfoTable.category == category)
        if query_result_list.count() == 0:
            return -1
        else:
            query_result = db.query(database.BatchCategoryInfoTable).filter(database.BatchCategoryInfoTable.batch_id == batch_id, database.BatchCategoryInfoTable.category == category).first()
            return query_result.category_mapping_id


def add_dataset_info(name:str,desc:str):
    """
    [
        增加一个数据集信息,返回创建数据的个数
    ]

    Args:
        name (str): [数据集名称]
        desc (str): [数据集描述]
    """
    with database.db_session() as db:
        
        try:
            ds_obj=database.DataSetInfoTable(dataset_name=name,dataset_desc=desc)
            db.add(ds_obj)
            db.commit()
            print(ds_obj.oid)
            return 1 
        except Exception as e:
            print(e)
        return 0

def delete_dataset_info(dataset_id:int):
    with database.db_session() as db:
        try:
            data_list=db.query(database.DataSetInfoTable).filter(database.DataSetInfoTable.oid == dataset_id)
            if data_list.count() == 0:
                return 0
            db.query(database.DataSetInfoTable).filter(database.DataSetInfoTable.oid == dataset_id).delete()
            db.commit()
            return 1
        except  Exception as e :
            print(e)
        return 0



def get_dataset_info(dataset_id):
    with database.db_session() as db:
        try:
            ds_obj_list=db.query(database.DataSetInfoTable).filter(database.DataSetInfoTable.oid==dataset_id)
            if ds_obj_list.count()>0:
                ds_obj=ds_obj_list[0]
                return schemas.DatasetInfoEntity(dataset_id=ds_obj.oid,name=ds_obj.dataset_name,desc=ds_obj.dataset_desc)
            else:
                return {}
        except Exception as e:
            print(e)
    return {}

def update_dataset_info(data:schemas.DatasetInfoEntity):
    with database.db_session() as db:
        try:
            ds_obj_list=db.query(database.DataSetInfoTable).filter(database.DataSetInfoTable.oid==data.dataset_id)
            if ds_obj_list.count()>0:
                ds_obj=ds_obj_list[0]
                ds_obj.dataset_name=data.name
                ds_obj.dataset_desc=data.desc 
                db.commit()
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
    return 0



def list_dataset_info():
    ans_list=[]
    with database.db_session() as db:
        try:
            ds_obj_list=db.query(database.DataSetInfoTable).all()
            for ds_obj in ds_obj_list:
                ans_list.append(schemas.DatasetInfoEntity(dataset_id=ds_obj.oid,name=ds_obj.dataset_name,desc=ds_obj.dataset_desc))
        except Exception as e:
            print(e)
    print(ans_list)
    return ans_list

def update_origin_text_info(oid , text):
    """[summary]

    Args:
        oid ([int]): [文本的唯一id]
        text ([str]): [最新的文本]
    """
    with database.db_session() as db:
        try:
            ds_obj_list=db.query(database.OriginTextDataTable).filter(database.OriginTextDataTable.oid==oid)
            if ds_obj_list.count()>0:
                ds_obj=ds_obj_list[0]
                ds_obj.text=text
                db.commit()
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
    return 0
 

def add_origin_text_info(dataset_id , text):
    """
    [ 增加一个文本数据 ]

    Args:
        dataset_id ([int]): [数据id]
        text ([string]): [文本内容]
    Returns:
        int: [ 创建对象的个数 ]
    """
    with database.db_session() as db:
        
        try:
            text_obj=database.OriginTextDataTable(dataset_id=dataset_id,text=text)
            db.add(text_obj)
            db.commit()
            return 1 
        except Exception as e:
            print(e)
        return 0
def batch_add_origin_text_info(dataset_id:int , text_list:List):
    """
    [批量增加文本数据]

    Args:
        dataset_id ([int]): [数据集id]
        text_list (List): [文本数据]

    Returns:
        int: [插入成功的个数]
    """
    sucess_count=0
    with database.db_session() as db:
        for text in text_list:
            try:
                text_obj=database.OriginTextDataTable(dataset_id=dataset_id,text=text)
                db.add(text_obj)
                db.commit()
                sucess_count=sucess_count+1
            except Exception as e:
                print(e)
    return sucess_count

def list_origin_text_info(dataset_id:int , page_index=0,page_size=50):
    ans_list = []
    with database.db_session() as db:
        query_result_list = db.query(database.OriginTextDataTable).filter(OriginTextDataTable.dataset_id == dataset_id).order_by(
                                                                          OriginTextDataTable.oid.desc()).limit(page_size).offset(page_size * page_index).all()
        
        for query_result in query_result_list:
            ans_list.append(
                {  
                    "oid":query_result.oid,
                    "text":query_result.text,
                    "dataset_id":query_result.dataset_id
                }
            )
    return ans_list

def list_all_origin_text_info(dataset_id:int):
    """[summary]

    Args:
        dataset_id (int): [description]

    Returns:
        [type]: [
                    [  
                        query_result.oid,
                        query_result.text,
                        query_result.dataset_id
                    ]
                ]
    """    
    ans_list = []
    with database.db_session() as db:
        query_result_list = db.query(database.OriginTextDataTable).filter(OriginTextDataTable.dataset_id == dataset_id).order_by(
                                                                          OriginTextDataTable.oid.desc()).all()
        for query_result in query_result_list:
            ans_list.append(
                [  
                    query_result.oid,
                    query_result.text,
                    query_result.dataset_id
                ]
            )
    return ans_list


def delete_origin_text_info(oid:int):
    with database.db_session() as db:
        try:
            data_list=db.query(database.OriginTextDataTable).filter(database.OriginTextDataTable.oid == oid)
            if data_list.count() == 0:
                return 0
            db.query(database.OriginTextDataTable).filter(database.OriginTextDataTable.oid == oid).delete()
            db.commit()
            return 1
        except  Exception as e :
            print(e)
        return 0


def add_rule_predict_task(dataset_id:int,batch_id:int):
    try:
        with database.db_session() as db:
            task_obj=database.RulePredictTask(
                dataset_id=dataset_id,
                batch_id=batch_id
            )
            db.add(task_obj)
            db.commit()

            return task_obj.oid
    except Exception as e:
            print(e)
            return -1




if __name__ == "__main__":
    # get_not_sure_data(3,40)
   # add_dataset_info(name="测试数据集",desc="2021-01-28")
    # add_dataset_info(dataset_id=3,text="一个洗呢长的文本呢")
    #batch_add_dataset_info(dataset_id=4,text_list=["一个洗呢长的文本呢","一种测试工作"])
   # list_origin_text_info(0,page_size=100)
    #update_dataset_info(schemas.DatasetInfoEntity(**{'dataset_id':7,'name':"ceshi",'desc':"ceshi"}))
    #add_rule_predict_task(1,2)
    #get_dataset_info(dataset_id=8)
    update_origin_text_info(oid=10,text="我就是测试一下")
    delete_origin_text_info(8013)
    #update_origin_text_info(oid)
    # set_wrong_data({14684: "预计的业绩", 17127: "UNKNOW"})
    # add_category('0','元信息',4, None)
