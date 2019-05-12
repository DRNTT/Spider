import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
import time


# 必须设置Cookie，否则无法获取到data
def get_page(offset):
    headers = {
        'Accept': 'application/json, text/javascript',
        'Accept-encoding': 'gzip, deflate, br',
        'Accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-type': 'application/x-www-form-urlencoded',
        'Host': 'www.toutiao.com',
        'Cookie': 'tt_webid=6689938985769108995; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16aa98df291762-0958afad1d90a2-3b654406-1fa400-16aa98df292514; CNZZDATA1259612802=1976895024-1557621840-%7C1557621840; tt_webid=6689938985769108995; csrftoken=40b7858f703aff22fcd52664d7980da2; s_v_web_id=30c9efc456d610d2fc3933e811a79fbc; uuid="w:85c6b4e8526441208216fe3d5e5ffcf5"; __tasessionId=df6u909a71557644434927',
        'Referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    timestamp = int(round(time.time() * 1000))
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'en_qc': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': timestamp
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(params)
    # print(url)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            # print(title)
            images = item.get('image_list')
            # print(images)
            if images is not None:
                for image in images:
                    yield {
                        'image': image.get('url'),
                        'title': title
                    }

def sava_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), '.jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Download', file_path)
    except requests.ConnectionError:
        print('Faild to Save Image')

def main(offset):
    json = get_page(offset)
    print(json)
    for item in get_images(json):
        sava_image(item)

GROUP_START = 1
GROUP_END = 20

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()