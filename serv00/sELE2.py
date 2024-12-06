import os
import random
import string

import ddddocr
import requests
from DrissionPage import ChromiumPage, SessionPage

from serv00 import pynamesgenerator
ocr = ddddocr.DdddOcr()


def getemail(name):
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://products.aspose.app',
        'priority': 'u=1, i',
        'referer': 'https://products.aspose.app/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36',
    }

    files = {
        'email': 'najxjdn@gmail.com'
    }

    response = requests.post('https://api.products.aspose.app/email/api/FakeEmail/Generate', headers=headers,
                             data=files)
    if response.status_code == 200:
        return  response.json()['generatedAddress']
    else:
        raise Exception

def generate_random_string(length=6):
    # 可供选择的字符（字母和数字）
    characters = string.ascii_letters + string.digits
    # 随机选择字符并连接成字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def download_ob(url):
    response = requests.get(url)
    panme = 'img/cap' + generate_random_string() + '.png'
    if response.status_code == 200:
        # 保存图片
        with open(panme, 'wb') as file:
            file.write(response.content)
            return panme
    else:
        return False

flag = True



while(flag):
    page = ChromiumPage()
    # page.get('https://www.croxyproxy.rocks/_zh/')
    # ing = page.ele('@placeholder=Enter an URL or a search query to access')
    # ing.input('https://www.serv00.com/offer/create_new_account')
    # ela = page.ele('#requestSubmit')
    # ela.click()
    #
    # page.wait.eles_loaded('.hero-content')
    page.get('https://webproxy.lumiproxy.com/request?area=UA&u=https://www.serv00.com/offer/create_new_account')

    names = pynamesgenerator.gen_two_words(split=' ', lowercase=False).split(' ')
    username = pynamesgenerator.gen_two_words(split='', lowercase=True) + pynamesgenerator.gen_year(1988, 2015)
    username = username[:15]

    ele = page.ele('@placeholder=First name...')
    ele.input(names[0])

    ele = page.ele('@placeholder=Last name...')
    ele.input(names[1])

    ele = page.ele('@placeholder=Username...')
    ele.input(username)

    ele = page.ele('@placeholder=E-mail address')
    ele.input('yigafraddouga-5972@yopmail.com')

    ch = page.ele('#id_tos')
    ch.check()

    img = page.ele('.captcha is-')
    src = img.attr("src")
    src = src.replace('https://webproxy.lumiproxy.com','https://www.serv00.com')

    pname = download_ob(src)
    with open(pname, 'rb') as f:
        img_tytes = f.read()
        # 调用识别方法
        res = ocr.classification(img_tytes)
        if res:
            code = page.ele('@placeholder=CODE...')
            code.input(res)
            code = page.ele('@placeholder=Answer...')
            code.input(0)
            btn = page.ele('.button is-primary')
            btn.click()
            page.wait(float(3))
            err = page.ele('.control has-error')
            if err:
                print("213")
            else:
                flag = False
                break
        else:
            page.close()





