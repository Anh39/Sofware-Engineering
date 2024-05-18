import asyncio
import os
import aiohttp
from aiohttp import web
import json
from backend.common import folder_path,common
from backend.server.model import TranslationRequest,TranslationResponse
from fastapi import HTTPException
from typing import Literal
from backend.server.model import *

config = common.get_config()
headers = {
    "Content-Type": "application/json"
}

class DatabaseAPI:
    def __init__(self) -> None:
        self.base_url = common.get_url(config['database'])
        self.session : aiohttp.ClientSession = None
    def start(self) :
        self.session = aiohttp.ClientSession(self.base_url)
    async def stop(self) :
        await self.session.close()
        self.session = None
    async def user(self,action : Literal['get','add','update','delete',None] = None,
                   search : dict[str,object] | None = None,
                   user : RegistedUser | Guest = None,
                   token : str = None
                   ) -> RegistedUser | Guest | HTTPException | None:
        try:
            data = {
                'search' : search,
                'user' : user.model_dump() if user != None else None,
                'token' : token
            }
            if (action == 'get'):
                async with self.session.get('/user',params=data['search']) as response:
                    if (response.status == 200):
                        result = await response.json()
                        if (result == None):
                            return None
                        if (result['type_name'] == 'Guest'):
                            return Guest.model_validate(result)
                        else:
                            return RegistedUser.model_validate(result)
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'add'):
                async with self.session.post('/user',headers=headers,data=json.dumps(data['user'])) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'update'):
                async with self.session.patch('/user',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'delete'):
                async with self.session.delete('/user',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            else :
                return HTTPException(status_code=404,detail='Action not found')
        except Exception as e:
            print(e)
            return None
        
    async def history(self,action : Literal['get','add','delete',None] = None,
                   record : TranslateRecord = None,
                   token : str = None
                   ) -> list[TranslateRecord] | HTTPException:
        try:
            data = {
                'record' : record.model_dump() if record != None else None,
                'token' : token
            }
            if (action == 'get'):
                async with self.session.get('/history',params={'token' : token}) as response:
                    if (response.status == 200):
                        result = await response.json()
                        records = json.loads(result)
                        final_result = []
                        for record in records:
                            final_result.append(TranslateRecord.model_validate(record))
                        return final_result
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'add'):
                async with self.session.post('/history',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'update'):
                async with self.session.patch('/history',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'delete'):
                async with self.session.delete('/history',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            else :
                return HTTPException(status_code=404,detail='Action not found')
        except Exception as e:
            print(e)
            return None
        
    async def saved(self,action : Literal['get','add','delete',None] = None,
                   record : TranslateRecord = None,
                   token : str = None,
                   id : int = None
                   ) -> list[TranslateRecord] | HTTPException:
        try:
            data = {
                'record' : record.model_dump() if record != None else None,
                'token' : token,
                'id' : id
            }
            if (action == 'get'):
                async with self.session.get('/saved',params=json.dumps(data)) as response:
                    if (response.status == 200):
                        result = await response.json()
                        records = json.loads(result)
                        final_result = []
                        for record in records:
                            final_result.append(TranslateRecord.model_validate(record))
                        return final_result
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'add'):
                async with self.session.post('/saved',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):                        
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'update'):
                async with self.session.patch('/saved',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            elif (action == 'delete'):
                async with self.session.delete('/saved',headers=headers,data=json.dumps(data)) as response:
                    if (response.status == 200):
                        return None
                    else:
                        print(f'Error : {response.status} {self.session._base_url}')
                        return HTTPException(status_code=response.status,detail= await response.text())
            else :
                return HTTPException(status_code=404,detail='Action not found')
        except Exception as e:
            print(e)
            return None