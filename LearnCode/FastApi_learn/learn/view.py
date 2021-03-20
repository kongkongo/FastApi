from typing import List, Optional, Set
from fastapi import FastAPI,Cookie,Header
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
from    FastApi_learn.learn.schema    import  Item,Image,UserIn,UserOut

app = FastAPI()



# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item=Body(...,
# example={"name":"Foo","description":"A very    nice    Item","price":35.4,"tax":3.2})):     
# # Body 额外参数
#     results = {"item_id": item_id, "item": item}
#     return results

@app.post("/images/multiple/")
async   def     create_multiple_images(images:List[Image]):
    return  images

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
@app.get("/items/header")
# async   def    read_header(user_agent:Optional[str]=Header(None)):
    # 自动转换
# async   def     read_header(strange_header:Optional[str]=Header(None,convert_underscores=False)):
        # return  {"strange_header":strange_header}
# 重复的headers
async   def     read_header(x_token:Optional[List[str]]=Header(None)):
    return  {"x-Token   values":x_token}


# 响应模型
@app.post("/items/",response_model=Item)
async   def create_item(item:Item):
    return  item


# 返回与输入相同的数据
@app.post("/user/create_user",response_model=UserIn)
async   def    create_user(user:UserIn):
    return  user

# 添加输出模型
@app.post("/user/",response_model=UserOut)
async   def     create_user(user:UserIn):
    return  user

# 使用 response_model_exclude_unset 参数
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}
@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]
# @app.get("items/{item_id}",response_model=Item,response_model_exclude_unset=True)
# async   def read_item(item_id:str):
#     return  items[item_id]
@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]



if  "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
