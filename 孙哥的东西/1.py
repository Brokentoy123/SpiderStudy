from selenium import webdriver
import time
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
import cv2
import requests
import numpy as np
import json
import os
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
import tkinter


def getScreamSize():
    # 通过tkinter获取屏幕大小
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    print(width, height)
    tk.quit()
    return width, height


# 保存cookie维持会话状态，失败了
def saveCookies(browser):
    cookies = browser.get_cookies()
    with open(cookiesFile, 'w') as cookie:
        json.dump(cookies, cookie)


def setAttribute(browser, element, name, value):
    browser.execute_script(
        "arguments[0].setAttribute(arguments[1],arguments[2])", element, name, value)


def getImgPos(src1, src2):
    print('path:', path)
    slide_bkg_png = os.path.join(path, 'slide_bkg.png')
    slide_block_png = os.path.join(path, 'slide_block.png')
    img1 = requests.get(src1, headers=header).content
    with open(slide_bkg_png, 'wb')as f:
        f.write(img1)
    img2 = requests.get(src2, headers=header).content
    with open(slide_block_png, 'wb')as f:
        f.write(img2)

    # 使用python的OpenCV模块识别滑动验证码的缺口
    block = cv2.imread(slide_block_png, 0)
    template = cv2.imread(slide_bkg_png, 0)


    cv2.imwrite('template.jpg', template)
    cv2.imwrite('block.jpg', block)
    block = cv2.imread('block.jpg')
    template = cv2.imread('template.jpg')
    bg_edge = cv2.Canny(template, 100, 200)
    tp_edge = cv2.Canny(block, 100, 200)
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    # cv2.imshow('bg_pic', bg_pic)
    # cv2.imshow('tp_pic', tp_pic)
    # cv2.waitKey(0)

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    X = (max_loc[0]+min_loc[0])/2
    Y =(max_loc[1]+min_loc[1])/2
    print("x:", X, "y:", Y)
    th, tw = tp_pic.shape[:2]

    tl = max_loc  # 左上角点的坐标

    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标

    cv2.rectangle(template, tl, br, (0, 0, 255), 2)  # 绘制矩形

    cv2.imwrite('out.jpg', template)  # 保存在本地
    return X


def getcookies_decode_to_dict(browser):
    path = os.path.abspath('cookies.txt')
    if not os.path.exists(path):
        print('Cookie文件不存在，请先运行cookiesload.py')
    else:
        cookies_dict = {}
    with open(path, 'r') as f:
        cookies = json.load(f)

    for i in cookies:
        print(i)


def get_track(distance):
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 0
    while current < distance:
        if current < mid:
            # 加速度为正2
            a = 2
        else:
            # 加速度为负3
            a = -3
        # 初速度为v0
        v0 = v
        # 当前速度v = v0+at
        v = v0 + a * t
        # 移动距离x = v0t+1/2*a*t*t
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        track.append(round(move))
    return track


def input_time_random():
    return random.randint(100, 151)

async def _injection_js(page):
        """注入js
        """
        await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,''{ webdriver:{ get: () => false } }) }')  # 本页刷新后值不变
        await page.evaluateOnNewDocument('() => {window.navigator.chrome = {runtime: {},// etc.};}')
        await page.evaluateOnNewDocument('() =>{Object.defineProperty(navigator, "plugins", {get: () => [1, 2, 3, 4, 5,6],});}')

if __name__ == '__main__':
    url = "https://www.oceanengine.com"
    user = "976004996@qq.com"
    password = "Szh976004996"
    cookiesFile = 'cookies.txt'
    path = os.path.abspath(os.path.curdir)
    if os.path.exists(os.path.abspath(cookiesFile)):
        pass
    else:
        file = open(os.path.abspath(cookiesFile), 'w')
        file.close()

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 隐藏window.navigator.webdriver
    option.add_argument("--disable-blink-features=AutomationControlled")
    # 添加user-agent
    # option.add_argument(
    #     'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
    header = {}
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    # }
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
    ]

    header['User-Agent'] = random.choice(user_agent_list)
    headerString = "user-agent=" + header.get('User-Agent')
    option.add_argument(headerString)

    # browser = webdriver.Chrome(options=option)
    # browser = webdriver.Safari()
    # wait = WebDriverWait(browser, 5)

    async def main():
        js1 = '''() =>{
                Object.defineProperties(navigator,{
                webdriver:{
                    get: () => false
                    }
                })
            }'''

        webdriver_js = '''() =>{
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }
'''

        browser = await launch({'headless': False, 'userDataDir': 'D:\\temporary', 'args': ['--no-sandbox', '--start-maximized'], })

        page = await browser.newPage()
        width, height = getScreamSize()
        # print(width, height)
        await page.setViewport({  # 最大化窗口
            "width": width,
            "height": height
        })
        print("设置最大化")
        # 设置请求头userAgent
        await page.setUserAgent(header.get('User-Agent'))
        await page.goto('https://e.oceanengine.com/account/page/service/login?from=https%3A%2F%2Fwww.oceanengine.com%2F', {"waitUntil": 'networkidle2'})
        await page.evaluate(js1)
        _injection_js(page)
        # await page.evaluate(webdriver_js)
        print("执行js1")
        await asyncio.sleep(2)

        # 输入账号密码
        mailInput = await page.xpath('//input[@name="email"]')
        # 输入密码
        passwordInput = await page.xpath('//input[@name="password"]')
        await mailInput[0].type(user)
        # await page.type(user)
        await passwordInput[0].type(password)
        # await page.type(passwordInput, password, input)
        await asyncio.sleep(3)
        # 输入账号密码后登录
        loginBtn = await page.xpath('//*[@id="account-sdk"]/section/div[6]/button')
        # print(loginBtn)
        await loginBtn[0].click()
        await asyncio.sleep(1)
        frame = page.frames
        img1 = await page.xpath('//img[contains(@id,"captcha-verify-image")]')
        img2 = await page.xpath('//img[contains(@class,"captcha_verify_img_slide")]')
        # 后面的进度条
        back_bar = await page.xpath('//*[@id="account-sdk-slide-container"]/div/div[3]/div[1]/span')

        # print(img1[0].getProperty('src').jsonValue(),img2[0].getProperty('src').jsonValue())
        img1Src = await(await img1[0].getProperty('src')).jsonValue()
        print('img1Src序列化')
        img2Src = await(await img2[0].getProperty('src')).jsonValue()
        print('imgSrc2序列化')
        X = getImgPos(img1Src, img2Src)
        track = get_track(X)
        await page.hover('.secsdk-captcha-drag-icon')
        slider = await page.xpath('//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
        sliderInfo = await slider[0].boundingBox()
        mouse = page.mouse

        print("sliderInfo:",sliderInfo)
        await mouse.move(sliderInfo['x'], sliderInfo['y'])
        await mouse.down()
        sum = 0
        for i in track:
            sum = sum + i
            await mouse.move(sliderInfo['x']+sum/1.62,sliderInfo['y']+i)
            print(mouse._x)
        
        # await mouse.move(sliderInfo['x']+X+45,sliderInfo['y'] + 30)
        await asyncio.sleep(0.3)
        # 松开鼠标
        await mouse.up()
        time.sleep(100)

    asyncio.get_event_loop().run_until_complete(main())
    # 手动登录，获取cookie信息
    # getCookie()
