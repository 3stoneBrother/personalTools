"""Support for archive.org."""
import datetime
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import bs4
import argparse
import sys
import urllib

def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d jd.com")
    parser.add_argument('-d', '--domain', help="input domain",default=None)
    parser.add_argument('-od', '--ouputDomain', help="ouput domain",action="store_true")
    parser.add_argument('-ol', '--ouputLink', help="ouput link",action="store_true")

    return parser.parse_args()

def chromeRequests(url):
    opt = Options()
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument("--proxy-server=socks5://127.0.0.1:1080")

    browser = webdriver.Chrome(chrome_options=opt)
    try:
        url = url
        browser.get(url)
        h = browser.page_source
    except:
        h="error"

    browser.quit()
    return h


def time_machine(host, mode):
    """Query archive.org."""
    now = datetime.datetime.now()
    to = str(now.year) + str(now.day) + str(now.month)
    if now.month > 6:
    	fro = str(now.year) + str(now.day) + str(now.month - 6)
    else:
    	fro = str(now.year - 1) + str(now.day) + str(now.month + 6)
    url = "http://web.archive.org/cdx/search?url=%s&matchType=%s&collapse=urlkey&fl=original&filter=mimetype:text/html&filter=statuscode:200&output=json&from=%s&to=%s" % (host, mode, fro, to)
    page = chromeRequests(url)
    soup = bs4.BeautifulSoup(page, 'lxml')
    response =soup.find_all("pre")[0].string
    parsed = json.loads(response)[1:]
    urls = []
    for item in parsed:
        urls.append(item[0])
    return urls

if __name__=='__main__':
    args = parse_args()
    domain = args.domain
    if args.ouputDomain:
        domainList = []
        domain_link = time_machine(domain, "domain")
        for link in domain_link:
            proto, rest = urllib.splittype(link)
            res, rest = urllib.splithost(rest)
            if res:
                domainList.append(res)
        domain_link = list(set(domainList))
        for domain_sub in domain_link:
            print domain_sub

    else:
        domain_link = time_machine(domain,"domain")
        for link in domain_link:
            print link
