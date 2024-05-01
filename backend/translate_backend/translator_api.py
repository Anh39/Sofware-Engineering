from abc import abstractmethod
import aiohttp,asyncio
from urllib.parse import urlencode,quote

class BaseAPI:
    name = 'Base'
    base_url = ''
    def __init__(self,from_lang : str = 'en',to_lang : str = 'vi') -> None:
        self.from_lang : str = from_lang
        self.to_lang : str = to_lang
        self.session = aiohttp.ClientSession(self.base_url)
    async def close(self):
        await self.session.close()
    @abstractmethod
    def translate(self,content : str):
        return None
    
class MyMemoryAPI(BaseAPI):
    name = 'MyMemory'
    base_url = 'https://api.mymemory.translated.net'
    def __init__(self, from_lang: str = 'en', to_lang: str = 'vi',email : str = None) -> None:
        super().__init__(from_lang, to_lang)
        self.email = email
    async def translate(self,content : str):
        params = {'q' : content,'langpair' : '{}|{}'.format(self.from_lang,self.to_lang)}
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
            
            
        