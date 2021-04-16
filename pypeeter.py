import asyncio
from pyppeteer import launch
 
 
async def main():
    browser = await launch(headless=False, args=['--disable-infobars', '--no-sandbox'])
    page = await browser.newPage()
    await page.goto('http://www.baidu.com')
    await asyncio.sleep(100)
    await browser.close()
