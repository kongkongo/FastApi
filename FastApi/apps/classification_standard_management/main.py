import traceback
import pathlib
import sys
import  time
from pydantic.main import BaseModel

from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
try:
    _project_root = str(pathlib.Path(__file__).resolve().parents[2])
    sys.path.append(_project_root)
except Exception as e:
    traceback.print_exc()
from typing import Dict,List
import uvicorn


from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from fastapi import FastAPI, BackgroundTasks,Body, Depends
from fastapi import File, UploadFile, status
from fastapi.responses import FileResponse, Response, StreamingResponse
from apps.classification_standard_management import schemas
from apps.classification_standard_management.curd import ClassificationDetailDBManager, ClassificationFilterDBManager, ClassificationItemInfoTableDBManager,ClassificationStandardInfoDBManager
from basic.schemas import BasicQueryParameter,FilterQueryParameter


app=FastAPI()

@app.post("/classification_standard_info/create/",response_model=Dict)
def    create_cil(data:schemas.CreateClassificationStandardInfoEntity):
    """
    添加分类标准
    """
    try:
        ClassificationStandardInfoDBManager.create(**dict(data))
        result={
            "num":1,
        }
        return  result
    except  Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})
@app.delete("/classification_standard_info/delete/{oid}/",status_code=HTTP_200_OK)
def    delete_cil(oid:int):
    try:
        entity=ClassificationStandardInfoDBManager.delete(oid)
        if  entity:
            result={"status":1} 
            return  result
    except  Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})

@app.post("/classification_standard_info/update/",status_code=HTTP_200_OK)
def     update_cil(data:schemas.ClassificationStandardInfoEntity):
    try:
        oid=data.oid
        # print(oid)
        data_info=dict(data)
        del data_info['oid']
        # print(data_info)
        entity=ClassificationStandardInfoDBManager.update(oid,**data_info)
        if  entity:
            return  {"status":"ok"}
    except  Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})

@app.get("/classification_standard_info/list/{oid}/",response_model=schemas.ClassificationStandardInfoEntity)
def list_csi(oid:int):
    try:
        entity=ClassificationStandardInfoDBManager.view(oid)
        if entity :
            dict_info=entity.jsonify()
            dict_info["create_datetime"]=dict_info["create_datetime"].strftime("%Y-%m-%d_%H:%M:%S")
            return schemas.ClassificationStandardInfoEntity(**dict_info)
        return None
    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "异常 error"})

@app.post("/classification_standard_info/list_view/",response_model=List[schemas.ClassificationStandardInfoEntity])
def list_view_standard(pageinfo:BasicQueryParameter):
     try:
        #print(data.dict())
        ans_list=[]
        cii_obj_list=ClassificationStandardInfoDBManager.list_view(pageinfo)
        for cii_obj in cii_obj_list:
            dict_info=cii_obj.jsonify()
            dict_info["create_datetime"]=dict_info["create_datetime"].strftime("%Y-%m-%d_%H:%M:%S")
            ans_list.append(
                schemas.ClassificationStandardInfoEntity(**dict_info)
            )
        return ans_list
     except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "异常 error"})


@app.post("/classification_item_info/create/",response_model=Dict)
def  create_cil(data:schemas.CreateClassificationStandardInfoEntity):
    try:
        # print(data.dict())
        ClassificationItemInfoTableDBManager.create(**dict(data))
        result={
            "num":1,
        }
        return  result
    except  Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify error"})

@app.get("/classification_item_info/list/{oid}/",response_model=schemas.ClassificationItemInfoEntity)
def  view_cil(oid:int):
    """
    查看类别信息
    """
    try:
        entity=ClassificationItemInfoTableDBManager.view(oid)
        if  entity:
            dict_info=entity.jsonify()
            dict_info["create_datetime"]=dict_info["create_datetime"].strftime("%Y-%m-%d_%H:%M:%S")
            return  schemas.ClassificationItemInfoEntity(**dict_info)
        return  None
    except  Exception:
        traceback.print_exc() 
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})

@app.post("/classification_item_info/list_view/",response_model=List[schemas.ClassificationItemInfoEntity])
def list_view_cii(pageinfo:BasicQueryParameter):
    try:
        #print(data.dict())
        ans_list=[]
        cii_obj_list=ClassificationItemInfoTableDBManager.list_view(pageinfo)
        print(cii_obj_list)
        for cii_obj in cii_obj_list:
            dict_info=cii_obj.jsonify()
            dict_info['create_datetime']=dict_info["create_datetime"].strftime("%Y-%m-%d_%H:%M:%S")
            ans_list.append(
                # schemas.ClassificationItemInfoEntity(cii_obj.jsonify())
                schemas.ClassificationItemInfoEntity(**dict_info)
            )
        return ans_list

    except Exception:
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "异常 error"})

@app.delete("/classification_item_info/delete/{oid}/",status_code=HTTP_200_OK)
def delete_cil(oid:int):
    """
    删除类别信息
    """
    try:
        entity=ClassificationItemInfoTableDBManager.delete(oid)
        if  entity:
            result={"status":1}
            return  result
    except  Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})

@app.post("/classification_item_info/update/",status_code=HTTP_200_OK)
def update_cil(data:schemas.ClassificationItemInfoEntity):
    """
    [更改类别信息]
    """
    # print(data)
    try:
        oid=data.oid
        # print(oid)
        # print(type(data))
        data_info=dict(data)
        # print(type(data_info))
        print(data_info)
        del data_info['oid']
        print(data_info)
        entity=ClassificationItemInfoTableDBManager.update(oid,**data_info)
        if  entity:
            # return  schemas.ClassificationItemInfoEntity
            return {"status":"ok"}
    except Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})

@app.post("/classification_filter_list_view/filterlist/",status_code=HTTP_200_OK)
def filter(data:FilterQueryParameter):
     try:
        entity=ClassificationItemInfoTableDBManager.filter_list_view(data)
        if  entity:
            return  entity
     except Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})

@app.post("/classification_detail_view/list/",status_code=HTTP_200_OK)
def filter(data:schemas.ClassificationDetailView):
     try:
        # print(data)
        entity=ClassificationDetailDBManager.detail_view(data)
        if  entity:
            return  entity
     except Exception:
        traceback.print_exc()
        return  JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"classify    error"})





if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)