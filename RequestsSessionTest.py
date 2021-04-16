import requests

session = requests.Session()
session.get('http://httpbin.org/cookies/set/number/123123123')
res = session.get('http://httpbin.org/cookies')
print(res.text)