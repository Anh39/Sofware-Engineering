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
    id : int
    token : str