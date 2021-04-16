from bs4 import BeautifulSoup
import re

with open ('bs4Test.html','r') as html:
    html = BeautifulSoup(html,'lxml')
    lis = html.find_all('li')
    for li in lis:
        print(li.string)
    print(html.find_all(text=re.compile('link')))