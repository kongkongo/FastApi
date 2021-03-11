from    typing      import      Optional
from    fastapi     import      FastAPI,Query
from    pydantic    import      BaseModel

app=FastAPI()

class   Item(BaseModel):
    name:str
    price:float
    is_offer:Optional[bool]=None


@app.get("/")
def     home():
    return  {"Hello":"World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get('/user')
async   def     user(
    *,
    user_id:int=Query(...,title="The    ID  of    the   user    to     get",gt=0)
):
 return     {"user_id":user_id }

 #示例升级
 #PUT请求
@app.put("/items/{item_id}")
def     update_item(item_id:int,item:Item):
    return     {"item_name":item.name,"item_price":item.price,",item_id":item_id}

@app.post('/user/update')
async   def   update_user(
    *,
    user_id:int,
    really_update:int =Query(...)
    ):
    pass
