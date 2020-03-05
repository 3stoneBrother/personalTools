# coding:utf-8

import requests
import re
from bs4 import BeautifulSoup
import sys

keywords="京东"


proxies = { "http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080", }

import argparse


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -k 京东")
    parser.add_argument('-k', '--keywords', help="input key words",default=None)
    return parser.parse_args()

def getWeixinGongzhonghao(keywords,pagenum):
    url="https://weixin.sogou.com/weixin?query={}&type=1&page={}&ie=utf8".format(keywords,pagenum)

    headers={
        "User-Agent":"(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
    }

    session = requests.session()
    session.proxies = {'http': 'socks5://127.0.0.1:1080',
                       'https': 'socks5://127.0.0.1:1080'}

    rep = session.get(url,headers=headers).text

    num =  re.findall(r"resultbarnum:(.*?)--",rep)[0]

    resultList = []

    soup = BeautifulSoup(rep,"html.parser")
    for item in soup.find_all("li"):
        if "sogou_vr" in str(item):
            title = re.sub("<.*?>","",str(item.dd))
            weixinID = item.label.string
            try:
                enterprise=re.findall("</i>(.*?)</dd>",str(item))[0]
            except:
                enterprise1 = re.findall("<em>(.*?)</a>",str(item))[0]
                enterprise = re.sub("<.*?>", "", enterprise1)


            resultList.append(str(weixinID) + "#" + str(enterprise) + "#" + title)
    return num,resultList

def main(keywords):
    num,result = getWeixinGongzhonghao(keywords,1)
    pagenum = int(num)/10 + 1

    if pagenum == 1:
        for item in result:
            print item
    else:
        for item in result:
            print item
        for pnum in range(2,pagenum+1):
            _,result = getWeixinGongzhonghao(keywords,pnum)
            for item in result:
                print item


if __name__=='__main__':
    args = parse_args()
    keywords = args.keywords
    main(keywords)