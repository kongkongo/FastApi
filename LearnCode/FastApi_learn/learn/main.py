from    fastapi     import  FastAPI,Path,Body,HTTPException
from    typing      import  Optional
from fastapi.security.oauth2 import OAuth2PasswordRequestFormStrict
from    pydantic    import  BaseModel,Field, fields
from fastapi.param_functions import Depends, Query
from  fastapi.security  import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
import  uvicorn
import  pathlib
import  sys
import  traceback
try:
    _project_root = str(pathlib.Path(__file__).resolve().parents[1])
    sys.path.append(_project_root)
except Exception as e:
    traceback.print_exc()
from  learn.schema  import  User


app=FastAPI()

# @app.put("/items/{item_id}")
# # async   def    update_item(item_id:int,item:Item,user:User,importance:int=Body(...)):
# async   def    update_item(item_id:int,item:Item=Body(...,embed=True)):

#     results={"item_id":item_id,"item":item}
#     return  results

# # 多个请求体参数和查询参数
# @app.get("/items/{items_id}")
# async   def    read_items(*,items_id:int=Path(...,title="The ID of  the  item   to  get",gt=0,le=1000),
# q:str,
# size:float=Query(...,gt=0,lt=10.5)
# ):
#     results={"item_id":items_id}
#     if  q:
#         results.update({'q':q})
#     return  results

# @app.get("/items/")
# async   def  read_item(token:str=Depends(oauth2_schema)):
#     return  {"token":token}

# def fake_decode_token(token):
#     return  User(username=token+"fakedecoded",email="john@example.com",full_name="John  Doe")

# async   def   get_current_user(token:str=Depends(oauth2_schema)):
#     user=fake_decode_token(token)
#     return  user

# @app.get("/users/me")
# async   def read_user_me(current_user:User=Depends(get_current_user)):
#     return  current_user

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}
oauth2_schema=OAuth2PasswordBearer(tokenUrl="token")
def fake_hash_password(password:str):
    return  "fakehashed"+password

class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user
    
async def get_current_user(token: str = Depends(oauth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async   def get_current_active_user(current_user:User=Depends(get_current_user)):
    if  current_user.disabled:
        raise   HTTPException(status_code=400,detail="Inactive  user")
    return  current_user

@app.post("/token/")
async   def login(form_data:OAuth2PasswordRequestForm=Depends()):
    user_dict=fake_users_db.get(form_data.username)
    if  not user_dict:
        raise   HTTPException(status_code=400,detail="Incorrect  username   or  password")
    user=UserInDB(**user_dict)
    hashed_password=fake_hash_password(form_data.password)
    if  not hashed_password==user.hashed_password:
        raise   HTTPException(status_code=400,detail="Incorrect username    or  password")
    return  {"acess_token":user.username,"token_type":"bearer"}

@app.get("/users/me")
async   def read_user_me(current_user:User=Depends(get_current_active_user)):
    return  current_user
if  "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)