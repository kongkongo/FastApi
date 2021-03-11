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
from apps.classification_standard_management.curd import ClassificationDetailDBManager, ClassificationItemInfoTableDBManager,ClassificationStandardInfoDBManager
from basic.schemas import BasicQueryParameter,FilterQueryParameter


app=FastAPI()


@app.post("/classification_detail_view/list/",response_model=List[schemas.ClassificationDetailView])
def list_view_cii(data:schemas.ClassificationDetailView):
    try:        
        #print(data.dict())        
        ans_list=[]        
        cii_obj_list=ClassificationDetailDBManager.detail_view(data)    
        
        csi_info_obj=ClassificationDetailDBManager.detail_filter_view(data)
        # print(csi_info_obj)      
        for  csi_info   in  csi_info_obj: 
            csi_info=csi_info.jsonify()   
            print(csi_info)
            if csi_info:                
                csi_info["create_datetime"]=csi_info["create_datetime"].strftime("%Y-%m-%d_%H:%M:%S")            
                ans_list.append(                    
                    schemas.ClassificationDetailView(**csi_info)                
                    ) 
        # print(ans_list)       
        return ans_list
    except Exception:        
        traceback.print_exc()        
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "异常 error"})





if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)