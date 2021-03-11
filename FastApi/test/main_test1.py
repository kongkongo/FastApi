from    typing  import  List,Dict
from    datetime    import  date
from fastapi import FastAPI,Form,Query
from    typing      import      Optional,Union
from  pydantic  import  BaseModel,EmailStr

app=FastAPI()

def     main(user_id:str):
    return  user_id

#A  Pydantic    model
# class   User(BaseModel):
#     id:int
#     name:str
#     joined:date

# my_user:User = User(id=3,name="John Doe",joined="2018-07-19")

# second_user_data={
#     "id":4,
#     "name":"Mary",
#     "joined":"2018-11-30",
# }

# my_second_user:User=User(**second_user_data)


# def process_items(prices:Dict[str,float]):
#     for item_name,item_price    in  prices.items():
#         print(item_name)
#         print(item_price)

# class   Person:
#     def __init__(self,name:str) :
#         self.name=name

# def get_person_name(one_person:Person):
#     return  one_person.name


# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}

# #查询参数
# fake_items_db=[{'item_name':'foo'},{'item_name':'Bar'},{'item_name':'Baz'}]
# # @app.get('/items/')
# # async   def  read_item(skip:int=0,limit:int=10):
# #     return  fake_items_db[skip:skip+limit]
# @app.get("/items/{item_id}")
# # async def read_item(item_id: str, q: Optional[str] = None):
# #     if q:
# #         return {"item_id": item_id, "q": q}
# #     return {"item_id": item_id}
# async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item

# #多个参数
# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(
#     user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
# ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item

# #必须参数（由于 needy 是必需参数，因此你需要在 URL 中设置它的值：否则会报错）
# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item


# #请求体

# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None

# @app.post("/items/")
# # async def create_item(item: Item):
# #     return item
 
#  #使用模型
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# #请求体+路径参数
# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}

# @app.get("/items/")
# async def read_items(q: Optional[str] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
# async def read_items(q: Optional[str] = Query(None, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


#响应模型，添加输出模型
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user

#响应模型编码参数
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: float = 10.5
#     tags: List[str] = []


# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }

# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: str):
#     return items[item_id]

    #Union 或者 anyOf

# class BaseItem(BaseModel):
#     description: str
#     type: str


# class CarItem(BaseItem):
#     type = "car"


# class PlaneItem(BaseItem):
#     type = "plane"
#     size: int


# items = {
#     "item1": {"description": "All my friends drive a low rider", "type": "car"},
#     "item2": {
#         "description": "Music is my aeroplane, it's my aeroplane",
#         "type": "plane",
#         "size": 5,
#     },
# }


# @app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
# async def read_item(item_id: str):
#     return items[item_id]

#模型列表
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

#formdata

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

#文件操作
from  fastapi   import  File,UploadFile
from fastapi.responses import HTMLResponse

# @app.post("/files/")
# async   def  create_file(file: bytes=File(...)):
#     return  {"file_size":len(file)}

# @app.post("/uploadfile/")
# async   def create_upload_file(file:UploadFile=File(...)):
#     return  {"filename":file.filename}

#多文件上传
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}

# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}

# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)

@app.post("/files/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

#响应错误信息
#进口 HTTPException

from    fastapi import HTTPException

items={"foo":"The   Foo Wrestlers"}

@app.get("/items/{item_id}")
async   def     read_item(item_id):
        if  item_id not in  items:
            raise   HTTPException(status_code=404,detail="Items not found")
        return  {"item":items[item_id]}

@app.get("/items-header/{item_id}")
async   def  read_item_header(item_id:str):
    if  item_id   not   in  items:
        raise   HTTPException(
                    status_code=404,
                    detail="Item    not     found",
                    headers={"X-Error":"There   goes    my  errors"},
    )
    return  {'item':items[item_id]}