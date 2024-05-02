from backend import folder_path
import json
import uuid
from enum import Enum
import hashlib
from typing import Dict
from backend.translator import Translator
from backend.datatype import *

class Model:
    """Lớp static để quản lý Model
    """
    def __init__(self) -> None:
        self.users : Dict[str,User|RegistedUser] = {}
        self.translator : Translator = Translator()
    def save_user_info(self,path = folder_path.backend.user):
        user_info = []
        for ele in self.users:
            user_info.append(self.users[ele].to_dict())
        with open(path,'w') as file:
            file.write(json.dumps(user_info))
    async def init(self,path : str = folder_path.backend.user):
        await self.translator.init()
        content = []
        with open(path,'r') as file:
            content = json.loads(file.read())
        for ele in content:
            if (ele['type'] == 'Guest'):
                new_user = Guest.from_dict(ele)
            else:
                new_user = RegistedUser.from_dict(ele)
            self.users[new_user.identifier] = new_user
    def get_email(self,username : str) -> str:
        for id in self.users:
            user = self.users[id]
            if isinstance(user,RegistedUser):
                if user.username == username:
                    return user.email
    def login(self,username : str,password : str) -> str:
        if (username != None and password != None):
            for id in self.users:
                user = self.users[id]
                if isinstance(user,RegistedUser):
                    if user.username == username and user.password == password:
                        return user.identifier
        return False
    def add_guest(self) -> str:
        session_id = str(uuid.uuid4())
        new_guest = Guest(session_id)
        self.users[new_guest.identifier] = new_guest
        return new_guest.identifier
    def add_user(self,username : str,password : str,email : str) -> str:
        if (username != None and password != None):
            for id in self.users:
                user = self.users[id]
                if isinstance(user,RegistedUser):
                    if user.username == username and user.password == password:
                        return None
            session_id = str(uuid.uuid4())
            new_user = RegistedUser(session_id,username,password,email)
            self.users[new_user.identifier] = new_user
            self.save_user_info()
            for key in self.users:
                print(key,self.users[key].to_dict())
            return new_user.identifier
        else:
            return None
    def validate(self,identifier : str) -> bool:
        return (identifier in self.users and type(self.users[identifier]) == RegistedUser)
    def guest_validate(self,identifier : str) -> bool:
        return (identifier in self.users)
    def add_history(self,identifier : str,content : any):
        user = self.users[identifier]
        user.add_history(content)
        self.save_user_info()
    def get_history(self,identifier : str,from_it : int,amount : int) -> list:
        user = self.users[identifier]
        return user.get_history(from_it,amount)
    def save(self,identifier : str,translation : dict[str,object]):
        user : RegistedUser = self.users[identifier]
        user.add_save(translation)
    def get_saved(self,identifier : str,from_it : int,amount : int) -> list:
        user : RegistedUser = self.users[identifier]
        return user.get_saved(from_it,amount)
    async def translate_text(self,identifier : str,content : any) -> str:
        from_language = content['from_language']
        to_language = content['to_language']
        from_content = content['content']
        to_content = await self.translator.translate(from_language,to_language,from_content)
        content = {
            'from_language' : from_language,
            'to_language' : to_language,
            'from_content' : from_content,
            'to_content' : to_content
        }
        self.add_history(identifier,content)
        return to_content
        