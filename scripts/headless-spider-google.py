#coding:utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4
import argparse
import sys
import urllib
import time
import random
import re

opt = Options()
# opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_argument("--proxy-server=socks5://127.0.0.1:1080")
browser = webdriver.Chrome(chrome_options=opt)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -k jd.com")
    parser.add_argument('-k', '--keywords', help="input keywords info",default=None)
    parser.add_argument('-od', '--ouputDomain', help="ouput domain",action="store_false")

    return parser.parse_args()

def chromeRequests(url):
    try:
        url = url
        browser.get(url)
        h = browser.page_source
        currenturl = browser.current_url
        if currenturl.startswith("https://wappass.Google.com"):
            print "\033[1;41;40mplease open the head module,to bypass the antisplider!\033[0m"
            time.sleep(15)
            h = browser.page_source
    except:
        h="error"
    return h

def parseHtml(page,isLink):
    soup = bs4.BeautifulSoup(page, 'lxml')
    linkfinder = soup.find_all("div", {"class": "rc"})

    for item in linkfinder:
        GoogleEncodeUrl = item.a["ping"]
        parsedUrl = GoogleEncodeUrl.split("url=")[1]

        if isLink:
            proto, rest = urllib.splittype(parsedUrl)
            res, rest = urllib.splithost(rest)
            if res:
                print res
        else:
            parsedUrl = re.sub("&ved=[a-zA-Z_0-9]*", "", parsedUrl)
            print parsedUrl




def mainGoogle(keywords,isLink):

    url = "https://www.google.com.hk/search?safe=strict&source=hp&q={}&num=20".format(keywords)
    page =  chromeRequests(url)


    soup = bs4.BeautifulSoup(page, 'lxml')

    linkfinder = soup.find_all("div",{"class": "rc"})

    for item in linkfinder:
        GoogleEncodeUrl = item.a["ping"]
        parsedUrl = GoogleEncodeUrl.split("url=")[1]

        if isLink:
            proto, rest = urllib.splittype(parsedUrl)
            res, rest = urllib.splithost(rest)
            if res:
                print res
        else:
            parsedUrl = re.sub("&ved=[a-zA-Z_0-9]*", "", parsedUrl)
            print parsedUrl

    pageNum = soup.find_all("a",{"class": 'fl'})

    pageNumList = []
    for _ in pageNum:
        text=  _.get_text()
        if is_number(text):
            pageNumList.append(int(str(_.get_text())))

    # del (pageNumList[0])

    for num in pageNumList:
        xmlPath = '//*[@id="xjs"]/div/table/tbody/tr/td[{}]/a'.format(num+1)
        pageBoton = browser.find_element_by_xpath(xmlPath)
        pageBoton.click()
        time.sleep(random.randint(3,8))

        h = browser.page_source
        parseHtml(h,isLink)
    browser.quit()

if __name__=='__main__':
    args = parse_args()
    keywords = args.keywords
    if args.ouputDomain:
        isLink = False
    else:
        isLink = True

    mainGoogle(keywords,isLink)




