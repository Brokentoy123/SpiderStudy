import re
import requests
import os
from http import cookiejar
from urllib import request as urlreq, response

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
}
cookie = cookiejar.CookieJar()
handler = urlreq.HTTPCookieProcessor(cookiejar)
r = requests.get('https://www.zhihu.com/explore',headers=headers) #没有登录，就无法使用
opener = urlreq.build_opener(handler)
res = opener.open('https://www.zhihu.com/explore')
print(res)
pattern = re.compile('[*<a.*?>(.*)</a>.*]',re.S)
titles = re.findall(pattern,r.text)

file = open("/Users/shiqinghua/Desktop/zhihu.html",'w')
file.write(r.text)
# print(r.text)