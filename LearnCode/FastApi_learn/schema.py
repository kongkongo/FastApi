from    typing      import  List,Optional,Set
from    pydantic    import  BaseModel,Field
from enum import Enum
from pydantic.networks import EmailStr, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags:List[str]=[]
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

class   Offer(BaseModel):
    name:str
    description:Optional[str]=None
    price:float
    items:List[Item]


class   UserIn(BaseModel):
    username:str
    password:str
    email:EmailStr
    full_name:Optional[str]=None

class   UserOut(BaseModel):
    username:str
    email:EmailStr
    full_name:Optional[str]=None


class   PageInfo(BaseModel):
    """
    list    信息，浏览某一页，这个页面的大小
    """
    page_index:int=0
    page_size:int=50    #默认值
