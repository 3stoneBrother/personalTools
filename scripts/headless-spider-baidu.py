#coding:utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4
import requests
import time
import argparse
import sys
import urllib
import time
import random

opt = Options()
# opt.add_argument('--headless')
opt.add_argument('--disable-gpu')
opt.add_argument("--proxy-server=socks5://127.0.0.1:1080")
browser = webdriver.Chrome(chrome_options=opt)

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -k jd.com")
    parser.add_argument('-k', '--keywords', help="input keywords info",default=None)
    parser.add_argument('-od', '--ouputDomain', help="ouput domain",action="store_false")

    return parser.parse_args()


def getLocation(url):
    url = url
    headers = {
        "User-Agent": "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
    }
    response = requests.get(url=url,headers=headers,allow_redirects=False)
    return response.headers['location']

def chromeRequests(url):
    try:
        url = url
        browser.get(url)
        h = browser.page_source
        currenturl = browser.current_url
        if currenturl.startswith("https://wappass.baidu.com"):
            print "\033[1;41;40mplease open the head module,to bypass the antisplider!\033[0m"
            time.sleep(15)
            h = browser.page_source
    except:
        h="error"
    return h

def parseHtml(page,isLink):
    soup = bs4.BeautifulSoup(page, 'lxml')
    linkfinder = soup.find_all("div", {"class": 'result c-container'})
    for item in linkfinder:
        baiduEncodeUrl = item.a["href"]
        parsedUrl = getLocation(baiduEncodeUrl)
        if isLink:
            proto, rest = urllib.splittype(parsedUrl)
            res, rest = urllib.splithost(rest)
            if res:
                print res
        else:
            print parsedUrl



def mainBaidu(keywords,isLink):

    url = "https://www.baidu.com/s?&wd={}&ie=utf-8&pn=1&rn=20".format(keywords)
    page =  chromeRequests(url)


    soup = bs4.BeautifulSoup(page, 'lxml')

    linkfinder = soup.find_all("div",{"class": "result c-container "})

    if len(linkfinder) == 0:
        linkfinder = soup.find_all("h3",{"class": "t"})

    for item in linkfinder:
        baiduEncodeUrl =  item.a["href"]
        parsedUrl = getLocation(baiduEncodeUrl)
        if isLink:
            proto, rest = urllib.splittype(parsedUrl)
            res, rest = urllib.splithost(rest)
            if res:
                print res
        else:
            print parsedUrl

    pageNum = soup.find_all("span",{"class": 'pc'})

    pageNumList = []
    for _ in pageNum:
        pageNumList.append(int(str(_.get_text())))

    del (pageNumList[0])

    for num in pageNumList:
        xmlPath = '//*[@id="page"]/a[{}]/span[2]'.format(num)
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

    mainBaidu(keywords,isLink)




