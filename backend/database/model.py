from pydantic import BaseModel
from backend.server.model import *

class TranslationRecordTokenized(BaseModel):
    token : str
    record : TranslateRecord
class Token(BaseModel):
    token : str
class TokenizedUser(BaseModel):
    token : str
    user : RegistedUser | Guest
class TokenizedId(BaseModel):
    token : str
    id : int
    
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey,Column
from sqlalchemy import String,DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime   

class Base(DeclarativeBase):
    pass
    
class User(Base):
    __tablename__ = "user"
    
    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    type_name : Mapped[str]
    token : Mapped[str] = mapped_column(unique=True)
    username : Mapped[str] 
    password : Mapped[str]
    email : Mapped[str] 
    
    have_history : Mapped[Optional[List["TranslationRecord"]]] = relationship(
        cascade="all, delete-orphan"
    )
    have_saved : Mapped[Optional[List["TranslationRecord"]]] = relationship(
        cascade="all, delete-orphan"
    )
    
    @classmethod
    def model_validate(cls,data : dict[str,object]) -> "User":
        user = User()
        user.type_name = data['type_name']
        user.token = data['token']
        user.username = data.get('username',None)
        user.password = data.get('password',None)
        user.email = data.get('email',None)
        return user
    def model_dump(self) -> dict[str,object]:
        result = {
            'id' : self.id,
            'type_name' : self.type_name,
            'token' : self.token,
            'username' : self.username,
            'password' : self.password,
            'email' : self.email
        }
        return result
    
class TranslationRecord(Base):
    __tablename__ = "translation_record"
    
    id : Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    record_type : Mapped[str]
    user_token : Mapped[str] = mapped_column(ForeignKey("user.token",ondelete="CASCADE",onupdate="CASCADE"))
    from_language : Mapped[str]
    to_language : Mapped[str]
    from_content : Mapped[str]
    to_content : Mapped[str]
    engine_used : Mapped[str]
    time_created = Column(DateTime)
    
    @classmethod
    def model_validate(cls,data : dict[str,object]) -> "TranslationRecord":
        record = TranslationRecord()
        record.record_type = data.get('record_type')
        record.user_token = data.get('user_token')
        record.from_language = data.get('from_language')
        record.to_language = data.get('to_language')
        record.to_content = data.get('to_content')
        record.from_content = data.get('from_content')
        record.engine_used = data.get('engine_used')
        record.time_created = datetime.now()
        return record
    def model_dump(self) -> dict[str,object]:
        result = {
            'id' : self.id,
            'record_type' : self.record_type,
            'user_token' : self.user_token,
            'from_language' : self.from_language,
            'to_language' : self.to_language,
            'from_content' : self.from_content,
            'to_content' : self.to_content,
            'engine_used' : self.engine_used
        }
        return result