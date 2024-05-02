from abc import abstractmethod
import json
import aiohttp,asyncio
from urllib.parse import urlencode,quote
from backend.translate_backend.playwright_handler import Handler
from openai import AsyncOpenAI
import tiktoken
from enum import Enum
from backend import folder_path

with open(folder_path.config,'r') as file:
    config = json.loads(file.read())


class MyMemoryAPI:
    name = 'MyMemory'
    base_url = 'https://api.mymemory.translated.net'
    def __init__(self,email : str = None) -> None:
        self.session = aiohttp.ClientSession(self.base_url)
        self.email = email
    async def close(self):
        await self.session.close()
    async def translate(self,content : str,from_lang : str = 'en',to_lang : str = 'vi'):
        params = {'q' : content,'langpair' : '{}|{}'.format(from_lang,to_lang)}
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
                
class GooglePlaywrightAPI:
    name = 'Goggle Playwright'
    def __init__(self) -> None:
        self.handler = Handler()
    async def init(self):
        await self.handler.init()
    async def translate(self,content : str,from_lang : str = 'en',to_lang : str = 'vi'):
        result = await self.handler.translate(content,from_lang,to_lang)
        return result
            
class gpt_model(Enum):
        gpt35turbo = 'gpt-3.5-turbo-1106'
        gpt4turbo = 'gpt-4-turbo-preview'        
class OpenAIAPI:
    INIT_TOKEN = 3
    MESSAGE_TOKEN = 4
    ENCODER_NAME = 'cl100k_base'
    def __init__(self) -> None:
        self.encoder = tiktoken.get_encoding(self.ENCODER_NAME)
        self.client = AsyncOpenAI(
            api_key=config['translator']['openai_api_key']
        )
        self.model = 'gpt-3.5-turbo-1106'
    async def translate(self,content : str,from_lang : str = 'en',to_lang : str = 'vi'):
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
                        'content' : 'Translate [Content] from "{}" to "{}". [Content] = "{}"'.format(from_lang,to_lang,content),
                    }
                ],
                model=self.model
            )
        except Exception as e:
            print('API or CONNECTION error. API key : {}'.format(config['translator']['openai_api_key']))
            return 'Server error'
            
        result = json.loads(chat_completion.model_dump_json())
        result = result['choices'][0]['message']['content']
        result = json.loads(result)
        result = result['Translation']
        return result
