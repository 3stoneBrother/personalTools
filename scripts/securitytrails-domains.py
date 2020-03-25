#coding:utf-8

import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import sys
import argparse

proxies = { "http": "http://127.0.0.1:8088", "https": "http://127.0.0.1:8088", }


def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d jd.com")
    parser.add_argument('-d', '--domain', help="input domain",default=None)

    return parser.parse_args()

def getDomain(domain):
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument("--proxy-server=socks5://127.0.0.1:1080")
    browser = webdriver.Chrome(chrome_options=opt)

    url = 'https://securitytrails.com/list/apex_domain/{}'.format(domain)
    browser.get(url)

    pagesource = browser.page_source

    token = re.findall('window.csrf_token = "(.*?)";',pagesource)[0]
    cookiesList = browser.get_cookies()

    s = requests.Session()
    for i in cookiesList:
        requests.utils.add_dict_to_cookiejar(s.cookies, {i['name']: i['value']})

    strHeaders = '''Accept: application/json
    Sec-Fetch-Dest: empty
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
    Content-Type: application/json;charset=UTF-8
    Origin: https://securitytrails.com
    Sec-Fetch-Site: same-origin
    Sec-Fetch-Mode: cors
    Referer: https://securitytrails.com/list/apex_domain/baidu.com
    Accept-Encoding: gzip, deflate
    Accept-Language: zh-CN,zh;q=0.9,en;q=0.8'''
    headers = {}
    for iterms in strHeaders.split("\n"):
        key = iterms.split(": ")[0]
        value = iterms.split(": ")[1]
        headers[key] = value

    data = {"_csrf_token":token}

    url = 'https://securitytrails.com/app/api/v1/list?apex_domain={}'.format(domain)
    requests.packages.urllib3.disable_warnings()
    reponse = s.post(url,headers=headers,data=json.dumps(data),verify=False)
    recordsList = json.loads(reponse.text)["records"]
    for record in recordsList:
        print record["hostname"]
    recordsCount = json.loads(reponse.text)["record_count"]

    for num in range(2,recordsCount+1):
        url = 'https://securitytrails.com/app/api/v1/list?page={}&apex_domain={}'.format(num,domain)
        try:
            requests.packages.urllib3.disable_warnings()
            reponse = s.post(url, headers=headers, data=json.dumps(data))
            recordsList = json.loads(reponse.text)["records"]
            for record in recordsList:
                print record["hostname"]
        except Exception as e:
            print "need sign up"
            sys.exit()


if __name__=='__main__':
    args = parse_args()
    domain = args.domain








