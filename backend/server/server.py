from fastapi import FastAPI,Request,Response,HTTPException,Query,Cookie,Header
from backend.server.model import *
from backend.common import common
from backend.server.manager import Manager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from backend.translate_server.api import TranslateAPI


GetToken = Header
user_manger : Manager = None
translate_api : TranslateAPI = None
async def init():
    global user_manger,translate_api
    user_manger = Manager()
    await user_manger.init()
    translate_api = TranslateAPI()
    translate_api.start()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


unauthorized_resonse = {401 : {"model" : str, "description" : "Unauthorized"}}
auto_set_token = True

@app.get("/")
async def root():
    return {"message" : "Konnichiwa Sekai!"}

@app.post('/guest',tags=['Authentication'])
async def guest_entry() -> LoginResponse:
    if (True):
        token = user_manger.add_guest()
        response = LoginResponse(success=True,token=token)
        if (auto_set_token):
            response = Response(content=response.model_dump_json())
            response.set_cookie(key='Token',value=token)
            return response
        else:
            return response
    
@app.post('/login',tags=['Authentication'])
async def users_login(
    data : LoginRequest
) -> LoginResponse:
    token = user_manger.login(
        username=data.username,
        password=data.password
    )
    if (token):
        response = LoginResponse(success=True,token=token)
        if (auto_set_token):
            response = Response(content=response.model_dump_json())
            # response.set_cookie(key='Token',value=token,samesite='none')
            return response
        else:
            return response
    else:
        response = LoginResponse(success=False,token='')
        return response

@app.post('/register',tags=['Authentication'])
async def users_register(
    data : RegisterRequest
) -> LoginResponse:
    token = user_manger.add_user(
        username=data.username,
        password=data.password,
        email=data.email
    )
    if (token != None):
        response = LoginResponse(success=True,token=token)
        return response
    else:
        response = LoginResponse(success=False,token='')
        return response
    
@app.get('/history',tags=['Record'],responses=unauthorized_resonse)
async def get_history(
    start_from : int = Query(gt=-1,lt=1000),
    amount : int = Query(gt=-1,lt=1000),
    token : str = GetToken(None)
) -> list[TranslateRecord]:
    validation = user_manger.guest_validate(token)
    if (validation):
        result = user_manger.get_history(token,start_from,amount)
        return result
    else:
        raise HTTPException(status_code=401)
    
@app.get('/saved',tags=['Record'],responses=unauthorized_resonse)
async def get_saved(
    start_from : int = Query(gt=-1,lt=1000),
    amount : int = Query(gt=-1,lt=1000),
    token : str = GetToken(None)
) -> list[TranslateRecord]:
    validation = user_manger.validate(token)
    if (validation):
        result = user_manger.get_saved(token,start_from,amount)
        return result
    else:
        raise HTTPException(status_code=401)
    
@app.post('/save',tags=['Record'],responses=unauthorized_resonse)
async def save_record(
    request : Request,
    data : TranslateRecord,
    token : str = GetToken(None)
):
    validation = user_manger.validate(token)
    if (validation):
        user_manger.save(token,data.model_dump())
        response = Response(status_code=200)
        return response
    else:
        raise HTTPException(status_code=401)

@app.post('/translate/text',tags=['Translate'],responses=unauthorized_resonse)
async def translate_test(
    data : TranslationRequest,
    token : str = GetToken(None)
) -> TranslationResponse:
    validation = user_manger.guest_validate(token)
    if (validation):
        result = await user_manger.translate_text(token,data.model_dump())
        response = TranslationResponse(to_content=result)
        return response
    else:
        raise HTTPException(status_code=401)
    
app.add_event_handler('startup',init)    

def start():
    config = common.get_config('server')
    uvicorn.run(app,host=config['host'],port=config['port'])

async def async_start():
    config = common.get_config('server')
    server_config = uvicorn.Config(app,host=config['host'],port=config['port'])
    server = uvicorn.Server(server_config)
    await server.serve()