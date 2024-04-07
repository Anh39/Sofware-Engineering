from translate import Translator
import time

class Handler:
    translators = {}
    @classmethod
    def _create_translator(self,lang : tuple): 
        return Translator(from_lang=lang[0],to_lang=lang[1])
    @classmethod
    def translate(self,from_lang,to_lang,text):
        lang = (from_lang,to_lang)
        if (lang not in self.translators):
            self.translators[lang] = self._create_translator(lang)
        start_time = time.time()
        result = self.translators[lang].translate(text)
        end_time = time.time()
        print(f'Translate time : {end_time-start_time}')
        return result