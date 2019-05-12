from urllib.parse import urlencode
from pyquery import PyQuery as pq
import json
import requests

base_url = 'https://m.weibo.cn/api/container/getIndex?'

# Referer用来标识请求从哪个页面发送过来的
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_page(page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }

    url = base_url + urlencode(params)

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json_):
    if json_:
        items = json_.get('data').get('cards')
        for item in items:
            mblog = item.get('mblog')
            if mblog:
                weibo = {}
                weibo['id'] = mblog.get('id')
                weibo['text'] = pq(mblog.get('text')).text()
                weibo['attitudes'] = mblog.get('attitudes_count')
                weibo['comments'] = mblog.get('comments_count')
                weibo['reposts'] = mblog.get('reposts_count')
                yield weibo

if __name__ == '__main__':
    for page in range(1, 11):
        json_ = get_page(page)
        results = parse_page(json_)
        file = open('data.json', 'a', encoding='gb18030')
        for result in results:
            print(result)
            file.write(json.dumps(result, ensure_ascii=False) + '\n')
        file.close()