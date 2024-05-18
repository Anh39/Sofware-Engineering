import asyncio
import os
import aiohttp
from aiohttp import web
import json
from backend.common import folder_path,common
from backend.server.model import TranslationRequest,TranslationResponse

config = common.get_config()

class TranslateAPI:
    def __init__(self) -> None:
        self.base_url = common.get_url(config['translate_server'])
        self.session : aiohttp.ClientSession = None
    def start(self) :
        self.session = aiohttp.ClientSession(self.base_url)
    async def stop(self) :
        await self.session.close()
        self.session = None
    async def get_models(self) -> list[str]:
        try:
            async with self.session.get(url='/models') as response:
                if (response.status == 200):
                    result = await response.json()
                    return result
                else:
                    print(f'Error : {response.status}')
                    return None
        except Exception as e:
            print(e)
            return None
    async def translate_test(self,translation_request : TranslationRequest) -> TranslationResponse:
        try:
            async with self.session.get(url='/translate_text',data=translation_request.model_dump_json()) as response:
                if (response.status == 200):
                    result = await response.json()
                    return TranslationResponse.model_validate(result)
                else:
                    print(f'Error : {response.status}')
                    return None
        except Exception as e:
            print(e)
            return None