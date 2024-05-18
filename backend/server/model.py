from pydantic import BaseModel,Field
from abc import abstractmethod
import hashlib


class LoginRequest(BaseModel):
    username : str = Field(
        min_length=3,
        max_length=50,
        pattern='^[A-Za-z0-9]*$',
        title='User name'
    )
    password : str = Field(
        min_length=3,
        max_length=50,
        pattern='^[A-Za-z0-9]*$',
        title='Password'
    )

class LoginResponse(BaseModel):
    success : bool = False
    token : str = Field(max_length=5000)

class RegisterRequest(LoginRequest):
    email : str = Field(
        min_length=11,
        max_length=50,
        pattern='^[A-Za-z0-9@.]*$',
        title ='Email'
    )
    
class TranslationRequest(BaseModel):
    # token : str = Field(
    #     min_length=1,
    #     max_length=256
    # )
    from_language : str = Field(
        min_length=2,
        max_length=8
    )
    to_language : str = Field(
        min_length=2,
        max_length=8
    )
    from_content : str = Field(
        min_length=1,
        max_length=5000
    )
    engine : str = Field(
        min_length=1,
        max_length=50,
        default='auto'
    )

class TranslationResponse(BaseModel):
    to_content : str = Field(
        min_length=1,
        max_length=5000
    )
    engine_used : str = Field(
        min_length=1,
        max_length=500,
        default='Google'
    ) 
    
class TranslateRecord(TranslationRequest,TranslationResponse):
    pass
    
class GetRecordRequest(BaseModel):
    start_from : int = Field(gt=0,lt=10000)
    amount : int = Field(gt=0,lt=10000)
    
class Type:
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
    type_name = 'User'
    def __init__(self,token : str) -> None:
        self.token = str(token)
        self.history = []
    def add_history(self,element):
        self.history.append(element)
    def get_history(self,from_it : int,amount : int):
        return self.history[from_it:min(from_it+amount,len(self.history)-from_it-1)]
    def get_token(self) -> str:
        return self.token
    @abstractmethod
    def to_dict(self) -> dict:
        return {
            'type' : self.type_name,
            'token' : self.token,
            'history' : self.history
        }
    @abstractmethod
    def from_dict(self,input : dict[str,object]) -> 'User':
        result = User(input['token'])
        result.history = input.get('history',[])
        return result
    def __hash__(self) -> int:
        return hashlib.sha256(str(self.token))
class Guest(User):
    type_name = 'Guest'
    def to_dict(self) -> dict:
        return super().to_dict()
    @classmethod
    def from_dict(self, input: dict[str, object]) -> User:
        new_user = Guest(input['token'])
        new_user.history = input.get('history',[])
        return new_user
class RegistedUser(User):
    type_name = 'RegistedUser'
    def __init__(self, token: str,username,password,email) -> None:
        super().__init__(token)
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
        new_user = RegistedUser(input['token'],input['username'],input['password'],input['email'])
        new_user.history = input['history']
        new_user.saved = input['saved']
        return new_user