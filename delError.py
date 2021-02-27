from urllib.error import HTTPError
from urllib import request
try:
    response = request.urlopen("https://cuiqingcai.com/index.html")
except HTTPError as e:
    print(e.code,e.reason,e.headers,sep='\n')