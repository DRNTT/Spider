import requests
import re
import json


# 获取一页信息
def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?<img data-src="(.*?)".*?<a.*?title="(.*?)".*?<p class="star">(.*?)</p>'
                         '.*?<p class="releasetime">(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'rank': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip(),
            'time': item[4][5:].strip(),
            'score': item[5].strip() + item[6].strip()
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.writelines(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        # print(item)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        main(offset = i * 10)