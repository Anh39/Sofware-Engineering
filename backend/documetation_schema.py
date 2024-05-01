from aiohttp_apispec import setup_aiohttp_apispec,docs,request_schema,headers_schema
from apispec import APISpec
from marshmallow import Schema, fields

class RequestSchema(Schema):
    # id = fields.Int()
    # name = fields.Str(description="name")
    pass

class ValidationSchema(Schema):
    ssid = fields.Str(description='Session ID của người dùng.')
    
class LoginSchema(Schema):
    username = fields.Str(description='Tên đăng nhập của người dùng.')
    password = fields.Str(description='Mật khẩu của người dùng.')
class RegisterSchema(Schema):
    username = fields.Str(description='Tên đăng nhập của người dùng.')
    password = fields.Str(description='Mật khẩu của người dùng.')
    email = fields.Str(description='Email của người dùng.')
class ResetPasswordSchema(Schema):
    username = fields.Str(description='Tên đăng nhập của người dùng.')
    
class GetHistorySchema(Schema):
    from_item = fields.Int(description='Bắt đầu từ bản ghi.')
    amount = fields.Int(description='Số bản ghi lấy về.')
class GetSavedSchema(Schema):
    from_item = fields.Int(description='Bắt đầu từ bản ghi.')
    amount = fields.Int(description='Số bản ghi lấy về.')
class SaveSchema(Schema):
    from_lang = fields.Str(description='Ngôn ngữ của nội dung')
    to_lang = fields.Str(description='Ngôn ngữ cần được dịch sang')
    from_content = fields.Str(description='Nội dung cần được dịch')
    to_content = fields.Str(description='Nội dung đã được dịch')

class TranslationResponseSchema(Schema):
    from_lang = fields.Str(description='Ngôn ngữ của nội dung')
    to_lang = fields.Str(description='Ngôn ngữ cần được dịch sang')
    from_content = fields.Str(description='Nội dung cần được dịch')
    to_content = fields.Str(description='Nội dung đã được dịch')
class MultiTranslationResponseSchema(Schema):
    translations = fields.List(fields.Nested(TranslationResponseSchema),description='Các bản dịch')
class TranslationResponseShortSchema(Schema):
    text = fields.Str(description='Bản dịch')
    
class TranslateTextSchema(Schema):
    from_lang = fields.Str(description='Ngôn ngữ của nội dung')
    to_lang = fields.Str(description='Ngôn ngữ cần được dịch sang')
    from_content = fields.Str(description='Nội dung cần được dịch')
    

    