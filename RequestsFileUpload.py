import requests


file = open('favicon.ico','rb')
r = requests.post('http://httpbin.org/post')
print(r.text)
