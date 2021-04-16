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




# 保存cookie维持会话状态，失败了
def saveCookies(browser):
    cookies = browser.get_cookies()
    with open(cookiesFile, 'w') as cookie:
        json.dump(cookies, cookie)


def getCookie():
    browser.maximize_window()
    browser.get(url)

    loginButton = browser.find_element_by_xpath('//a[@class="login operation-item"]')

    loginButton.click()

    time.sleep(2)
    # 输入账号密码
    mailInput = browser.find_element_by_xpath('//input[@name="email"]')
    # 输入密码
    passwordInput = browser.find_element_by_xpath('//input[@name="password"]')
    # 获取登录按钮
    loginBtn = browser.find_element_by_xpath('//button[@class="account-center-action-button"]')
    mailInput.send_keys(user)
    passwordInput.send_keys(password)
    loginBtn.click()
    time.sleep(2)
    # 获取验证码图片及其相应的偏移量
    y = get_img_pos()
    # print("y=", y, type(y))
    # 获取验证码滑块
    # button = browser.find_element_by_xpath('//*[@id="secsdk-captcha-drag-wrapper"]/div[2]/div')
    button = browser.find_element_by_xpath('//*[@id="secsdk-captcha-drag-wrapper"]/div[2]')
    # button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'secsdk-captcha-drag-wrapper')))
    print("btnlocation:",button.location)
    # ActionChains(browser).click_and_hold(on_element=button).perform()
    # 将偏移量转换为列表，通过循环列表来模拟人鼠标拖动的情况
    track = get_track(y)
    # transform是在拖动滑块时，style有变化的节点
    transform = browser.find_element_by_xpath('//*[@id="account-sdk-slide-container"]/div/div[2]/img[2]')
    print(track)
    # iframe = browser.find_element_by_xpath('//iframe')
    # browser.switch_to.frame(iframe)

    ActionChains(browser).click_and_hold(on_element=button).perform()
    # sum = 0
    for x in track:
        print("正在移动", x)
        # sum = sum + x
        # setAttribute(browser,transform,'style','transform:translate('+str(sum)+'px,0px)')
        ActionChains(browser).move_to_element_with_offset(to_element=button, xoffset=x, yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(browser).release().perform()

    # ActionChains(browser).move_to_element_with_offset(to_element=button, xoffset=int(y) * 0.4 + 18, yoffset=0).perform()
    # time.sleep(1)
    # ActionChains(browser).release(on_element=button).perform()
    time.sleep(20)

    saveCookies(browser=browser)

def setAttribute(browser,element,name,value):
    browser.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", element, name, value)

def get_img_pos():
    time.sleep(3)
    # browser.switch_to.frame(browser.find_element_by_id('tcaptcha_iframe'))
    image1 = browser.find_element_by_xpath('//img[contains(@id,"captcha-verify-image")]').get_attribute('src')  # 下载需要验证图
    image2 = browser.find_element_by_xpath('//img[contains(@class,"captcha_verify_img_slide")]').get_attribute(
        'src')  # 下载缺口图

    img1 = requests.get(image1, headers=header).content
    with open('slide_bkg.png', 'wb')as f:
        f.write(img1)
    img2 = requests.get(image2, headers=header).content
    with open('slide_block.png', 'wb')as f:
        f.write(img2)

    # 使用python的OpenCV模块识别滑动验证码的缺口
    block = cv2.imread('slide_block.png', 0)
    template = cv2.imread('slide_bkg.png', 0)

    cv2.imwrite('template.jpg', template)
    cv2.imwrite('block.jpg', block)
    block = cv2.imread('block.jpg')
    template = cv2.imread('template.jpg')
    bg_edge = cv2.Canny(template, 100, 200)
    tp_edge = cv2.Canny(block, 100, 200)
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)
    cv2.imshow('bg_pic', bg_pic)
    cv2.imshow('tp_pic', tp_pic)
    # cv2.waitKey(0)

    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    X = max_loc[1]
    Y = max_loc[0]
    print("x:",X,"y:",Y)
    th, tw = tp_pic.shape[:2]

    tl = max_loc  # 左上角点的坐标

    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标

    cv2.rectangle(template, tl, br, (0, 0, 255), 2)  # 绘制矩形

    cv2.imwrite('out.jpg', template)  # 保存在本地

    # block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
    # block = (255 - block)
    # cv2.imwrite('block.jpg', block)
    # block = cv2.imread('block.jpg')
    #
    # cv2.imshow('template.jps', template)
    # result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
    # x, y = np.unravel_index(result.argmax(), result.shape)
    # # 图片测试
    # print(np.unravel_index(result.argmax(), result.shape))
    # print(x, y)
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
    # for cookie in cookies:
    #     cookies_dict[cookie['name']] = cookie['value']

    # for cookie in cookies:
    #     cookie_dict = {
    #         'domain': '.oceanengine.com',
    #         'name': cookie.get('name'),
    #         'value': cookie.get('value'),
    #         "expires": '',
    #         'path': '/',
    #         'httpOnly': False,
    #         'HostOnly': False,
    #         'Secure': False
    #     }
    #     browser.add_cookie(cookie_dict)

    # print(cookies_dict)
    # browser.add_cookie(cookies_dict)


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


if __name__ == '__main__':
    url = "https://www.oceanengine.com"
    user = "976004996@qq.com"
    password = "Szh976004996"
    cookiesFile = 'cookies.txt'
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
    headerString = "user-agent="+header.get('User-Agent')
    option.add_argument(headerString)
    # browser = webdriver.Chrome(options=option)
    browser = webdriver.Safari()
    wait = WebDriverWait(browser, 5)

    # 手动登录，获取cookie信息
    getCookie()
    # 读取cookie
    # cookieFile = open(os.path.abspath('cookies.txt'))
    # getcookies_decode_to_dict(browser)
    # response = requests.get(url=url, headers=header)
    # browser.get(url)
    # if "立即登录" in response.text:
    #     "登录失败"
    # else:
    #     "登录成功"
