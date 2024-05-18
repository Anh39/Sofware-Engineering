from backend.common import folder_path
import json
import uuid
from enum import Enum
import hashlib
from typing import Dict
from backend.server.model import RegistedUser,Guest,TranslateRecord,LoginRequest,RegisterRequest
from backend.database.api import DatabaseAPI
from fastapi import HTTPException

class UserController:
    DYNAMIC_TOKEN = False
    local_users : Dict[str,Guest|RegistedUser] = {}
    database_api : DatabaseAPI = DatabaseAPI()
    def start(self):
        self.database_api.start()
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
    async def delete_record(self,token : str,record : TranslateRecord) -> None:
        await self.database_api.saved(action='delete',token=token,record=record)
    async def get_user(self,token : str) :
        return await self._get_user_by_token(token)
    
# class Manager:
#     def __init__(self) -> None:
#         self.users : Dict[str,Guest|RegistedUser] = {}
#     def save_user_info(self,path = folder_path.backend.user):
#         user_info = []
#         for ele in self.users:
#             user_info.append(self.users[ele].model_dump_json())
#         with open(path,'w') as file:
#             file.write(json.dumps(user_info))
#     async def init(self,path : str = folder_path.backend.user):
#         # await self.translator.init()
#         content = []
#         try:
#             with open(path,'r') as file:
#                 content = json.loads(file.read())
#         except:
#             pass
#         for ele in content:
#             if (ele['type'] == 'Guest'):
#                 new_user = Guest.model_validate(ele)
#             else:
#                 new_user = RegistedUser.model_validate(ele)
#             self.users[new_user.token] = new_user
#     def get_email(self,username : str) -> str:
#         for id in self.users:
#             user = self.users[id]
#             if isinstance(user,RegistedUser):
#                 if user.username == username:
#                     return user.email
#     def login(self,username : str,password : str) -> str:
#         if (username != None and password != None):
#             for id in self.users:
#                 user = self.users[id]
#                 if isinstance(user,RegistedUser):
#                     if user.username == username and user.password == password:
#                         return user.token
#         return False
#     def add_guest(self) -> str:
#         session_id = str(uuid.uuid4())
#         new_guest = Guest(token=session_id)
#         self.users[new_guest.token] = new_guest
#         return new_guest.token
#     def add_user(self,username : str,password : str,email : str) -> str:
#         if (username != None and password != None):
#             for id in self.users:
#                 user = self.users[id]
#                 if isinstance(user,RegistedUser):
#                     if user.username == username and user.password == password:
#                         return None
#             session_id = str(uuid.uuid4())
#             new_user = RegistedUser(session_id,username,password,email)
#             self.users[new_user.token] = new_user
#             self.save_user_info()
#             return new_user.token
#         else:
#             return None
#     def validate(self,token : str) -> bool:
#         return (token in self.users and type(self.users[token]) == RegistedUser)
#     def guest_validate(self,token : str) -> bool:
#         return (token in self.users)
#     def add_history(self,token : str,content : TranslateRecord):
#         user = self.users[token]
#         user.add_history(content)
#         self.save_user_info()
#     def get_history(self,token : str,from_it : int,amount : int) -> list:
#         user = self.users[token]
#         return user.get_history(from_it,amount)
#     # def save(self,token : str,translation : dict[str,object]):
#     #     user : RegistedUser = self.users[token]
#     #     user.add_save(translation)
#     def get_saved(self,token : str,from_it : int,amount : int) -> list:
#         user : RegistedUser = self.users[token]
#         return user.get_saved(from_it,amount)
    # async def translate_text(self,token : str,content : any) -> str:
    #     from_language = content['from_language']
    #     to_language = content['to_language']
    #     from_content = content['from_content']
    #     to_content = await self.translator.translate(from_language,to_language,from_content)
    #     content = {
    #         'from_language' : from_language,
    #         'to_language' : to_language,
    #         'from_content' : from_content,
    #         'to_content' : to_content
    #     }
    #     self.add_history(token,content)
    #     return to_content
        