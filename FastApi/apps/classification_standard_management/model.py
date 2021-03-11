# -*- coding: utf-8 -*-
'''
    desc: 数据库模型定义
    author: liukun
    date: 2021-02-23
'''

import pathlib
import sys
_project_root = str(pathlib.Path(__file__).resolve().parents[2])
sys.path.append(_project_root)
from datetime import datetime
from server import database
from server.database import Base
from sqlalchemy.types import String, Integer, Boolean, Text, Date, DateTime, Float
from sqlalchemy.schema import Column
from sqlalchemy import Table
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement

class  CreateView(Base):
    __tablename__='cii_detail_view'
    oid = Column('oid', Integer, primary_key=True)
    name = Column('name', String(128, collation='utf8mb4_bin'))
    desc = Column('desc', String(256, collation='utf8mb4_bin'))
    create_datetime= Column('create_datetime', DateTime, default=datetime.now) # 任务创建时间
    mapping_value=Column('mapping_value', Integer, default=0) 
    csi_oid = Column('csi_oid', Integer) # 关联ClassificationStandardInfoTable 的oid
    csi_name=Column("csi_name",String(128,collation='utf8mb4_bin'))

    def jsonify(self):
        return {
            'oid':self.oid,
            'name':self.name,
            'desc':self.desc,
            'create_datetime':self.create_datetime,
            'mapping_value':self.mapping_value,
            'csi_oid':self.csi_oid,
            'csi_name':self.csi_name
        }


class ClassificationStandardInfoTable(Base):
    __tablename__ = 'classification_standard_info_table'

    oid = Column('oid', Integer, primary_key=True)
    name = Column('name', String(128, collation='utf8mb4_bin'))
    desc = Column('desc', String(256, collation='utf8mb4_bin'))
    create_datetime= Column('create_datetime', DateTime, default=datetime.now) # 任务创建时间
    

    def jsonify(self):
        return {
            'oid':self.oid,
            'name':self.name,
            'desc':self.desc,
            'create_datetime':self.create_datetime
        }

class ClassificationItemInfoTable(Base):
    __tablename__ = 'classification_item_info_table'
    oid = Column('oid', Integer, primary_key=True)
    name = Column('name', String(128, collation='utf8mb4_bin'))
    desc = Column('desc', String(256, collation='utf8mb4_bin'))
    mapping_value=Column('mapping_value', Integer, default=0)
    csi_oid = Column('csi_oid', Integer) # 关联ClassificationStandardInfoTable 的oid
    create_datetime= Column('create_datetime', DateTime, default=datetime.now) # 任务创建时间


    def jsonify(self):
        return {
            'oid':self.oid,
            'name':self.name,
            'desc':self.desc,
            'csi_oid':self.csi_oid,
            'create_datetime':self.create_datetime,
             'mapping_value': self.mapping_value

        }

if __name__ == "__main__":
    Base.metadata.create_all(database.engine)
    x="你好机器学习"
    y="你好北京"
    with database.db_session() as db: 
        obj=ClassificationStandardInfoTable(name="你好机器学习",desc="你好北京")
        db.add(obj)
        db.commit()
        obj= ClassificationItemInfoTable(name="你好机器学习",desc="你好北京",csi_oid=obj.oid)
        db.add(obj)
        db.commit()

    

