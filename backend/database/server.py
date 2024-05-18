from fastapi import FastAPI,Request,Response,HTTPException
from backend.server.model import *
from backend.common import common
import uvicorn
from backend.database.json_db import JSONDatabase
from backend.database.model import *

app = FastAPI()

handler = JSONDatabase()
async def init():
    global handler
    handler.start()

model_not_found_resonse = {401 : {"model" : str, "description" : "Data not found"}}
@app.get("/")
async def root():
    return {"message" : "Konnichiwa Sekai!"}

@app.get('/user',tags=['User'],responses=model_not_found_resonse)
async def get_user(
    token : str = None,
    username : str = None,
    email : str = None
) -> Guest | RegistedUser | None:
    return handler.get_user({
        'token' : token,
        'username' : username,
        'email' : email
    })

@app.post('/user',tags=['User'],responses=model_not_found_resonse)
async def add_user(
    user : RegistedUser | Guest
):
    handler.add_user(user)
    return Response(status_code=200)

@app.patch('/user',tags=['User'],responses=model_not_found_resonse)
async def update_user(
    data : TokenizedUser
):
    handler.update_user(data.token,data.user)
    return Response(status_code=200)

@app.delete('/user',tags=['User'],responses=model_not_found_resonse)
async def delete_user(
    data : Token
):
    handler.delete_user(data.token)
    return Response(status_code=200)

@app.get('/history',tags=['History'],responses=model_not_found_resonse)
async def get_history(
    data : Token
) -> list[TranslateRecord]:
    return handler.get_translation_history(data.token)

@app.post('/history',tags=['History'],responses=model_not_found_resonse)
async def add_history(
    data : TranslationRecordTokenized
):
    handler.add_translation_history(data.token,data.record)
    return Response(status_code=200)

@app.delete('/history',tags=['History'],responses=model_not_found_resonse)
async def delete_history(
    data : TokenizedId
):
    handler.delete_translation_history(data.token,data.id)
    return Response(status_code=200)

@app.get('/saved',tags=['Saved'],responses=model_not_found_resonse)
async def get_saved(
    data : Token
) -> list[TranslateRecord]:
    return handler.get_translation_saved(data.token)

@app.post('/saved',tags=['Saved'],responses=model_not_found_resonse)
async def add_saved(
    data : TranslationRecordTokenized
):
    handler.add_translation_saved(data.token,data.record)
    return Response(status_code=200)

@app.delete('/saved',tags=['Saved'],responses=model_not_found_resonse)
async def delete_saved(
    data : TokenizedId
):
    handler.delete_translation_saved(data.token,data.id)
    return Response(status_code=200)
    

app.add_event_handler('startup',init)    

def start():
    config = common.get_config('database')
    uvicorn.run(app,host=config['host'],port=config['port'])

async def async_start():
    config = common.get_config('database')
    server_config = uvicorn.Config(app,host=config['host'],port=config['port'])
    server = uvicorn.Server(server_config)
    await server.serve()