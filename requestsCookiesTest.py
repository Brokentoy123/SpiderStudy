import requests
import http

# r = requests.get("https://www.baidu.com")
cookies = 'Cookie: JOID=UVgWC0u3c0W7p9YqWLzTUYNnsXJKzgo42_2NcCfxQSfi36R-A2vaedCn1iJbzaEkGUWNMmhkJMrADIUe2A3cDKQ=; KLBRSID=ca494ee5d16b14b649673c122ff27291|1614782940|1614782938; SESSIONID=zzvhYXYtE1aRpqWXGH9HfUK75CgGd9D7Ktf4b5mrA4u; osd=UVkUBUy3cke1oNYrWrLUUYJlv3VKzwg23P2Mcin2QSbg0aN-AmnUftCm1CxczaAmF0KNM2pqI8rBDosZ2AzeAqM=; tst=r; _xsrf=0205c112-5111-41f7-9b35-b73ec286680e; q_c1=e91426238f504ed9b0f24b278fd42240|1614488347000|1614488347000; z_c0="2|1:0|10:1614427056|4:z_c0|92:Mi4xTGpTM0F3QUFBQUFBd05kb3dXeFlFaVlBQUFCZ0FsVk5zSUVuWVFCc0JUSjBuc2VqMG5xX1BSNzhpTmt3R3pSWV9B|865ea86e31730729fabaf460407f7b2bcf1e91acee3a1712049a9a6e7eb93ddf"; captcha_ticket_v2="2|1:0|10:1614427041|17:captcha_ticket_v2|312:eyJhcHBpZCI6IjIwMTIwMzEzMTQiLCJyZXQiOjAsInRpY2tldCI6InQwMzBWb29nQnNnRWxvY01wVlJWaFdLR2dKZkExdHpzNlhZQ3BiOFkyUDA1XzV4aHB2T3MyN2hoanJXb1pEV0dCOEJaQnlRUS15WHBDYS1sd2JLN3dUbjk3X0xLV0hZSDlRWGF2emFhQ3RqRTNIV24yQjhkZFNkOTl5aGQ5T2cxYVZkWjJkeXpoMGV4Wl83REZhSmZrclk1RHZTOGNRbDhfVWlkNWZkSXFCczdUTSoiLCJyYW5kc3RyIjoiQHVkNCJ9|208327371284b9a024accda742af7969439b2fac3aca69e7dc5e458363cdc91b"; captcha_session_v2="2|1:0|10:1614427022|18:captcha_session_v2|88:d21relQzOFExTzRnVU5Rc0w5TXV0NHhreEZ3cUhmSU55OVlWVFNDNHFmLzdDOGFCcXVMUmNpeDBVdGx5UE12aQ==|c76fa1c009958e7f440fb7a70780a8443ee78cf15570643f0a4fa30f9f9c57f6"; _zap=e869518b-c6b5-48f3-9e44-4f08342b2dba; d_c0="AMDXaMFsWBKPTtt_q3_eN0nhqFZEFvMQZQ8=|1607951734"'
jar = requests.cookies.RequestsCookieJar()
headers = {
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
}

# print(r.cookies)
# for key, value in r.cookies.items():
#     print("key:", key, "value:", value)
with open("zhihu.html", 'wb') as f:
    for cookie in cookies.split(';'):
        key, value = cookie.split('=', 1)
        jar.set(key, value)
        r = requests.get('http://www.zhihu.com', cookies=jar, headers=headers)
        print(r.text)
        f.write(r.content)
