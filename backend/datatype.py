from abc import abstractmethod
from enum import Enum
import hashlib

class Type(Enum):
    html = 'text/html'
    css = 'text/css'
    js = 'application/javascript'
    json = 'text/json'
    plain = 'text/plain'
    ico = 'image/x-icon'
    png = 'image/png'
    webp = 'image/webp'
    File = 'file_response'
    Text = 'text_response'
    
class User:
    """Lớp User (người dùng) gốc
    """
    type_name = 'User'
    def __init__(self,identifier : str) -> None:
        self.identifier = str(identifier)
        self.history = []
    def add_history(self,element):
        self.history.append(element)
    def get_history(self,from_it : int,amount : int):
        return self.history[from_it:from_it+amount]
    def get_identifier(self) -> str:
        return self.identifier
    @abstractmethod
    def to_dict(self) -> dict:
        return {
            'type' : self.type_name,
            'identifier' : self.identifier,
            'history' : self.history
        }
    @abstractmethod
    def from_dict(self,input : dict[str,object]) -> 'User':
        result = User(input['identifier'])
        result.history = input.get('history',[])
        return result
    def __hash__(self) -> int:
        return hashlib.sha256(str(self.identifier))
class Guest(User):
    """Lớp dùng để thể hiện Guest User (người dùng khách)
    Thừa kế từ lớp User
    """
    type_name = 'Guest'
    def to_dict(self) -> dict:
        return super().to_dict()
    @classmethod
    def from_dict(self, input: dict[str, object]) -> User:
        new_user = Guest(input['identifier'])
        new_user.history = input.get('history',[])
        return new_user
class RegistedUser(User):
    """Lớp dùng để thể hiện Registed User (người dùng đã đăng ký)
    Thừa kế từ lớp User

    Args:
        User (_type_): _description_
    """
    type_name = 'RegistedUser'
    def __init__(self, identifier: str,username,password,email) -> None:
        super().__init__(identifier)
        self.saved = []
        self.username = username
        self.password = password
        self.email = email
    def get_saved(self,from_it : int,amount : int):
        return self.history[from_it:from_it+amount]
    def add_save(self,element):
        self.saved.append(element)
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def get_email(self):
        return self.email
    def to_dict(self) -> dict:
        result = super().to_dict()
        result['username'] = self.username
        result['password'] = self.password
        result['email'] = self.email
        result['saved'] = self.saved
        return result
    @classmethod
    def from_dict(self, input: dict[str, object]) -> User:
        new_user = RegistedUser(input['identifier'],input['username'],input['password'],input['email'])
        new_user.history = input['history']
        new_user.saved = input['saved']
        return new_user