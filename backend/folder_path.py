import os

join = os.path.join
_project_path = os.getcwd()

class backend:
    """Path(Đương dẫn) cho các thư mục, tệp trong thư mục backend
    """
    path = join(_project_path,'backend')
    controller = join(path,'controller.py')
    model = join(path,'model.py')
    translator = join(path,'translator.py')
    server = join(path,'server.py')
    user = join(path,'user.json')
class frontend:
    """Path(Đương dẫn) cho các thư mục, tệp trong thư mục frontend
    """
    path = join(_project_path,'frontend')
    class public:
        """Path(Đương dẫn) cho các thư mục, tệp trong thư mục public
        """
        path = join(_project_path,'frontend','public')
        index = join(path,'index.html')
        style = join(path,'style.html')
        client = join(path,'client.js')
        favicon = join(path,'favicon.ico')