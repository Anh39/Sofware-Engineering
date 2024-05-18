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

class Handler :
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
    def add_RegisteredUser(self, username: str, password: str, email: str) -> None:
        insert_cmd = _insert_command('RegisteredUser', ['Username', 'Password', 'Email'], [username, password, email])
        self.cur.execute(insert_cmd.evaluate())
        self.commit()
    def get_user_by_username(self, username: str):
        command = _select_command(['*'], 'RegisteredUser', ['Username ='], [username])
        self.cur.execute(command.evaluate())
        result = self.cur.fetchone()
        return result
    def add_GuestUser(self, SSID: str):
        insert_cmd = _insert_command('GuestUser', ['SSID'], [SSID])
        self.cur.execute(insert_cmd.evaluate())
        self.commit()
    def get_user_by_SSID(self, SSID):
        command = _select_command(['*'], 'GuestUser', ['SSID ='], [SSID])
        self.cur.execute(command.evaluate())
        result = self.cur.fetchone()
        return result
    def get_all_RegisteredUser(self):
        cmd = 'SELECT * FROM RegisteredUser'
        self.cur.execute(cmd)
        result = self.cur.fetchall()
        return result
    def get_all_GuestUser(self):
        cmd = 'SELECT * FROM GuestUser'
        self.cur.execute(cmd)
        result = self.cur.fetchall()
        return result
    def update_RegisteredUser_email(self, user_name: str, new_email: str):
        command = _update_command('RegisteredUser', ['Email'], [new_email], ['Username ='], [user_name])
        self.cur.execute(command.evaluate())
        self.commit()
    def update_RegisteredUser_password(self, user_name: str, new_password: str):
        command = _update_command('RegisteredUser', ['Password'], [new_password], ['Username ='], [user_name])
        self.cur.execute(command.evaluate())
        self.commit()
    def add_translation(self, translation_type: TranslationType, original_data: str, translated_data: str,OriginalLanguage : str,TranslatedLanguage: str,time: str,saved : bool,tags : str,username :str,SSID :str) -> None:
        insert_cmd = _insert_command('Translation', ['translation_type', 'original_data', 'translated_data','OriginalLanguage', 'TranslatedLanguage', 'Time','Saved','Tags','Username','SSID'], [translation_type.value, original_data, translated_data, OriginalLanguage, TranslatedLanguage, time,saved ,tags, username,SSID])
        self.cur.execute(insert_cmd.evaluate())
        self.commit()
    def get_translation_by_Username(self,username: str):
        command = _select_command(['*'],'Translation',['Username ='],[username])
        self.cur.execute(command.evaluate())
        result = self.cur.fetchall()
        return result
    def get_translation_by_SSID(self,SSID: str):
        command = _select_command(['*'],'Translation',['SSID ='],[SSID])
        self.cur.execute(command.evaluate())
        result = self.cur.fetchall()
        return result
    def delete_translation(self, translation_id: int) -> None:
        delete_cmd = _delete_command('Translation', ['id'], [translation_id])
        self.cur.execute(delete_cmd.evaluate())
        self.commit()