from abc import abstractmethod
import aiohttp,asyncio
from urllib.parse import urlencode,quote
from backend.translate_backend.playwright_handler import Handler

class BaseAPI:
    name = 'Base'
    base_url = ''
    def __init__(self) -> None:
        self.session = aiohttp.ClientSession(self.base_url)
    async def close(self):
        await self.session.close()
    @abstractmethod
    def translate(self,content : str,from_lang : str = 'en',to_lang : str = 'vi'):
        return None
    
class MyMemoryAPI(BaseAPI):
    name = 'MyMemory'
    base_url = 'https://api.mymemory.translated.net'
    def __init__(self,email : str = None) -> None:
        super().__init__()
        self.email = email
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
            
            
        