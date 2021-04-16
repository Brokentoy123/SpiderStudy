import re
import requests
import json

def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (MacintoshIntel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.text)
        return response.text
    return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?<p.*?name.*?a.*?>(.*?)</a></p>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    results = re.findall(pattern, html)
    for result in results:
        yield {
            'index': result[0],
            'img': result[1],
            'title': result[2],
            'actor': result[3].strip()[3:],
            'time': result[4].strip()[5:],
            'score': result[5]+result[6]
        }
    return results


def main(offset):

    url = "http://maoyan.com/board/4?offset="+str(offset)
    html = get_one_page(url)
    results = parse_one_page(html)
    # print(results)
    for result in results:
        print(result)
        write_to_file(result)

def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n') #ensure_ascii指定False，输出内容为中文时就不会变成ascii码

if __name__=='__main__':
    for i in range(10):
        main(i*10)
