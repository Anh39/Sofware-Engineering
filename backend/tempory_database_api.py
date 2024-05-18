from database.databases import *
from backend.common import folder_path

class TemporyDatabaseAPI:
    def __init__(self) -> None:
        self.handler = handler(folder_path.database.database)
    def add_user(self,input : dict[str,object] = {
        'type' : None,
        'identifier' : None,
        'username' : None,
        'password' : None,
        'email' : None
    }):
        user_type = None
        # if (input['type'] == 'RegistedUser'):
        #     user_type = User_type.REGISTED
        # elif (input['type'] == 'Guest'):
        #     user_type = User_type.GUEST
        self.handler.add_user(input.get('username',None),input.get('password',None),input.get('email'),user_type)
    def add_history(self,input : dict[str,object] = {
        'type' : None,
        'username' : None,
        'from_content' : None,
        'to_content' : None,
        'from_language' : None,
        'to_language' : None,
        'time' : None
    }):
        user_id = self.handler.get_user_by_username(input['username'])
        translation_type = None
        if (input['type'] == 'text'):
            translation_type = TranslationType.TEXT
        self.handler.add_translation(user_id,translation_type,input.get('from_content',None),input.get('to_content',None),input['from_language'],input['to_language'],input.get('time',None))
    
    def get_translation(self,username : str):
        user_id = self.handler.get_user_by_username(username)
        result = self.handler.get_translation_by_UserID(user_id)
        print(result)