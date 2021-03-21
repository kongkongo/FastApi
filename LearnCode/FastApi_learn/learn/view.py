from typing import List, Optional, Set, Union,Dict
from fastapi import FastAPI,Cookie,Header,Form,File,UploadFile
from fastapi.params import Body
from pydantic import BaseModel
from pydantic.networks import HttpUrl
from    datetime    import  datetime,time,timedelta
from    uuid    import  UUID
import  uvicorn 

import  pathlib
import  sys
import  traceback
try:
    _project_root = str(pathlib.Path(__file__).resolve().parents[2])
    sys.path.append(_project_root)
except Exception as e:
    traceback.print_exc()
from    FastApi_learn.learn.schema    import  Item,Image,UserIn,UserOut,UserInDB,PlaneItem,CarItem

app = FastAPI()



# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item=Body(...,
# example={"name":"Foo","description":"A very    nice    Item","price":35.4,"tax":3.2})):     
# # Body 额外参数
#     results = {"item_id": item_id, "item": item}
#     return results

# @app.post("/images/multiple/")
# async   def     create_multiple_images(images:List[Image]):
#     return  images

# 额外数据类型
@app.put("/items/datatype/{item_id}")
async   def    read_items(
        item_id:UUID,
        start_datetime:Optional[datetime]=Body(None),
        end_datetime:Optional[datetime]=Body(None),
        repeat_at:Optional[time]=Body(None),
        process_after:Optional[timedelta]=Body(None)
):
        start_process=start_datetime+process_after
        duration=end_datetime-start_process
        return  {
            "item_id":item_id,
            "start_datetime":start_datetime,
            "end_datetime":end_datetime,
            "repeat_at":repeat_at,
            "process_after":process_after,
            "start_process":start_process,
            "duration":duration
        }

# 导入 Cookie,声明 Cookie 参数
@app.get("/items/cookie")
async   def    read_cookie(ads_id:Optional[str]=Cookie(None)):
    return  {"ads_id":ads_id}

# Header 参数,导入 Header
# @app.get("/items/header")
# async   def    read_header(user_agent:Optional[str]=Header(None)):
    # 自动转换
# async   def     read_header(strange_header:Optional[str]=Header(None,convert_underscores=False)):
        # return  {"strange_header":strange_header}
# 重复的headers
# async   def     read_header(x_token:Optional[List[str]]=Header(None)):
#     return  {"x-Token   values":x_token}


# 响应模型
# @app.post("/items/",response_model=Item)
# async   def create_item(item:Item):
#     return  item


# 返回与输入相同的数据
# @app.post("/user/create_user",response_model=UserIn)
# async   def    create_user(user:UserIn):
#     return  user

# 添加输出模型
# @app.post("/user/",response_model=UserOut)
# async   def     create_user(user:UserIn):
#     return  user

# 使用 response_model_exclude_unset 参数
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
#     "baz": {
#         "name": "Baz",
#         "description": "There goes my baz",
#         "price": 50.2,
#         "tax": 10.5,
#     },
# }
# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name", "description"},
# )
# async def read_item_name(item_id: str):
#     return items[item_id]
# # @app.get("items/{item_id}",response_model=Item,response_model_exclude_unset=True)
# # async   def read_item(item_id:str):
# #     return  items[item_id]
# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
# async def read_item_public_data(item_id: str):
#     return items[item_id]


# def fake_password_hasher(raw_password:str):
#     return  "superscrect"+raw_password
# def fake_save_user(user_in:UserIn):
#     hashed_password=fake_password_hasher(user_in.password)
#     user_in_db=UserInDB(**user_in.dict(),hashed_password=hashed_password)
#     print("User saved!  ..not   really")
#     return    user_in_db

# @app.post("/user/",response_model=UserOut)
# async   def     create_user(user_in:UserIn):
#     user_saved=fake_save_user(user_in)
#     return  user_saved


# items={
#     "item1": {"description": "All my friends drive a low rider", "type": "car"},
#     "item2": {"description": "Music is my aeroplane, it's my aeroplane","type": "plane","size": 5,}
#     }
# @app.get("/items/{item_id}",response_model=Union[PlaneItem,CarItem])
# async  def  read_item(item_id:str):
#     return  items[item_id]
# 模型列表
# items = [
#     {"name": "Foo", "description": "There comes my hero"},
#     {"name": "Red", "description": "It's my aeroplane"},
# ]
# @app.get("/items/",response_model=List[Item])
# async   def    read_items():
#     return  items

# 任意 dict 构成的响应
@app.get("/keyword-weights/",response_model=Dict[str,float])
async   def     read_keyword_weights():
    return  {"foo":2.3,"bar":6.6}

@app.post("/login/")
async   def   login(username:str=Form(...),password:str=Form(...)):
    return  {"username":username}

@app.post("/files/")
async   def create_file(file:bytes=File(...)):
    return  {"file_size":len(file)}
@app.post("/uploadfile/")
async   def create_upload_file(file:UploadFile=File(...)):
    return  {"filename":file.filename}


if  "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
