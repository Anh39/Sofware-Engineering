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
        
class util:
    @classmethod
    def get_tree(self,folder_path : str):
        temp_result = set()
        self._recurse_get_file(temp_result,folder_path)
        result = {}
        for key in temp_result:
            result[os.path.normpath(self.to_relative(key,folder_path))] = key
        return result
    @classmethod
    def to_relative(self,path : str,relto : str):
        relpath = os.path.relpath(path,relto)
        return relpath
    @classmethod
    def _recurse_get_file(self,result : set,input_path : str):
        for file_name in os.listdir(input_path):
            file_path = join(input_path,file_name)
            if (os.path.isdir(file_path)):
                self._recurse_get_file(result,file_path)
            else:
                result.add(file_path)