import aiohttp
from aiohttp import web
from backend import folder_path
from backend.controller import routes,route_start



app = web.Application()
app.add_routes(routes)
def start(port : int = 8080):
    """Khởi động sever

    Args:
        port (str, optional): Vị trí port, mặc định là 8080.
    """
    loop = route_start()
    web.run_app(app,host='127.0.0.1',port=port,loop=loop)

