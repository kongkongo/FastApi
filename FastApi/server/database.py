
# -*- coding: utf-8 -*-
'''
    desc: 数据库操作。
    author: liukun
    date: 2020-04-05
'''
import sys
import pathlib
import os
_project_root =  os.path.dirname(
    os.path.dirname(
            os.path.realpath(__file__)
    )
)
sys.path.append(_project_root)
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean, Text, Date, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf import config
import json
from contextlib import contextmanager
from sqlalchemy.sql.schema import MetaData
_project_root = str(pathlib.Path(__file__).resolve().parents[1])
sys.path.append(_project_root)


DIALECT = config.mysqlConfiger.get_config_value(config_key_name="dialect")
DRIVER = config.mysqlConfiger.get_config_value(config_key_name="driver")
USER = config.mysqlConfiger.get_config_value(config_key_name="user")
PASSWORD = config.mysqlConfiger.get_config_value(config_key_name="password")
HOST = config.mysqlConfiger.get_config_value(config_key_name="host")
PORT = config.mysqlConfiger.get_config_value(config_key_name="port")
DBNAME = config.mysqlConfiger.get_config_value(config_key_name="dbname")
CHARSET = config.mysqlConfiger.get_config_value(config_key_name="charset")
POOL_SIZE = config.mysqlConfiger.get_config_value(config_key_name="pool_size")



SQLALCHEMY_DATABASE_URL = '{}+{}://{}:{}@{}:{}/{}?charset={}'.format(DIALECT, DRIVER, USER, PASSWORD, HOST, PORT, DBNAME, CHARSET) \
    if CHARSET else \
    '{}+{}://{}:{}@{}:{}/{}'.format(DIALECT, DRIVER, USER, PASSWORD, HOST, PORT, DBNAME)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf8', pool_size=POOL_SIZE
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()








class OriginTextDataTable(Base):
    __tablename__ = 'origin_text_data_table'

    oid = Column('oid', Integer, primary_key=True)
    data_oid = Column('data_oid', Integer, default=-1)
    text = Column('text', Text(collation='utf8mb4_bin'), default='null')
    dataset_id = Column('dataset_id', Integer, default=0) # 数据属于的数据集合

class TextVecTable(Base):
    __tablename__ = 'text_vec_table'
    oid = Column('oid', Integer, primary_key=True)
    data_oid = Column('data_oid', Integer, default=-1)
    vec = Column('vec', Text(collation='utf8mb4_bin'), default='null')
    vec_type = Column('vec_type', String(128, collation='utf8mb4_bin'), default='null')

class XIsCategoryTable(Base):
    __tablename__ = 'x_is_category_table'
    oid = Column('oid', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    data_oid = Column('data_oid', Integer, default=-1)
    category = Column('category', String(128, collation='utf8mb4_bin'), default='null')

class XIsNotCategoryTable(Base):
    __tablename__ = 'x_is_not_category_table'
    oid = Column('oid', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    data_oid = Column('data_oid', Integer, default=-1)
    category = Column('category', String(128, collation='utf8mb4_bin'), default='null')

class XUncertainCategoryTable(Base):
    __tablename__ = 'x_uncertain_category_table'
    oid = Column('oid', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    data_oid = Column('data_oid', Integer, default=-1)
    category = Column('category', String(128, collation='utf8mb4_bin'), default='null')
    prob = Column('prob', Float, default=0.0)
    category_from = Column('category_from', String(128, collation='utf8mb4_bin'), default='null')
    finished = Column('finished', Integer, default=0)
    judgment_type = Column('judgment_type', Integer, default=0)
    judgment_category = Column('judgment_category', String(128, collation='utf8mb4_bin'), default='null')

class BatchCategoryInfoTable(Base):
    __tablename__ = 'batch_category_info_table'
    category_id = Column('category_id', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    category = Column('category', String(128, collation='utf8mb4_bin'), default='null')
    category_mapping_id = Column('category_mapping_id', Integer, default=-1)
    category_desc = Column('category_desc', Text(collation='utf8mb4_bin'), default='null')

class RulePredictionOfResultsTable(Base):
    __tablename__ = 'rule_prediction_of_results_table'
    oid = Column('oid', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    model_id = Column('model_id', Integer, default=0)
    data_oid = Column('data_oid', Integer, default=-1)
    dataset_id = Column('dataset_id', Integer, default=0)
    category = Column('category', String(128, collation='utf8mb4_bin'), default='null')
    meta_info = Column('meta_info', Text(collation='utf8mb4_bin'), default='{}')

class MetricInfoTable(Base):
    __tablename__ = 'metric_info_table'
    oid = Column('oid', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    hai_id = Column('hai_id', Integer, default=0) # model_id or ai_id #规则id或者其他的数据的id.
    hai_type = Column('hai_type',  String(128, collation='utf8mb4_bin'), default='null')
    meta_info =  Column('meta_info', Text(collation='utf8mb4_bin'), default='{}')

import server
from sqlalchemy.orm.scoping import scoped_session
class AiPredictonOfResultsTable(Base):
    __tablename__ = 'ai_prediction_of_results_table'
    oid = Column('oid', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    ai_id = Column('ai_id', Integer, default=0)
    data_oid = Column('data_oid', Integer, default=-1)
    category = Column('category', String(128, collation='utf8mb4_bin'), default='null')
    meta_info =  Column('meta_info', Text(collation='utf8mb4_bin'), default='{}')

class BatchRegularInfoTable(Base):
    __tablename__ = 'batch_regular_info_table'
    regular_id = Column('regular_id', Integer, primary_key=True)
    batch_id = Column('batch_id', String(32, collation='utf8mb4_bin'), default='0')
    category_id = Column('category_id', Integer, default=-1)
    content = Column('content', Text(collation='utf8mb4_bin'), default='null')
    regular_type = Column('regular_type', String(16, collation='utf8mb4_bin'), default='null')

class BatchInfoTable(Base):
    __tablename__ = 'batch_info_table'
    batch_id = Column('batch_id', Integer, primary_key=True)
    batch_name = Column('batch_name', String(128, collation='utf8mb4_bin'), default='null')
    batch_desc = Column('batch_desc', Text(collation='utf8mb4_bin'), default='null')

class DataSetInfoTable(Base):
    """ 数据集合信息 """
    __tablename__ = 'dataset_info_table'
    oid = Column('oid', Integer, primary_key=True, autoincrement=True)
    data_oid = Column('data_oid', Integer, default=-1, autoincrement=True)
    dataset_name = Column('name', String(128, collation='utf8mb4_bin'), default='null')
    dataset_desc = Column('desc', Text(collation='utf8mb4_bin'), default='null')

class RulePredictTask(Base):
    """
    规则预测任务
    """
    __tablename__ = 'rule_predict_task_table'
    oid = Column('oid', Integer, primary_key=True, autoincrement=True)
    batch_id = Column('batch_id', Integer, default='0') # 关联的id
    dataset_id=  Column('dataset_id', Integer, default='0') # 关联的数据集id
    create_datetime= Column('create_datetime', DateTime, default=datetime.now) # 任务创建时间
    start_datetime= Column('start_datetime', DateTime,nullable=True) # 任务开始时间
    end_datetime= Column('end_datetime', DateTime,nullable=True) # 任务结束时间
    status = Column('status', String(32, collation='utf8mb4_bin'), default='init') # processing 执行




def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()



@contextmanager
def db_session(db_url=SQLALCHEMY_DATABASE_URL):
    """ Creates a context with an open SQLAlchemy session.
    """
    engine = create_engine(db_url, convert_unicode=True)
    connection = engine.connect()
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
    yield db_session
    db_session.close()
    connection.close()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    with engine.connect() as conn:
        rs=conn.execute("select count(*),category from  x_is_category_table group by category ")
        data=rs.fetchone()
        print(data['count(*)'],data['category'])
        
