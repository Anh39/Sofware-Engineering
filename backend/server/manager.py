from backend.common import folder_path
import json
import uuid
from enum import Enum
import hashlib
from typing import Dict
from backend.server.model import RegistedUser,ChangePasswordRequest,Guest,TranslateRecord,LoginRequest,RegisterRequest,TranslationRequest,TranslationResponse,Id
from backend.database.api import DatabaseAPI
from fastapi import HTTPException
import asyncio

class UserController:
    DYNAMIC_TOKEN = False
    def __init__(self):
        self.database_api : DatabaseAPI = DatabaseAPI()
        self.translate_jobs : dict[str,list[tuple[asyncio.Task,TranslationRequest]]] = {}
        self.update_delay : float = 0.5
    def start(self):
        self.database_api.start()
        asyncio.create_task(self.maintain())
    async def _get_user_by_username(self,username : str) -> RegistedUser:
        result = await self.database_api.user(action='get',search={'username' : username})
        return result
    async def _get_user_by_token(self,token : str) -> Guest | RegistedUser:
        result = await self.database_api.user(action='get',search={'token' : token})
        return result
    async def _get_user_by_email(self,email : str) -> RegistedUser:
        result = await self.database_api.user(action='get',search={'email' : email})
        return result
    def _generate_token(self) -> str:
        return str(uuid.uuid4())
    async def _update_user_token(self,user : RegistedUser,new_token):
        user.token = new_token
    async def _add_registerd_user(self,user : RegistedUser):
        await self.database_api.user(action='add',user=user)
    async def _add_guest(self,user : Guest):
        await self.database_api.user(action='add',user=user)
    async def _delete_user(self,token : str):
        await self.database_api.user(action='delete',token=token)
    async def add_guest(self) -> str:
        user = Guest(token=self._generate_token())
        await self._add_guest(user)
        return user.token
    async def login(self,request : LoginRequest) -> str | None:
        user = await self._get_user_by_username(request.username)
        if (isinstance(user,HTTPException)):
            raise HTTPException(status_code=404)
        if (user.password == request.password):
            if (self.DYNAMIC_TOKEN):
                await self._update_user_token(user,self._generate_token())
            return user.token
        return None
    async def register(self,reqest : RegisterRequest,token : str) -> str | None:
        user = await self._get_user_by_username(reqest.username)
        if (user == None):
            user = await self._get_user_by_email(reqest.email)
            if (user == None):
                user = RegistedUser(
                    token = self._generate_token(),
                    email = reqest.email,
                    password = reqest.password,
                    username = reqest.username
                )
                if (token != None):
                    user.history = await self._get_user_by_token(token)
                    await self._delete_user(token)
                await self._add_registerd_user(user)
                return user.token
        return None
    async def validate(self,token : str) -> bool:
        user = await self._get_user_by_token(token)
        return user != None and user.type_name == 'Registed'
    async def guest_validate(self,token : str) -> bool:
        user = await self._get_user_by_token(token)
        return user != None
    async def add_history(self,token : str,record : TranslateRecord)-> RegistedUser | Guest:
        await self.database_api.history(action='add',token=token,record=record)
    async def save_record(self,token : str,record : TranslateRecord) -> None:
        await self.database_api.saved(action='add',token=token,record=record)
    async def delete_record(self,token : str,id : int) -> None:
        await self.database_api.saved(action='delete',token=token,id = id)
    async def get_user(self,token : str) :
        return await self._get_user_by_token(token)
    async def change_password(self,token : str,request : ChangePasswordRequest) -> bool:
        user = await self._get_user_by_token(token)
        if (user == None):
            return False
        if (user.password == request.old_password):
            user.password = request.new_password
            await self.database_api.user(action='update',token=token,user=user)
            return True
        else:
            return False
    def add_job(self,job : asyncio.Task,token : str,request : TranslationRequest):
        if (token in self.translate_jobs):
            self.translate_jobs[token].append((job,request))
        else:
            self.translate_jobs[token] = [(job,request)]

    async def maintain(self):
        while(True):
            empty_jobs_token = []
            for token in self.translate_jobs:
                jobs = self.translate_jobs[token]
                if (len(jobs) == 0):
                    empty_jobs_token.append(token)
                for job,request in jobs:
                    if job.done():
                        result : TranslationResponse = job.result()
                        record = TranslateRecord(
                            from_content=request.from_content,
                            to_content=result.to_content,
                            from_language=request.from_language,
                            to_language=request.to_language,
                            engine_used=result.engine_used
                        )
                        await self.add_history(token,record)
                        jobs.pop(0)
                    else:
                        break
                    
            for token in empty_jobs_token:
                self.translate_jobs.pop(token)
            await asyncio.sleep(self.update_delay)