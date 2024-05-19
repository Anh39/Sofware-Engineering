from abc import abstractmethod
from backend.database.model import TranslateRecord
from backend.server.model import *
from backend.server.model import Guest, RegistedUser, TranslateRecord

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
    
from sqlalchemy import create_engine,select,delete,update,func,asc,desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from backend.database.model import *
from backend.common import folder_path

class DatabaseHandler(Handler):
    def start(self) -> None:
        path = folder_path.util.to_relative(folder_path.database.database,folder_path._project_path)
        path = folder_path.join('backend',path)
        self.engine = create_engine("sqlite:///"+path,echo=True)
        Base.metadata.create_all(self.engine)
    def add_user(self, user: RegistedUser | Guest) -> bool:
        with Session(self.engine) as session:
            data = user.model_dump()
            new_user = User.model_validate(data)
            session.add(new_user)
            try:
                session.commit()
                return True
            except IntegrityError as e:  
                print("Failed to push User : ",e)
                return False
    def get_user(self, search: dict[str, object] = { 'token': None,'username': None,'email': None }) -> RegistedUser | Guest | None:
        with Session(self.engine) as session:
            query = select(User)
            if (search.get('username',None) != None):
                query = query.where(User.username == search['username'])
            if (search.get('token',None) != None):
                query = query.where(User.token == search['token'])
            if (search.get('email',None) != None):
                query = query.where(User.email == search['email']) 
            query_result = session.execute(query)
            query_result = query_result.fetchall()
            result = []
            for row in query_result:
                dict_result = row[0].model_dump()
                if (dict_result['type_name'] == 'Guest'):
                    user = Guest.model_validate(dict_result)
                else:
                    user = RegistedUser.model_validate(dict_result)
                result.append(user)
            if (len(result) > 0):
                return result[0]
            return None
    def update_user(self, token: str, user: Guest | RegistedUser) -> None:
        with Session(self.engine) as session:
            query = select(User)
            query = query.where(User.token == token)
            query_result = session.execute(query)
            query_result = query_result.fetchall()
            for row in query_result:
                old_user = row[0]
                for key, value in user:
                    setattr(old_user, key,value)
                session.commit()
                return True
        return False
    def delete_user(self, token) -> None:
        with Session(self.engine) as session:
            query = delete(User)
            query = query.where(User.token == token)
            session.execute(query)
            session.commit()
            return True
    def add_translation_history(self, token: str, record: TranslateRecord) -> None:
        with Session(self.engine) as session:
            data = record.model_dump()
            data.update(
                {
                    'record_type' : 'history',
                    'user_token' : token
                }
            )
            new_record = TranslationRecord.model_validate(data)
            session.add(new_record)
            try:
                session.commit()
                return True
            except IntegrityError as e:  
                print("Failed to push User : ",e)
                return False
    def get_translation_history(self, token: str) -> list[TranslateRecord]:
        with Session(self.engine) as session:
            query = select(TranslationRecord)
            query = query.where(TranslationRecord.user_token == token)
            query = query.where(TranslationRecord.record_type == 'history')
            query_result = session.execute(query)
            query_result = query_result.fetchall()
            result = []
            for row in query_result:
                dict_result = row[0].model_dump()
                print(dict_result)
                record = TranslateRecord.model_validate(dict_result)
                result.append(record)
            return result
    def delete_translation_history(self, token: str, id : int) -> None:
        with Session(self.engine) as session:
            record = session.query(TranslateRecord).where(TranslateRecord.id == id).first()[0]
            if (record.user_token == token):
                session.delete(record)
            # id+=1
            # subquery = session.query(TranslationRecord.id,TranslationRecord.time_created).where(TranslationRecord.user_token == token).where(TranslationRecord.record_type == 'history').order_by(TranslationRecord.time_created.desc()).limit(id).subquery()
            # target_id = session.query(subquery.c.id).order_by(subquery.c.time_created.asc()).first()[0]
            # target_to_delete = session.query(TranslationRecord).filter(TranslationRecord.id == target_id).one()
            # session.delete(target_to_delete)
            session.commit()
            return True
    def add_translation_saved(self, token: str, record: TranslateRecord) -> None:
        with Session(self.engine) as session:
            data = record.model_dump()
            data.update(
                {
                    'record_type' : 'save',
                    'user_token' : token
                }
            )
            new_record = TranslationRecord.model_validate(data)
            session.add(new_record)
            try:
                session.commit()
                return True
            except IntegrityError as e:  
                print("Failed to push User : ",e)
                return False
    def get_translation_saved(self, token: str) -> list[TranslateRecord]:
        with Session(self.engine) as session:
            query = select(TranslationRecord)
            query = query.where(TranslationRecord.user_token == token)
            query = query.where(TranslationRecord.record_type == 'save')
            query_result = session.execute(query)
            query_result = query_result.fetchall()
            result = []
            for row in query_result:
                dict_result = row[0].model_dump()
                print(dict_result)
                record = TranslateRecord.model_validate(dict_result)
                result.append(record)
            return result
    def delete_translation_saved(self, token: str, id : int) -> None:
        with Session(self.engine) as session:
            record = session.query(TranslationRecord).where(TranslationRecord.id == id).first()
            if (record.user_token == token):
                session.delete(record)
            # id += 1
            # subquery = session.query(TranslationRecord.id,TranslationRecord.time_created).where(TranslationRecord.user_token == token).where(TranslationRecord.record_type == 'save').order_by(TranslationRecord.time_created.desc()).limit(id).subquery()
            # target_id = session.query(subquery.c.id).order_by(subquery.c.time_created.asc()).first()[0]
            # target_to_delete = session.query(TranslationRecord).filter(TranslationRecord.id == target_id).one()
            # session.delete(target_to_delete)
            session.commit()
            return True