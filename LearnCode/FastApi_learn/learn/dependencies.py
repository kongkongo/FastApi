from typing import Optional
from fastapi import Depends, FastAPI,HTTPException
from fastapi.param_functions import Cookie, Header
import  uvicorn
import  pathlib
import  sys
import  traceback
try:
    _project_root = str(pathlib.Path(__file__).resolve().parents[1])
    sys.path.append(_project_root)
except Exception as e:
    traceback.print_exc()
from  learn.schema  import  CommonQueryParams

# app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):

    return {"q": q, "skip": skip, "limit": limit}


# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons

# @app.get("/users/")
# async def read_users(commons: dict = Depends(common_parameters)):
#     return commons

# @app.get("/items/")
# async   def   read_item(commons=Depends(CommonQueryParams)):
#     response={}
#     if  commons.q:
#         response.update({"q":commons.q})
#     items=fake_items_db[commons.skip:commons.skip+commons.limit]
#     response.update({"items":items})
#     return  response

# def query_extractor(q:Optional[str]=None):
#     return  q
# def query_or_cookie_extractor(q:str=Depends(query_extractor),last_query:Optional[str]=Cookie(None)):
#     if  not q:
#         return  last_query
#     return  q

# @app.get("/items/")
# async   def    read_query(query_or_default:str=Depends(query_or_cookie_extractor)):
#     return  {"q_or_cookie":query_or_default}

async   def verify_token(x_token:str=Header(...)):
    if  x_token!="fake-super-secret-token":
        raise   HTTPException(status_code=400,detail="X-Token   header  invalid")

async   def verify_key(x_key:str=Header(...)):
    if  x_key!="fake-super-secret-key":
        raise   HTTPException(status_code=400,detail="X-Key header  invaild")
    return  x_key

app=FastAPI(dependencies=[Depends(verify_key),Depends(verify_token)])

# @app.get("/items/",dependencies=[Depends(verify_token),Depends(verify_key)])
# async   def read_items():
#     return  [{"item":"Foo"},{"item":"Bar"}]

@app.get("/items/")
async   def read_items():
    return  [{"item":"Portal    Gun"},{"item":"Plumbus"}]
@app.get("/users/")
async   def read_users():
    return  [{"username":"Rick"},{"username":"Morty"}]


async   def get_db():
    db=DBSession()
    try:
        yield   db
    finally:
        db.close()

if  "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)