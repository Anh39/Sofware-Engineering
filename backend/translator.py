from enum import Enum
from backend.translate_backend.translate_lib_api import Handler
from backend.lib import Language


class Translator:
    """Lớp xử lý việc dịch

    """
    backend = Handler()
    lang_map = {
        'EN' : Language.English,
        'VN' : Language.Vietnamese,
        'English' : Language.English,
        'Vietnamese' : Language.Vietnamese
    }
    def __init__(self) -> None:
        pass
    def translate(self,
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
        from_language = self.lang_map[from_language]
        to_language = self.lang_map[to_language]
        result = self.backend.translate(from_language,to_language,text=input_text)
        return result