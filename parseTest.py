from urllib.parse import urlparse


result = urlparse('https://www.baidu.com/index.html;user?od=5#comment')
print(type(result),result)