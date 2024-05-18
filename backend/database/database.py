from abc import abstractmethod
from backend.server.model import *

class Handler:
    # CRUD 
    # Create - Add
    # Retrive - Get
    # Update - Update
    # Delete - Delete
    @abstractmethod
    def start(self) -> None:
        pass
    @abstractmethod
    def add_user(self,user : RegistedUser | Guest) -> None:
        pass
    @abstractmethod
    def get_user(self,search : dict[str,object] = {
            'token' : None,
            'username' : None,
            'email' : None
        }) -> RegistedUser | Guest:
        pass
    @abstractmethod
    def update_user(self,token : str, user : Guest | RegistedUser) -> None:
        pass
    @abstractmethod
    def delete_user(self,token) -> None:
        pass
    
    @abstractmethod
    def add_translation_history(self,token : str,record : TranslateRecord) -> None:
        pass
    @abstractmethod
    def get_translation_history(self,token : str) -> list[TranslateRecord]:
        pass
    @abstractmethod
    def delete_translation_history(self,token : str,record : TranslateRecord) -> None:
        pass
    
    @abstractmethod
    def add_translation_saved(self,token : str,record : TranslateRecord) -> None:
        pass
    @abstractmethod
    def get_translation_saved(self,token : str) -> list[TranslateRecord]:
        pass
    @abstractmethod
    def delete_translation_saved(self,token : str,record : TranslateRecord) -> None:
        pass
    
    
    