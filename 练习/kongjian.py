from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import time
import json


browser = webdriver.Firefox()
wait = WebDriverWait(browser, 10)

def index_page(qq, page):
    #  进入主页
    try:
        url = 'https://user.qzone.qq.com/' + qq
        browser.get(url)
        # 账号密码登录
        # if page is 1:
        #     browser.switch_to.frame('login_frame')
        #     browser.find_element_by_id('switcher_plogin').click()
        #     browser.find_element_by_id('u').clear()
        #     browser.find_element_by_id('u').send_keys('qq号')
        #     browser.find_element_by_id('p').clear()
        #     browser.find_element_by_id('p').send_keys('qq密码')
        #     browser.find_element_by_id('login_button').click()
        #     browser.switch_to.default_content()
        btn_ss = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#QM_Profile_Mood_A span')))
        btn_ss.click()
        browser.switch_to.frame('app_canvas_frame')
        if page > 1:
            print('正在爬取', page, '页')
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#pager .textinput')))
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#pager .bt_tx2')))
            input.clear()
            input.send_keys(page)
            submit.click()

        get_info()
    except TimeoutException:
        index_page(qq, page)


def get_info():
    time.sleep(3)
    html = browser.page_source
    # print(html)
    doc = pq(html)
    items = doc('#msgList .feed').items()
    for item in items:
        pic = []
        images = item.find('.md img').items()
        for image in images:
            pic.append(image.attr('data-src'))
        ss = {
            'author': item.find('.bd .qz_311_author').text(),
            'content': item.find('.bd .content').text(),
            'image': pic,
            'time': item.find('.ft .info').text()
        }
        save_to_txt(ss)


def save_to_txt(ss):
    with open('data.txt', 'a', encoding='gb18030') as file:
        file.write(json.dumps(ss, ensure_ascii=False) + '\n')


MAX_PAGE = 17

if __name__ == '__main__':
    for page in range(1, MAX_PAGE + 1):
        index_page('qq号', page)