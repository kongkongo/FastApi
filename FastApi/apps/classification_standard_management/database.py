from typing import List
# from database import Database
# import  databases
import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean, Text, Date, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import  pymysql
pymysql.install_as_MySQLdb()

from contextlib import contextmanager
from fastapi import FastAPI
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "mysql://root:root@127.0.0.1:3306/Test"
POOL_SIZE=3

# DATABASE_URL = "postgresql://user:password@postgresserver/db"

# database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String(255)),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

engine = sqlalchemy.create_engine(    
   DATABASE_URL,
    encoding='utf8', 
    pool_size=POOL_SIZE
 )

# engine = sqlalchemy.create_engine(
#     DATABASE_URL
# )
metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Base = declarative_base()

        
