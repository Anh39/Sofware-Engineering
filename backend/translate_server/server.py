from fastapi import FastAPI,Request,Response,HTTPException,Query,Cookie,Header
from backend.server.model import *
from backend.common import common
from backend.translate_server.translator_server_api import *
import uvicorn

app = FastAPI()

models : dict[str,BaseAPI] = {}

async def init():
    global models
    models = {
        'google' : GooglePlaywrightAPI(),
        'mymemory' : MyMemoryAPI(),
        'gpt3.5' : OpenAIAPI() ,
        'gpt4' : OpenAIAPI4()
    }
    unavailable_models = []
    for key in models:
        model = models[key]
        heathy = await model.start()
        if (not heathy):
            unavailable_models.append(key)
            print(key,"not available")
    for key in unavailable_models:
        models.pop(key)
    if (len(models) == 0):
        print('NO MODEL AVAILABLE')
        raise Exception

model_not_found_resonse = {401 : {"model" : str, "description" : "Model not found"}}
@app.get("/")
async def root():
    return {"message" : "Konnichiwa Sekai!"}

@app.get('/models',tags=['Metadata'])
async def get_models() -> list[str]:
    return list(models.keys())

@app.post('/translate/text',tags=['Translate'],responses=model_not_found_resonse)
async def translate_test(
    data : TranslationRequest
) -> TranslationResponse:
    engine = data.engine
    if (data.engine == 'auto'):
        if ('mymemory' in models):
            engine = 'mymemory'
        else:
            for key in models:
                engine = key
                break
    if (engine in models):
        result = await models[engine].translate(
            content = data.from_content,
            from_language = data.from_language,
            to_language = data.to_language
        )
        response = TranslationResponse(to_content=result,engine_used=engine)
        return response
    else:
        raise HTTPException(status_code=404,detail='Model not found')
    
app.add_event_handler('startup',init)    

def start():
    config = common.get_config('translate_server')
    uvicorn.run(app,host=config['host'],port=config['port'])

async def async_start():
    config = common.get_config('translate_server')
    server_config = uvicorn.Config(app,host=config['host'],port=config['port'])
    server = uvicorn.Server(server_config)
    await server.serve()