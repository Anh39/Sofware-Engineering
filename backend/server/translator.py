from enum import Enum
from backend.translate_server.translator_api import *
from backend.common import folder_path
import json

class Lang:
    languages = {}
    initialized = False
    @classmethod
    def initialize(self):
        self.initialized = True
        # frontend_files = folder_path.util.get_tree(folder_path.frontend.path)

        # for key in frontend_files:
        #     if ("language.json" in key):
        #         language_file = frontend_files[key]
        with open(folder_path.common.language,'r') as file:
            languages_dict = json.loads(file.read())
        for key in languages_dict:
            self.languages[key] = key #.split('-')[0]
    
        
        
                
with open(folder_path.config,'r') as file:
    config = json.loads(file.read())

class Translator:
    """Lớp xử lý việc dịch

    """
    mapping = {
        "google_playwright" : GooglePlaywrightAPI,
        "mymemory_aiohttp" : MyMemoryAPI,
        "openai_chatgpt" : OpenAIAPI
    }
    def __init__(self) -> None:
        self.backend = self.mapping[config['translator']['backend']]()
        self.languages = Lang()
    async def init(self):
        try:
            await self.backend.init()
        except:
            pass
    async def translate(self,
                from_language : str,
                to_language : str,
                input_text : str = '') -> str:
        """Dịch đầu vào.

        Args:
            EN,English,VN,Vietnamese
            from_language (str): Dịch từ ngôn ngữ
            to_language (str): Dịch sang ngôn ngữ
            input_text (str, optional): Nội dung đầu vào. Defaults to ''.

        Returns:
            str: Kết quả
        """
        if (self.languages.initialized == False):
            self.languages.initialize()
        from_language = self.languages.languages[from_language]
        to_language = self.languages.languages[to_language]
        # print(from_language,to_language)
        result = await self.backend.translate(input_text,from_language,to_language)
        # if (self.languages.initialized == False):
        #     self.languages.initialize()
        # if (from_language in self.languages.languages and to_language in self.languages.languages):
        #     
        #     result = await self.backend.concurent_translate(from_language,to_language,text=input_text)
        #     return result
        return result