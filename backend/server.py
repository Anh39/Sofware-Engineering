import aiohttp,json
from aiohttp import web
from backend import folder_path
from backend.controller import routes,route_start

from aiohttp_apispec import setup_aiohttp_apispec

app = web.Application()

setup_aiohttp_apispec(
    app=app,
    title='My documentation',
    version='v1',
    url='/api/docs/swagger.json',
    swagger_path='/api/docs'
)

with open(folder_path.config,'r') as file:
    config = json.loads(file.read())
    
app.add_routes(routes)


def start(port : int = 8080):

    loop = route_start()
    web.run_app(app,host=config['server']['host'],port=int(config['server']['port']),loop=loop)

