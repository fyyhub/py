import random
import string

import requests
from bs4 import BeautifulSoup
import ddddocr
from concurrent.futures import ThreadPoolExecutor
import pynamesgenerator


ocr = ddddocr.DdddOcr()
session = requests.Session()

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


def getemail():
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://22.do/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    data = {
        'type': 'Gmail',
    }

    response = requests.post('https://22.do/zh/mailbox/generate', headers=headers, data=data)
    return response.json()['data']['address']['email']



def rrqq(purs):
    try:
        proxies = {"http": 'http://' + purs, "https": 'http://' + purs}
        resp = session.get("https://www.serv00.com/offer/create_new_account", proxies=proxies,timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        csf = soup.find("input", {"name": "csrfmiddlewaretoken"})
        tok = csf.get("value")
        img = soup.find("img", {"class": "captcha is-"})
        img_id = soup.find("input", {"name": "captcha_0"}).get("value")
        pname = download_ob("https://www.serv00.com" + img.get("src"))
        with open(pname, 'rb') as f:
            img_tytes = f.read()
            # 调用识别方法
            res = ocr.classification(img_tytes)
            if res:
                cookies = {
                    'csrftoken': tok,
                }
                headers = {
                    'authority': 'www.serv00.com',
                    'accept': '*/*',
                    'accept-language': 'zh-CN,zh;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://www.serv00.com',
                    'referer': 'https://www.serv00.com/offer/create_new_account',
                    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36',
                }
                names = pynamesgenerator.gen_two_words(split=' ', lowercase=False).split(' ')
                username = pynamesgenerator.gen_two_words(split='', lowercase=True) + pynamesgenerator.gen_year(1988, 2015)
                username = username[:15]

                emial = getemail()

                data = {
                    'csrfmiddlewaretoken': tok,
                    'first_name': names[0],
                    'last_name': names[1],
                    'username': username,
                    'email': emial,
                    'captcha_0': img_id,
                    'captcha_1': res,
                    'question': '0',
                    'tos': 'on',
                }
                response = session.post('https://www.serv00.com/offer/create_new_account.json', cookies=cookies,
                                        headers=headers,
                                        data=data, proxies=proxies, timeout=60)
                print(response)
                print(emial)
                print(response.text)
    except Exception as e:
        pass


if __name__ == '__main__':
    with open("filter/proxyip.txt", "r"):
        purses = [line.strip() for line in open("filter/proxyip.txt", "r")]
    with ThreadPoolExecutor(5) as executor:
        for purs in purses:
            executor.submit(rrqq, purs)
