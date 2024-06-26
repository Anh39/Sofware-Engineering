from backend.database.database import Handler
from backend.common import folder_path
from backend.server.manager import *
from backend.database.model import Id
import json

from backend.server.model import Guest, RegistedUser, TranslateRecord

class JSONDatabase(Handler):
    container : list[RegistedUser|Guest] = []
    def _save(self) -> None:
        data = []
        for user in self.container:
            data.append(user.model_dump())
        with open(folder_path.common.user,'w') as file:
            file.write(json.dumps(data))
    def start(self) -> None:
        with open(folder_path.common.user,'r') as file:
            json_data = json.loads(file.read())
        for user in json_data:
            if (user['type_name'] == 'Guest'):
                self.container.append(Guest.model_validate(user))
            else:
                self.container.append(RegistedUser.model_validate(user))
    def add_user(self, data: RegistedUser | Guest) -> None:
        self.container.append(data)
        self._save()
    def get_user(self, data: dict[str, object] = ...) -> RegistedUser | Guest:
        if ('token' in data and data['token'] != None):
            token = data['token']
            for user in self.container:
                if (user.token == token):
                    return user
        if ('username' in data and data['username'] != None):
            username = data['username']
            for user in self.container:
                if (user.username == username):
                    return user
        return None
    def update_user(self, token: str, user: Guest | RegistedUser):
        for i in range(len(self.container)):
            if (self.container[i].token == token):
                self.container[i] = user
        self._save()
    def add_translation_history(self, user_token: str, data: TranslateRecord) -> None:
        self.get_user({'token' : user_token}).add_history(data)
        self._save()
    def get_translation_history(self, user_token: str) -> list[TranslateRecord]:
        return self.get_user({'token' : user_token}).history
    def add_translation_saved(self, user_token: str, data: TranslateRecord) -> None:
        self.get_user({'token' : user_token}).add_saved(data)
        self._save()
    def get_translation_saved(self, user_token: str) -> list[TranslateRecord]:
        return self.get_user({'token' : user_token}).saved
    def delete_translation_history(self, token: str, record: TranslateRecord) -> None:
        user = self.get_user({'token' : token})
        while (True):
            complete = True
            for user_record in user.history:
                if (user_record == record):
                    user.history.remove(user_record)
                    complete = False
            if (complete):
                break
        self._save()
    def delete_translation_saved(self, token: str, id : int) -> None:
        user = self.get_user({'token' : token})
        user.history.pop(id)
        # while (True):
        #     complete = True
        #     for user_record in user.saved:
        #         if (user_record == record):
        #             user.saved.remove(user_record)
        #             complete = False
        #     if (complete):
        #         break
        self._save()