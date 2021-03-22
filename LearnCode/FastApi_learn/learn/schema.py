from datetime import datetime
from    typing      import  List,Optional,Set
from    pydantic    import  BaseModel,Field
from enum import Enum
from pydantic.networks import EmailStr, HttpUrl
from    typing  import  Union

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    # tax: float = 10.5
    tax:Optional[float]=None
    # tags:List[str]=[]
    tags:Set[str]=[]
    # Field 的附加参数
    # name: str=Field(...,example="Foo")
    # description: Optional[str] = Field(None,example="A very nice   Item")
    # price: float=Field(...,example=35.4)
    # tax: Optional[float] = Field(None,example=3.2)
    # 使用 Config 和 schema_extra 为Pydantic模型声明一个示例
    # class   Config:
    #     schema_extra={
    #         "example":{
    #             "name":"Foo",
    #             "description":"A    very    nice    Item",
    #             "price":35.4,
    #             "tax":3.2,
    #         }
    #     }
    # tags: Set[str] = set()
    # images: Optional[List[Image]] = None

# class   Offer(BaseModel):
#     name:str
#     description:Optional[str]=None
#     price:float
#     items:List[Item]


class   UserBase(BaseModel):
    username:str
    # password:str
    email:EmailStr
    full_name:Optional[str]=None


class   UserIn(UserBase):
    # username:str
    password:str
    # email:EmailStr
    # full_name:Optional[str]=None

class   UserOut(UserBase):
    pass

class   UserInDB(UserBase):
    # username:str
    hashed_password:str
    # email:EmailStr
    # full_name:Optional[str]=None


# Union 或者 anyOf
class   BaseItem(BaseModel):
    description:str
    type:str
class   CarItem(BaseItem):
    type="car"
class   PlaneItem(BaseItem):
    type="plane"
    size:int

# class   Item(BaseModel):  
#     name:str
#     description:str

class   UnicornException(Exception):
    def __init__(self, name:str) :
        self.name=name


class   Item_Json(BaseModel):
    title:str
    timestamp:datetime
    description:Optional[str]=None


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

class   User(BaseModel):
    username:str
    email:Optional[str]=None
    full_name:Optional[str]=None
    disabled:Optional[bool]=None

class   UserInDB(User):
    hashed_password:str

