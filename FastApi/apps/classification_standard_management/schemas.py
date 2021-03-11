from    typing      import  List,Optional
from    pydantic    import  BaseModel
from enum import Enum

from sqlalchemy.sql.expression import desc




class   ClassificationDetailView(BaseModel):
    """
     多条件查询视图
    """
    name:str
    desc:str=""
    mapping_value:int
    csi_oid:int
    create_datetime:str
    csi_name:str


class CreateClassificationStandardInfoEntity(BaseModel):
    """
    创建分类标注集
    """
    name: str # 数据集合名称
    desc: str="" # 数据集合描述

class   ClassificationStandardInfoEntity(BaseModel):
    """
    数据集信息
    """
    oid:int #数据集id
    create_datetime:str

class   UpdateClassificationStandardInfoEntity(CreateClassificationStandardInfoEntity):
    """
    更新分类标注集
    """
    oid: int # 数据集id.


class   DeleteClassificationStandardInfoEntity(CreateClassificationStandardInfoEntity):
    """
    删除分类标注集
    """
    oid: int # 数据集id.



#---
class CreateClassificationItemInfoEntity(BaseModel):
    """
    [
        创建分类名称
    ]

    Args:
        BaseModel ([type]): [description]

    Returns:
        [type]: [description]
    """
    name:str 
    desc:str 
    csi_oid:int

class   ClassificationItemInfoEntity(BaseModel):
    """
        [
            分类名称信息
        ]

        Args:
            BaseModel ([type]): [description]

        Returns:
            [type]: [description]
    """
    oid:int
    create_datetime:str


class   DeleteClassificationItemInfoEntity(CreateClassificationItemInfoEntity):
    """
    [删除分类]
    """
    oid:int        #分类标准oid

class UpdateClassificationItemInfoEntity(CreateClassificationItemInfoEntity):
    """
    [更新分类名称]
    """
    oid:int     #分类标准oid


