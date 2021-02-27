import urllib.request
import socket
import urllib.error

#捕获timeout
try:
    response = urllib.request.urlopen('http://httpbin.org/get',timeout=0.01)
except urllib.error.URLError as e:
    if isinstance(e.reason,socket.timeout):
        print("TIME OUT")
