from translate import Translator
from backend.lib import Language

class Handler:
    Trans_VI_EN = Translator(from_lang="vi",to_lang="en")
    Trans_EN_VI = Translator(from_lang="en",to_lang="vi")
    @classmethod
    def __translate_en(self,text : str):
        return self.Trans_EN_VI.translate(text)
    @classmethod
    def __translate_vi(self,text : str):
        return self.Trans_VI_EN.translate(text)
    @classmethod
    def translate(self,from_lang,to_lang,text):
        if (from_lang == Language.English and to_lang == Language.Vietnamese):
            return self.__translate_en(text)
        elif (from_lang == Language.Vietnamese and to_lang == Language.English):
            return self.__translate_vi(text)
        return text+"'ERROR'"