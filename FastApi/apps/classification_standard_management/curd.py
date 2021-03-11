import pathlib
import sys
from sqlalchemy import engine,or_

from sqlalchemy.sql.base import Executable
from sqlalchemy.sql.elements import ClauseElement
# from sqlalchemy.sql.selectable import alias
_project_root = str(pathlib.Path(__file__).resolve().parents[2])
sys.path.append(_project_root)
from datetime import datetime
from server import database
from  apps.classification_standard_management.model import ClassificationItemInfoTable,ClassificationStandardInfoTable,CreateView
from basic.schemas import BasicQueryParameter, FilterQueryParameter

import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine,Table
from sqlalchemy.schema import Column,MetaData
from sqlalchemy.types import String, Integer, Boolean, Text, Date, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker,aliased


class DBManager:
    """
    [
        抽象的Model的增删改查的函数.
        通过设置ClassName= class 名称,实现对于数据的增删改查的设置. 
    ]

    Returns:
        [type]: [description]
    """    
    ClassName=None
    @classmethod
    def create(cls,**value_dict):
        with database.db_session() as db:
            
            obj=cls.ClassName(**value_dict)
            db.add(obj)
            db.commit()
    @classmethod
    def update(cls,oid:int,**value_dict):
        with database.db_session() as db:
            query_result_list =db.query(cls.ClassName).filter(cls.ClassName.oid==oid)
            if query_result_list.count()==0:
                return 0 
            else:
                obj=query_result_list[0]
                for key,value in value_dict.items():
                    if hasattr(obj,key) and key != "oid":
                        setattr(obj,key,value)
                db.commit()
                return 1
    @classmethod 
    def view(cls,oid:int):
        with database.db_session() as db:
            query_result_list =db.query(cls.ClassName).filter(cls.ClassName.oid==oid)
            if query_result_list.count()==0:
                return None 
            else:
                return query_result_list.one()
    @classmethod 
    def list_view(cls,parameter:BasicQueryParameter):
        with database.db_session() as  db:
            query_result=db.query(cls.ClassName).limit(parameter.page_size).offset(parameter.page_index*parameter.page_size)
            ans_list=[]
            if query_result.count()==0:
                return ans_list
            for  result in query_result:
                ans_list.append(result)
                print(result.jsonify())
            return ans_list
    @classmethod 
    def delete(cls,oid:int):
        with database.db_session() as  db: 
            query_result_list =db.query(cls.ClassName).filter(cls.ClassName.oid==oid)
            if query_result_list.count()==0:
                return 0 
            else:
                query_result_list.delete()
                db.commit()
                return 1 
    @classmethod
    def filter_list_view(cls,parameter:FilterQueryParameter):
        with database.db_session() as   db:
            csi_oid=parameter.csi_oid
            filter_list=db.query(cls.ClassName).filter(cls.ClassName.csi_oid==csi_oid).limit(parameter.page_size).offset(parameter.page_index*parameter.page_size)
            print(filter_list)
            ans_list=[]
            if  filter_list.count()==0:
                return 0
            for  filterlst in filter_list:
                ans_list.append(filterlst.jsonify())
            # print(ans_list)
            return  ans_list

    @classmethod 
    def detail_view(cls,Data:CreateView):
        with database.db_session() as db:
            cii=aliased(ClassificationItemInfoTable)
            csi=aliased(ClassificationStandardInfoTable)
            # 两表联查
            query_result=db.query(cii).join(csi,cii.csi_oid==csi.oid)
            ans_list=[]
            if  query_result.count()==0:
                return 0
            for  querylst    in query_result:
                ans_list.append(querylst.jsonify())
            # print(ans_list)
            return  ans_list

    @classmethod 
    def detail_filter_view(cls,Data:CreateView):
        with database.db_session() as db:
            query_result_list =db.query(cls.ClassName).filter(or_(
                cls.ClassName.name==Data.name,
                cls.ClassName.desc==Data.desc,
                cls.ClassName.create_datetime==Data.create_datetime,
                cls.ClassName.mapping_value==Data.mapping_value,
                cls.ClassName.csi_oid==Data.csi_oid,
                cls.ClassName.csi_name==Data.csi_name)).all()
            print(query_result_list)
            if query_result_list:
                return query_result_list
            else:
                return None 

class ClassificationStandardInfoDBManager(DBManager):
    ClassName=ClassificationStandardInfoTable


class ClassificationItemInfoTableDBManager(DBManager):
    ClassName=ClassificationItemInfoTable

class   ClassificationFilterDBManager(DBManager):
    ClassName=ClassificationItemInfoTable

class   ClassificationDetailDBManager(DBManager):
    ClassName=CreateView



if __name__ == "__main__":


    # oid=ClassificationItemInfoTableDBManager.create(name="123",desc="1234",csi_oid=7)
    # print(oid)
    # params=BasicQueryParameter(page_size=3,page_index=1)
    # ClassificationItemInfoTableDBManager.list_view(params)
    # ClassificationItemInfoTableDBManager.view(13)
    # ClassificationStandardInfoDBManager.view(16)

    # ClassificationItemInfoTableDBManager.delete(10)
    # ClassificationItemInfoTableDBManager.update(7,name="Tom",desc="你猜猜")

    # ClassificationStandardInfoDBManager.create(name="我在测试",desc="1234")   
    # obj=FilterQueryParameter(page_size=100,page_index=0,csi_oid=1000,)
    # ClassificationFilterDBManager.filter_list_view(obj)
   """ ClassificationDetailDBManager.detail_view({
  "oid": 0,
  "name": "string",
  "desc": "string",
  "mapping_value": 0,
  "csi_oid": 1,
  "create_datetime": "string",
  "csi_name": "string"
})"""