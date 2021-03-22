import  pathlib
import  sys
import  traceback
from fastapi.exceptions import RequestValidationError
from starlette.applications import Starlette
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
try:
    _project_root = str(pathlib.Path(__file__).resolve().parents[1])
    sys.path.append(_project_root)
except Exception as e:
    traceback.print_exc()
    
from    fastapi import  FastAPI,HTTPException
from   learn.schema    import  UnicornException,Item
import  uvicorn

app=FastAPI()

items={"foo":"The   Foo     Wrestlers"}
# @app.get("/items/{item_id}")
# async   def    read_item(item_id:str):
#     if  item_id   not   in    items:
#         raise   HTTPException(status_code=404,detail="Item  not found",headers={"X-Error":"There    goes    my  error"})
#     return  {"item":items[item_id]}

@app.exception_handler(UnicornException)
async   def    unicorn_exception_handler(request:Request,exc:UnicornException):
    return  JSONResponse(
        status_code=418,
        content={"message":f"Oop!{exc.name} did something.There goes   a    rainbow..."}
    )
@app.exception_handler(StarletteHTTPException)
async   def http_exception_handler(request,exc):
    return  PlainTextResponse(str(exc.detail),status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async   def validation_exception_handler(request,exc):
    return  PlainTextResponse(str(exc),status_code=400)

@app.get("/items/{item_id}")
async   def  read_item(item_id:int):
    if  item_id==3:
        raise   HTTPException(status_code=418,detail="Nope! I   don't   like    3.")
    return  {"item_id":item_id}
@app.get("/unicorns/{name}")
async   def  read_unicorn(name:str):
    if  name =="yolo":
        raise   UnicornException(name=name)
    return  {"unicorn_name":name}

if  "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)