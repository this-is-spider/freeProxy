# -*- coding=utf-8 -*-
import csv
import random
import requests
from pyquery import PyQuery as pq

user_agent_list = [
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

def get_proxy(page=20):
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    all_proxy = (page-1) * 15
    success_proxy = 0
    datas = []
    for i in range(1, page):
        url = 'https://www.kuaidaili.com/free/inha/' + str(i) + '/'
        response = requests.get(url=url, headers=headers)
        try:
            if response.status_code == 200:
                print('连接成功')
                doc = pq(response.text)
                start = 1
                data = {}
                for each in doc('td').items():
                    if each.attr['data-title'] == 'IP':
                        data['ip'] = each.text()
                    if each.attr['data-title'] == 'PORT':
                        data['port'] = each.text()
                    start += 1
                    if start % 8 == 0:
                        start = 1
                        if check_proxy(data):
                            success_proxy += 1
                            datas.append(data)
                        else:
                            print('无效代理')
                        data={}
            save_proxy(datas)
        except:
            print('连接失败')
    success_percent = round(success_proxy / all_proxy, 2) * 100
    print(str(success_percent) + '%')




def check_proxy(data):
    url = 'https://www.baidu.com'
    proxy = {'http' : 'http://' + data['ip'] + ':' + data['port']}
    response = requests.get(url=url, proxies=proxy)
    if response.status_code == 200:
        print(proxy)
        return True
    else:
        return False


def save_proxy(datas):
    with open('自建代理.CSV', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for data in datas:
            proxy = 'http://' + data['ip'] + ':' + data['port']
            writer.writerow([proxy])


if __name__ == '__main__':
    get_proxy(page=20)
