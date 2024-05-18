from abc import abstractmethod
import json
import aiohttp,asyncio
from urllib.parse import urlencode,quote
from backend.translate_server.playwright_handler import Handler
from openai import AsyncOpenAI
import tiktoken
from enum import Enum
from backend.common import folder_path

try:
    with open(folder_path.apikey,'r') as file:
        apikey = json.loads(file.read())
except:
    print('OpenAI api key not found')
    apikey = {'openai' : None}
        
class BaseAPI:
    name = 'Base'
    async def start(self):
        print('Engine {} started.'.format(self.name))
        return True
    async def stop(self):
        print('Engine {} stopped.'.format(self.name))
    @abstractmethod
    async def translate(self,content : str,from_language : str = 'en-US',to_language :str = 'vi-VN'):
        return 'Base model'
class MyMemoryAPI(BaseAPI):
    name = 'MyMemory'
    base_url = 'https://api.mymemory.translated.net'
    def __init__(self,email : str = None) -> None:
        self.session = aiohttp.ClientSession(self.base_url)
        self.email = email
    async def stop(self):
        await self.session.close()
    async def translate(self,content : str,from_language : str = 'en-US',to_language : str = 'vi-VN'):
        params = {'q' : content,'langpair' : '{}|{}'.format(from_language,to_language)}
        if (self.email != None):
            params['de'] = self.email
        async with self.session.get(url='/get',params=params) as response:
            result = await response.json()
            translation = result['responseData']['translatedText']
            if translation:
                return translation
            else:
                matches = result['matches']
                if (len(matches) > 0):
                    return matches[0]['translation']
                else:
                    return 'ERROR'
                       
class GooglePlaywrightAPI(BaseAPI):
    name = 'Goggle Playwright'
    def __init__(self) -> None:
        self.handler = Handler()
    async def start(self):
        await self.handler.init()
        await super().start()
        return True
    async def translate(self,content : str,from_language : str = 'en-US',to_language : str = 'vi-VN'):
        result = await self.handler.translate(content,from_language[:2],to_language[:2])
        return result
                 
class OpenAIAPI(BaseAPI):
    name = 'GPT3.5'
    INIT_TOKEN = 3
    MESSAGE_TOKEN = 4
    ENCODER_NAME = 'cl100k_base'
    def __init__(self) -> None:
        self.encoder = tiktoken.get_encoding(self.ENCODER_NAME)
        self.client : AsyncOpenAI = None
        self.model = 'gpt-3.5-turbo-1106'
    async def start(self):
        await super().start()
        if (apikey['openai'] != None):
            self.client = AsyncOpenAI (
                api_key=apikey['openai']
            )
            return True
        return False
    async def translate(self,content : str,from_language : str = 'en-US',to_language : str = 'vi-VN'):
        stripped = content.strip()
        if (len(stripped) < 1):
            return ''
        try:
            chat_completion = await self.client.chat.completions.create(
                messages = [
                    {
                        'role' : 'system',
                        'content' : 'You are a translator. Provide translation only in json format : {"Translation" : "translated content"} . No comment or explaination.'
                    },
                    {
                        'role' : 'user',
                        'content' : 'Translate [Content] from "{}" to "{}". [Content] = "{}"'.format(from_language,to_language,content),
                    }
                ],
                model=self.model
            )
        except Exception as e:
            print('API or CONNECTION error. API key : {}'.format(apikey['openai']))
            return 'Server error'
            
        result = json.loads(chat_completion.model_dump_json())
        result = result['choices'][0]['message']['content']
        result = json.loads(result)
        result = result['Translation']
        return result
    
class OpenAIAPI4(OpenAIAPI):
    name = 'GPT4'
    def __init__(self) -> None:
        super().__init__()
        self.model = 'gpt-4-turbo-preview'
