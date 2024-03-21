from enum import Enum

class Language(Enum):
    """Lớp Enum chứa các loại ngôn ngữ khả dụng
    """
    English = 'English'
    Vietnamese = 'Vietnamese'

class Translator:
    """Lớp xử lý việc dịch

    """
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
        return input_text+'translated'