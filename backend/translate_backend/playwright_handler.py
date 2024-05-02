import asyncio
import time
from playwright.async_api import async_playwright,Playwright,Browser,Page
from asyncio import Task

class PageManager:
    def __init__(self,page : Page) -> None:
        self._completed = True
        self.page : Page = page
    def done(self) -> bool:
        return self._completed
    async def complete_task(self,close_page : bool = False):
        if (close_page):
            await self.page.close()
        self._completed = True
    def start(self):
        self._completed = False
class Handler:
    def __init__(self) -> None:
        self.to_text_field_xpath = "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div[1]/div[6]/div/div[1]/span[1]/span/span"
        self.interval = 0.1
        self.driver : Playwright.chromium = None
        self.browser : Browser = None
        self.pools : list[PageManager] = []
        self.init_pool : int = 64
    async def init(self):
        self.playwright_content_manager= async_playwright()
        self.playwright = await self.playwright_content_manager.start()
        self.browser = await self.playwright.chromium.launch()
        for i in range(self.init_pool):
            await self.new_page()
    async def new_page(self):
        page = await self.browser.new_page()
        new_page_manager = PageManager(page)
        self.pools.append(new_page_manager)
    async def close(self):
        await self.browser.close()
        await self.playwright_content_manager.__aexit__()
    async def get_available(self,auto_create : bool = True):
        for manager in self.pools:
            if (manager.done()):
                return manager
        if (auto_create == True):
            await self.new_page()
            return self.pools[-1]
        else:
            return None
    async def _translate(self,page : Page,content : str,from_lang : str = 'en',to_lang : str = 'vi'):
        prompt = f"https://translate.google.com/?sl={from_lang}&tl={to_lang}&text={content}&op=translate"
        # start = time.time()
        await page.goto(prompt)
        # print('END',time.time()-start)
        output_text_area = await page.wait_for_selector('/'+self.to_text_field_xpath)
        # print(output_text_area)
        result = await output_text_area.inner_text()
        # print(result)
        return result
    async def translate(self,content : str,from_lang : str = 'en',to_lang : str = 'vi'):
        page_manager = await self.get_available()
        page_manager.start()
        result = await self._translate(page_manager.page,content,from_lang,to_lang)
        await page_manager.complete_task()
        return result