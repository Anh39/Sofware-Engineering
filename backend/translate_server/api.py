import asyncio
import os
import aiohttp
from aiohttp import web
import json
from backend.common import folder_path,common
from backend.server.model import TranslationRequest,TranslationResponse
from fastapi import HTTPException

config = common.get_config()
headers = {
    "Content-Type": "application/json"
}

class TranslateAPI:
    def __init__(self) -> None:
        self.base_url = common.get_url(config['translate_server'])
        self.session : aiohttp.ClientSession = None
    def start(self) :
        self.session = aiohttp.ClientSession(self.base_url)
    async def stop(self) :
        await self.session.close()
        self.session = None
    async def get_models(self) -> list[str] | HTTPException:
        try:
            async with self.session.get(url='/models') as response:
                if (response.status == 200):
                    result = await response.json()
                    return result
                else:
                    print(f'Error : {response.status}')
                    return HTTPException(status_code=response.status,detail= await response.text())
        except Exception as e:
            print(e)
            return None
    async def translate_test(self,translation_request : TranslationRequest) -> TranslationResponse | HTTPException:
        try:
            async with self.session.post(url='/translate/text',headers=headers,data=translation_request.model_dump_json()) as response:
                if (response.status == 200):
                    result = await response.json()
                    return TranslationResponse.model_validate(result)
                else:
                    print(f'Error : {response.status}')
                    return HTTPException(status_code=response.status,detail= await response.text())
        except Exception as e:
            print(e)
            return None