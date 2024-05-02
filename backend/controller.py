from aiohttp import web
from backend import folder_path
import os
import asyncio
import json
from enum import Enum
from backend.model import Model
from backend.model import Type
import time
from backend.translate_backend.translator_api import MyMemoryAPI
from aiohttp_apispec import setup_aiohttp_apispec,docs,request_schema,headers_schema
from backend.documetation_schema import *

public = folder_path.frontend.public
frontend_files = folder_path.util.get_tree(folder_path.frontend.path)

model : Model = None

async def init():
    global model
    model = Model()
    await model.init()



for key in frontend_files:
    if ("index.html" in key):
        index_file = frontend_files[key]

routes = web.RouteTableDef()
no_cache = {'Cache-Control':'no-cache'}


@docs(
    tags=["Entry"],
    description="Url mặc định khi vào page",
    responses = {
        200 : {'description' : 'Server không lỗi'},
        500 : {'description' : 'Server lỗi'}
    }
)
@request_schema(Schema())
@routes.get('/')
async def entry(request : web.Request):
    try:
        session_id = model.add_guest()
        response = web.FileResponse(path=index_file,status=200)
        response.set_cookie('uuid',session_id)
        return response
    except:
        return web.Response(text='Server error',status=500)

@docs(
    tags=["Authentication"],
    description="Đăng nhập",
    responses={
        200 : {'description' : 'Đăng nhập thành công'},
        401 : {'description' : 'Đăng nhập thất bại'}
    }
)
@headers_schema(ValidationSchema())
@request_schema(LoginSchema())
@routes.post('/authentication/login')
async def login(request : web.Request):
    content = await request.json()
    uuid = model.login(content['username'],content['password'])
    if (uuid == False or uuid == None):
        return web.Response(text='Sai tên người dùng/mật khẩu',status=401)
    else:
        response = web.Response(text='Đăng nhập thành công',status=200)
        response.set_cookie('uuid',uuid)
        return response
@docs(
    tags=["Authentication"],
    description="Đăng ký",
    responses={
        200 : {'description' : 'Đăng ký thành công'},
        401 : {'description' : 'Đăng ký thất bại'}
    }
)
@headers_schema(ValidationSchema())
@request_schema(RegisterSchema())
@routes.post('/authentication/register')
async def register(request : web.Request):
    content = await request.json()
    uuid = model.add_user(content['username'],content['password'],content['email'])
    if (uuid == False or uuid == None):
        return web.Response(text='Đăng ký thất bại',status=401)
    else:
        response = web.Response(text='Đăng ký thành công',status=200)
        response.set_cookie('uuid',uuid)
        return response
@docs(
    tags=["Authentication","Not Implemented"],
    description="Đặt lại mật khẩu",
    responses={
        200 : {'description' : 'Đặt lại mật khẩu thành công'},
        401 : {'description' : 'Đặt lại mật khẩu thất bại'}
    }
)
@headers_schema(ValidationSchema())
@request_schema(ResetPasswordSchema())
@routes.patch('/authentication/reset_password')
async def reset_password(request : web.Request):
    return web.Response(text='Method not implemented',status=500)

@docs(
    tags=["Utility"],
    description="Lấy về lịch sử bản dịch",
    responses={
        200 : {
            'schema' : MultiTranslationResponseSchema,
            'description' : 'Các bản dịch'
            },
        401 : {'description' : 'Lỗi khi xác thực'}
    }
)
@headers_schema(ValidationSchema())
@request_schema(GetHistorySchema())
@routes.post('/utility/history')
async def get_history(request : web.Request):
    session_id = request.cookies.get('uuid')
    guest_validate = model.guest_validate(session_id)
    if (guest_validate != False):
        body = await request.json()
        history = model.get_history(session_id,body['from_item'],body['amount'])
        return web.Response(text=json.dumps(history),status=200,content_type=Type.json)
    else:
        return web.Response(text='Lỗi xác thực',status=401)

@docs(
    tags=["Utility"],
    description="Lấy về bản dịch đã lưu",
    responses={
        200 : {
            'schema' : MultiTranslationResponseSchema,
            'description' : 'Các bản dịch'
            },
        401 : {'description' : 'Lỗi khi xác thực'}
    }
)
@headers_schema(ValidationSchema())
@request_schema(GetSavedSchema())
@routes.post('/utility/saved')
async def get_saved(request : web.Request):
    session_id = request.cookies.get('uuid')
    validate = model.guest_validate(session_id)
    if (validate != False):
        body = await request.json()
        saved = model.get_history(session_id,body['from_item'],body['amount'])
        return web.Response(text=json.dumps(saved),status=200,content_type=Type.json)
    else:
        return web.Response(text='Lỗi xác thực',status=401)
    
@docs(
    tags=["Utility"],
    description="Lưu bản dịch",
    responses={
        200 : {'description' : 'Các bản dịch'},
        401 : {'description' : 'Lỗi khi xác thực'}
    }
)
@headers_schema(ValidationSchema())
@request_schema(SaveSchema())
@routes.post('/utility/save')
async def save_translation(request : web.Request):
    session_id = request.cookies.get('uuid')
    validate = model.validate(session_id)
    if (validate != False):
        save_content = await request.json()
        model.save(session_id,save_content)
        return web.Response(text='Saved',content_type=Type.plain,status=200)
    else:
        return web.Response(text='Lỗi xác thực',status=401)

@docs(
    tags=["Translate"],
    description="Dịch nội dung text",
    responses={
        200 : {
            'schema' : TranslationResponseShortSchema,
            'description' : 'Nội dung dịch'
            },
        401 : {'description' : 'Lỗi khi xác thực'}
    }
)
@headers_schema(ValidationSchema())
@request_schema(GetHistorySchema())
@routes.post('/translate/text')
async def translate(request : web.Request):
    start_time = time.time()
    session_id = request.cookies.get('uuid')
    if (model.guest_validate(session_id)):
        content = await request.json()
        text_result = await model.translate_text(session_id,content)
        result = {
            "text" : text_result,
            "prompt" : content["content"]
        }
        end_time = time.time()
        print(f'Request process time : {end_time-start_time}')
        return web.Response(text=json.dumps(result),status=200)
    else:
        return web.Response(text='Lỗi xác thực',status=401)

@routes.get('/{tail:.*}')
async def request_resoure(request : web.Request):
    path = os.path.normpath(request.match_info['tail'])
    if (path in frontend_files):
        return web.FileResponse(path=frontend_files[path],status=200)
    return web.Response(text='File not found',status=404)

def route_start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    return loop