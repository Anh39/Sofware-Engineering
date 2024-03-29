from aiohttp import web
from backend import folder_path
import os
import asyncio
import json
from enum import Enum
from backend.model import Model
from backend.model import Type

public = folder_path.frontend.public

mapping = {
    'index.html' : public.index,
    'style.css' : public.style,
    'client.js' : public.client,
    'favicon.ico' : public.favicon
}


routes = web.RouteTableDef()
no_cache = {'Cache-Control':'no-cache'}

@routes.get('/')
async def entry(request : web.Request):
    try:
        session_id = Model.add_guest()
        response = web.FileResponse(path=mapping['index.html'],status=200)
        response.set_cookie('uuid',session_id)
        return response
    except:
        return web.Response(text='Server error',status=500)

@routes.get('/{name}')
async def request_resource(request : web.Request):
    name = request.match_info['name']
    try:
        session_id = request.cookies.get('uuid')
        if (Model.guest_validate(session_id)):
            return web.FileResponse(path=mapping[name],status=200)
        return web.Response(text='Server error',status=500)
    except:
        return web.Response(text='Resource not found',status=404)
    
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
        uuid = Model.add_user(content['username'],content['password'],content['email'])
        if (uuid == False or uuid == None):
            return web.Response(text='Failed to register',status=401)
        else:
            response = web.Response(text='Login successfully',status=200)
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
    session_id = request.cookies.get('uuid')
    kind = request.match_info['kind']
    if (Model.guest_validate(session_id)):
        if (kind == 'text'):
            content = await request.json()
            result = Model.translate_text(session_id,content)
            return web.Response(text=result,content_type=Type.plain,status=200)
    return web.Response(text='Method not implemented',status=500)