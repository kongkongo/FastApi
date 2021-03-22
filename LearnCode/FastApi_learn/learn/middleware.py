import  time
from   fastapi  import  FastAPI,Request, responses
from    fastapi.middleware.cors import  CORSMiddleware

import  uvicorn

app=FastAPI()

@app.middleware("http")
async   def add_process_time_header(request:Request,call_next):
    start_time=time.time()
    response=await  call_next(request)
    process_time=time.time()-start_time
    response.headers["X-Process-Time"]=str(process_time)
    return  response

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async   def main():
    return  {"message":"Hello   world"}



if  "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)