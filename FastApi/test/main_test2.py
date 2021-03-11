# # from fastapi import FastAPI, Request
# # from fastapi.responses import JSONResponse
# # from fastapi import FastAPI, HTTPException
# # from fastapi.exceptions import RequestValidationError
# # from fastapi.responses import PlainTextResponse
# # from starlette.exceptions import HTTPException as StarletteHTTPException


# # class UnicornException(Exception):
# #     def __init__(self, name: str):
# #         self.name = name


# # app = FastAPI()


# # # @app.exception_handler(UnicornException)
# # # async def unicorn_exception_handler(request: Request, exc: UnicornException):
# # #     return JSONResponse(
# # #         status_code=418,
# # #         content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
# # #     )


# # # @app.get("/unicorns/{name}")
# # # async def read_unicorn(name: str):
# # #     if name == "yolo":
# # #         raise UnicornException(name=name)
# # #     return {"unicorn_name": name}

# # @app.exception_handler(StarletteHTTPException)
# # async def http_exception_handler(request, exc):
# #     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


# # @app.exception_handler(RequestValidationError)
# # async def validation_exception_handler(request, exc):
# #     return PlainTextResponse(str(exc), status_code=400)


# # @app.get("/items/{item_id}")
# # async def read_item(item_id: int):
# #     if item_id == 3:
# #         raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
# #     return {"item_id": item_id}

# #     #响应状态码
# # from typing import Optional, Set
# # from fastapi import FastAPI, status
# # from pydantic import BaseModel

# # # class Item(BaseModel):
# # #     name: str
# # #     description: Optional[str] = None
# # #     price: float
# # #     tax: Optional[float] = None
# # #     tags: Set[str] = []


# # # @app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
# # # async def create_item(item: Item):
# # #     return item

# # # 来自文档字符串的描述
# # class Item(BaseModel):
# #     name: str
# #     description: Optional[str] = None
# #     price: float
# #     tax: Optional[float] = None
# #     tags: Set[str] = []


# # @app.post("/items/", response_model=Item, summary="Create an item")
# # async def create_item(item: Item):
# #     """
# #     Create an item with all the information:

# #     - **name**: each item must have a name
# #     - **description**: a long description
# #     - **price**: required
# #     - **tax**: if the item doesn't have tax, you can omit this
# #     - **tags**: a set of unique tag strings for this item
# #     """
# #     return item
# from datetime import datetime
# from typing import Optional

# from fastapi import FastAPI
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel

# fake_db = {}


# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: Optional[str] = None


# app = FastAPI()


# @app.put("/items/{id}")
# def update_item(id: str, item: Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data

#PUT更新
from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded