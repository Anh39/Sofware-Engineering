import sqlite3
import datetime
import copy
from queue import SimpleQueue
import os
from enum import Enum

def _convert_to_string(input = None):
    if (input != None):
        if (type(input) == list):
            for i in range(len(input)):
                input[i] = _convert_to_string(input[i])
            return input
        else:
            return str(input)
    else:
        return None
    
class _select_command :
    def __init__(self,column_ : list = ['*'],from_ : str = '',addition_query : list = None,value : list = None) -> None:
        self.column_ = column_
        self.from_ = from_
        self.addition_query = addition_query
        self.value = value
    def evaluate(self) -> str:
        self.column_ = _convert_to_string(self.column_)
        self.from_ = _convert_to_string(self.from_)
        self.addition_query = _convert_to_string(self.addition_query)
        self.value = _convert_to_string(self.value)
        if (self.addition_query == None):
            return 'SELECT ' + ','.join(self.column_) + ' FROM ' + self.from_
        else:
            conditions = ''
            for i in range(len(self.value)):
                conditions += self.addition_query[i] + '"' + self.value[i] + '"'
            return 'SELECT ' + ','.join(self.column_) + ' FROM ' + self.from_ + ' WHERE ' + conditions
        
class _delete_command:
    def __init__(self,from_ : str = '',addition_query : list = None,value : list = None) -> None:
        self.from_ = from_
        self.addition_query = addition_query
        self.value = value
    def evaluate(self) -> str:
        self.from_ = _convert_to_string(self.from_)
        self.addition_query = _convert_to_string(self.addition_query)
        self.value = _convert_to_string(self.value)
        if (self.addition_query == None):
            return 'DELETE FROM ' + self.from_
        else:
            conditions = ''
            for i in range(len(self.value)):
                conditions += self.addition_query[i] + '"' + self.value[i] + '"'
            return 'DELETE FROM ' + self.from_ + ' WHERE ' + conditions
        
class _update_command:
    def __init__(self,from_ : str = '',set_column : list = None,set_value : list = None,addition_query : list = None,value : list = None) -> None:
        self.from_ = from_
        self.set_column = set_column
        self.set_value = set_value
        self.addition_query = addition_query
        self.value = value
    def evaluate(self) -> str:
        self.from_ = _convert_to_string(self.from_)
        self.set_column = _convert_to_string(self.set_column)
        self.set_value = _convert_to_string(self.set_value)
        self.addition_query = _convert_to_string(self.addition_query)
        self.value = _convert_to_string(self.value)
        set_conditions = []
        for i in range(len(self.set_column)):
            set_conditions.append(f"{self.set_column[i]} = '{self.set_value[i]}'")
        set_conditions = ', '.join(set_conditions)
        if (self.addition_query == None):
            return 'UPDATE ' + self.from_ + ' SET ' + set_conditions
        else:
            conditions = ''
            for i in range(len(self.value)):
                conditions += self.addition_query[i] + '"' + self.value[i] + '"'
            return 'UPDATE ' + self.from_ + ' SET ' + set_conditions + ' WHERE ' + conditions
        
class _insert_command:
    def __init__ (self,table : str = '',column : list = ['*'],value : list = []):
        self.table = table
        self.column = column
        self.value = value
    def evaluate(self) -> str:
        self.table = _convert_to_string(self.table)
        self.column = _convert_to_string(self.column)
        self.value = _convert_to_string(self.value)
        return 'INSERT INTO ' + self.table + '(' + ','.join(self.column) + ') VALUES ("' + '","'.join(self.value) + '")'

class TranslationType(Enum):
    TEXT = "dịch chữ "
    IMAGE = "hình ảnh"
    DOC = "tài liệu"
    AUDIO = "âm thanh"

class User_type(Enum):
    GUEST = 'người dùng khách'
    REGISTED = 'người dùng đăng kí'

class handler :
    def __init__(self,path : str) -> None:
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
    def get_current_time(self):
        curr_time = datetime.datetime.now()
        formated_time = curr_time.strftime('%Y-%m-%d %H:%M:%S')
        return formated_time
    def commit(self) -> bool:
        try:
            self.conn.commit()
            return True
        except:
            print('Failed to commit')
            return False
    def close(self) -> None:
        self.conn.close()
    def add_user(self, username: str, password: str, email: str,UserType: User_type) -> None:
        insert_cmd = _insert_command('Users', ['Username', 'Password', 'Email','UserType'], [username, password, email,UserType.value])
        self.cur.execute(insert_cmd.evaluate())
        self.commit()
    def get_user_by_username(self, username: str):
        command = _select_command(['UserID'], 'Users', ['Username ='], [username])
        self.cur.execute(command.evaluate())
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None
    def update_user_email(self, user_id: int, new_email: str):
        command = _update_command('Users', ['Email'], [new_email], ['UserID ='], [user_id])
        print(command.evaluate())
        self.cur.execute(command.evaluate())
        self.commit()
    def update_user_password(self, user_id: int, new_password: str):
        command = _update_command('Users', ['Password'], [new_password], ['UserID ='], [user_id])
        self.cur.execute(command.evaluate())
        self.commit()
    def add_translation(self, user_id: int, translation_type: TranslationType, original_data: str, translated_data: str,OriginalLanguage : str,TranslatedLanguage: str,time: str) -> None:
        insert_cmd = _insert_command('Translation', ['UserID', 'translation_type', 'original_data', 'translated_data','OriginalLanguage', 'TranslatedLanguage', 'Time'], [user_id, translation_type.value, original_data, translated_data, OriginalLanguage, TranslatedLanguage, time])
        self.cur.execute(insert_cmd.evaluate())
        self.commit()
    def get_translation_by_UserID(self,UserID:int):
        command = _select_command(['*'],'Translation',['UserID ='],[UserID])
        self.cur.execute(command.evaluate())
        result = self.cur.fetchone()
        return result
    def delete_translation(self, translation_id: int) -> None:
        delete_cmd = _delete_command('Translation', ['id'], [translation_id])
        self.cur.execute(delete_cmd.evaluate())
        self.commit()