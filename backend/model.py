from backend import folder_path
import json
import uuid
from enum import Enum
import hashlib
from typing import Dict
from backend.translator import Translator

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
    def __init__(self,identifier : uuid.UUID) -> None:
        self.identifier = str(identifier)
        self.history = []
    def add_history(self,element):
        self.history.append(element)
    def get_history(self,from_it : int,amount : int):
        return self.history[from_it:from_it+amount]
    def get_identifier(self) -> str:
        return self.identifier
    def __hash__(self) -> int:
        return hashlib.sha256(str(self.identifier))
class Guest(User):
    """Lớp dùng để thể hiện Guest User (người dùng khách)
    Thừa kế từ lớp User
    """
    pass
class RegistedUser(User):
    """Lớp dùng để thể hiện Registed User (người dùng đã đăng ký)
    Thừa kế từ lớp User

    Args:
        User (_type_): _description_
    """
    def __init__(self, identifier: uuid.UUID,username,password,email) -> None:
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

class Model:
    """Lớp static để quản lý Model
    """
    username_password = {}
    email_info = {}
    users : Dict[uuid.UUID,User] = {}
    translator : Translator
    @classmethod
    def init(self,path : str = folder_path.backend.user):
        """Setup (cài đặt) cơ bản cho lớp
        """
        self.translator = Translator()
        content = []
        with open(path,'r') as file:
            content = json.loads(file.read())
        for ele in content:
            self.username_password[ele['username']] = ele['password']
            self.email_info[ele['email']] = {
                'username' : ele['username'],
                'password' : ele['password']
            }
    @classmethod
    def get_email(self,username : str) -> str:
        """Lấy về email

        Args:
            username (str): Tên người dùng

        Returns:
            str: email
        """
        for ele in self.email_info:
            if(self.email_info[ele]['username'] == username):
                return ele
    @classmethod
    def login(self,username : str,password : str) -> str:
        """Đăng nhập

        Args:
            username (str): Tên người dùng
            password (str): Mật khẩu

        Returns:
            str: session_id nếu thành công
            bool: False nếu thất bại
        """
        if (username != None and password != None):
            if (username in self.username_password):
                if (self.username_password[username] == password):
                    session_id = uuid.uuid4()
                    new_user = RegistedUser(session_id,username,password,self.get_email(username))
                    self.users[new_user.identifier] = new_user
                    return new_user.identifier
        return False
    
    @classmethod
    def add_guest(self) -> str:
        """Thêm Guest User (người dùng khách)

        Returns:
            str: session_id
        """
        session_id = uuid.uuid4()
        new_guest = Guest(session_id)
        self.users[new_guest.identifier] = new_guest
        return new_guest.identifier
    @classmethod
    def add_user(self,username : str,password : str,email : str) -> str:
        """Đăng ký người dùng mới

        Args:
            username (str): Tên người dùng
            password (str): Mật khẩu
            email (str): Email

        Returns:
            str: session_id
        """
        if (username not in self.username_password and email not in self.email_info):
            session_id = uuid.uuid4()
            new_user = RegistedUser(session_id,username,password,email)
            self.users[new_user.identifier] = new_user
            return new_user.identifier
        else:
            return None
    @classmethod
    def validate(self,identifier : str) -> bool:
        """Xác thực người dùng đã đăng ký

        Args:
            identifier (str): session_id

        Returns:
            bool: True/False
        """
        return (identifier in self.users and type(self.users[identifier]) == RegistedUser)
    @classmethod
    def guest_validate(self,identifier : str) -> bool:
        """Xác thực người dùng khách (Kiểm tra xem có vào bằng phương thức mặc định không (vào bằng index.html))

        Args:
            identifier (str): session_id

        Returns:
            bool: True/False
        """
        return (identifier in self.users)
    @classmethod
    def add_history(self,identifier : str,content : any):
        """Thêm bản ghi lịch sử

        Args:
            identifier (str): session_id
            content (any): Nội dung

        """
        user = self.users[identifier]
        user.add_history(content)
    @classmethod
    def get_history(self,identifier : str,from_it : int,amount : int) -> list:
        """Lấy về lịch sử

        Args:
            identifier (str): session_id
            from_it (int): Lấy bắt đầu từ
            amount (int): Số lượng lấy

        Returns:
            list: Kết quả
        """
        user = self.users[identifier]
        return user.get_history(from_it,amount)
    @classmethod
    def save(self,identifier : str,content : any):
        """Lưu bản ghi người dùng yêu cầu

        Args:
            identifier (str): session_id
            content (any): Nội dung
        """
        user : RegistedUser = self.users[identifier]
        user.add_save(content)
    @classmethod
    def get_saved(self,identifier : str,from_it : int,amount : int) -> list:
        """Lấy bản ghi người dùng đã lưu

        Args:
            identifier (str): session_id
            from_it (int): Lấy bắt đầu từ
            amount (int): Số lượng lấy

        Returns:
            list: Kết quả
        """
        user : RegistedUser = self.users[identifier]
        return user.get_saved(from_it,amount)
    @classmethod
    def translate_text(self,identifier : str,content : any) -> str:
        """Dịch nội dung chữ

        Args:
            identifier (str): session_id
            content (any): Nội dung

        Returns:
            str: Kết quả
        """
        from_language = content('from_language')
        to_language = content('to_language')
        from_content = content('fom_content')
        to_content = self.translator.translate(from_language,to_language,from_content)
        content = {
            'from_language' : from_language,
            'to_language' : to_language,
            'from_content' : from_content,
            'to_content' : to_content
        }
        self.add_history(identifier,content)
        return to_content
        

    
Model.init()