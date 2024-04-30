from translate import Translator
import time
from typing import Dict
import threading
import asyncio
import uuid

class Handler:
    translators : {tuple,Translator} = {} 
    all_jobs = set()
    last_job = None
    
    @classmethod
    def _create_translator(self,lang : tuple): 
        return Translator(from_lang=lang[0],to_lang=lang[1])
    @classmethod
    async def concurent_translate(self,from_lang,to_lang,text):
        id = str(uuid.uuid4())
        self.last_job = id
        self.all_jobs.add(self.last_job)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None,self.translate,from_lang,to_lang,text)
        self.all_jobs.remove(id)
        if (id == self.last_job):
            while True:
                await asyncio.sleep(0.5)
                if (len(self.all_jobs) == 0 and id != self.last_job):
                    continue
                else:
                    break
        return result
            
    @classmethod
    def translate(self,from_lang,to_lang,text):
        lang = (from_lang,to_lang)
        if (lang not in self.translators):
            self.translators[lang] = self._create_translator(lang)
        start_time = time.time()
        result = self._create_translator(lang).translate(text)
        end_time = time.time()
        print(f'Translate time : {end_time-start_time}')
        return result