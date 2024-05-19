import asyncio
from fastapi import FastAPI,Request,Response,HTTPException,Query,Cookie,Header
from backend.server.model import *
from backend.common import common
from backend.server.manager import UserController
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from backend.translate_server.api import TranslateAPI


GetToken = Header
user_manger : UserController = None
translate_api : TranslateAPI = None
async def init():
    global user_manger,translate_api
    user_manger = UserController()
    user_manger.start()
    translate_api = TranslateAPI()
    translate_api.start()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://127.0.0.1:3000',
        'http://localhost:3000'
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


unauthorized_resonse = {401 : {"model" : str, "description" : "Unauthorized"}}
auto_set_token = True

@app.get("/")
async def root():
    return {"message" : "Konnichiwa Sekai!"}

@app.post('/entry',tags=['Authentication'])
async def guest_entry(
    token : str = GetToken(None)
) -> LoginResponse:
    if (True):
        if (token != None):
            validate = await user_manger.guest_validate(token)
            if (not validate):
                token = await user_manger.add_guest()
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
    token = await user_manger.login(data)
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
    data : RegisterRequest,
    token : str = GetToken(None)
) -> LoginResponse:
    token = await user_manger.register(data)
    if (token != None):
        response = LoginResponse(success=True,token=token)
        return response
    else:
        response = LoginResponse(success=False,token='')
        return response
@app.patch('/change_password',tags=['Authentication'])
async def change_password(
    data : ChangePasswordRequest,
    token : str = GetToken(None)
):
    validate = await user_manger.validate(token)
    if (validate):
        result = await user_manger.change_password(token,data)
        if (result):
            return Response(status_code=200)
    raise HTTPException(status_code=401)

@app.get('/history',tags=['Record'],responses=unauthorized_resonse)
async def get_history(
    start_from : int = Query(gt=-1,lt=1000),
    amount : int = Query(gt=-1,lt=1000),
    token : str = GetToken(None)
) -> list[TranslateRecord]:
    validation = await user_manger.validate(token)
    if (validation):
        request = GetRecordRequest(start_from=start_from,amount=amount)
        result = await user_manger.get_history(token,request)
        return result
    else:
        raise HTTPException(status_code=401)
    
@app.get('/saved',tags=['Record'],responses=unauthorized_resonse)
async def get_saved(
    start_from : int = Query(gt=-1,lt=1000),
    amount : int = Query(gt=-1,lt=1000),
    token : str = GetToken(None)
) -> list[TranslateRecord]:
    validation = await user_manger.validate(token)
    if (validation):
        request = GetRecordRequest(start_from=start_from,amount=amount)
        result = await user_manger.get_record(token,request)
        return result
    else:
        raise HTTPException(status_code=401)
    
@app.post('/save',tags=['Record'],responses=unauthorized_resonse)
async def save_record(
    data : TranslateRecord,
    token : str = GetToken(None)
):
    validation = await user_manger.validate(token)
    if (validation):
        await user_manger.save_record(token,data)
        response = Response(status_code=200)
        return response
    else:
        raise HTTPException(status_code=401)

@app.delete('/save',tags=['Record'],responses=unauthorized_resonse)
async def delete_record(
    id : int,
    token : str = GetToken(None)
):
    validation = await user_manger.validate(token)
    if (validation):
        await user_manger.delete_record(token,id)
        respose = Response(status_code=200)
        return respose
    else:
        raise HTTPException(status_code=401)

@app.post('/translate/text',tags=['Translate'],responses=unauthorized_resonse)
async def translate_text(
    data : TranslationRequest,
    token : str = GetToken(None)
) -> TranslationResponse:
    # validation = await user_manger.guest_validate(token)
    # if (validation):
    task = asyncio.create_task(translate_api.translate_test(data))
    user_manger.add_job(task,token,data)
    result = await task
    if (isinstance(result,HTTPException)):
        raise result
    response = result
    return response
    # else:
    #     raise HTTPException(status_code=401)
    
app.add_event_handler('startup',init)    

def start():
    config = common.get_config('server')
    uvicorn.run(app,host=config['host'],port=config['port'])

async def async_start():
    config = common.get_config('server')
    server_config = uvicorn.Config(app,host=config['host'],port=config['port'])
    server = uvicorn.Server(server_config)
    await server.serve()