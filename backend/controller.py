from aiohttp import web
from backend import folder_path
import os
import asyncio
import json
from enum import Enum
from backend.model import Model
from backend.model import Type
import time

public = folder_path.frontend.public
frontend_files = folder_path.util.get_tree(folder_path.frontend.path)

for key in frontend_files:
    if ("index.html" in key):
        index_file = frontend_files[key]

routes = web.RouteTableDef()
no_cache = {'Cache-Control':'no-cache'}

@routes.get('/')
async def entry(request : web.Request):
    try:
        session_id = Model.add_guest()
        response = web.FileResponse(path=index_file,status=200)
        response.set_cookie('uuid',session_id)
        return response
    except:
        return web.Response(text='Server error',status=500)

# @routes.get('/{name}')
# async def request_resource(request : web.Request):
#     name = request.match_info['name']
#     try:
#         session_id = request.cookies.get('uuid')
#         if (Model.guest_validate(session_id)):
#             return web.FileResponse(path=mapping[name],status=200)
#         return web.Response(text='Server error',status=500)
#     except:
#         return web.Response(text='Resource not found',status=404)

@routes.post('/authentication/{kind}')
async def authentication(request : web.Request):
    kind = request.match_info['kind']
    if (kind == 'login'):
        content = await request.json()
        uuid = Model.login(content['username'],content['password'])
        if (uuid == False or uuid == None):
            return web.Response(text='Wrong username/password',status=401)
        else:
            response = web.Response(text='Login successfully',status=200)
            response.set_cookie('uuid',uuid)
            return response
    elif (kind == 'register'):
        content = await request.json()
        print(content)
        uuid = Model.add_user(content['username'],content['password'],content['email'])
        if (uuid == False or uuid == None):
            return web.Response(text='Failed to register',status=401)
        else:
            response = web.Response(text='Register successfully',status=200)
            response.set_cookie('uuid',uuid)
            return response
    elif (kind == 'reset_password'):
        return web.Response(text='Method not implemented',status=500)
    else:
        return web.Response(text='Method not implemented',status=500)


@routes.post('/utility/{kind}')
async def utility(request : web.Request):
    kind = request.match_info['kind']
    session_id = request.cookies.get('uuid')
    guest_validate = Model.guest_validate(session_id)
    if (guest_validate != False):
        if (kind == 'history'):
            history = Model.get_history(session_id,0,10)
            return web.Response(text=json.dumps(history),status=200,content_type=Type.json)
        elif (kind == 'saved'):
            if (Model.validate(session_id)):
                saved = Model.get_saved(session_id,0,10)
                return web.Response(text=json.dumps(saved),status=200,content_type=Type.json)
        elif (kind == 'save'):
            if(Model.validate(session_id)):
                save_content = await request.json()
                Model.save(session_id,save_content)
                return web.Response(text='Saved',content_type=Type.plain,status=200)
    return web.Response(text='Method not implemented',status=500)

@routes.post('/translate/{kind}')
async def translate(request : web.Request):
    start_time = time.time()
    session_id = request.cookies.get('uuid')
    kind = request.match_info['kind']
    if (Model.guest_validate(session_id) or True):
        if (kind == 'text'):
            content = await request.json()
            text_result = await Model.translate_text(session_id,content)
            result = {
                "text" : text_result,
                "prompt" : content["content"]
            }
            end_time = time.time()
            print(f'Request process time : {end_time-start_time}')
            return web.Response(text=json.dumps(result),status=200)
    return web.Response(text='Method not implemented',status=500)

@routes.get('/{tail:.*}')
async def request_resoure(request : web.Request):
    path = os.path.normpath(request.match_info['tail'])
    if (path in frontend_files):
        return web.FileResponse(path=frontend_files[path],status=200)
    return web.Response(text='File not found',status=404)