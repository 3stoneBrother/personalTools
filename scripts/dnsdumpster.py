#coding:utf-8
import re
import requests
import argparse
import sys

def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d jd.com")
    parser.add_argument('-d', '--domain', help="input domain",default=None)
    return parser.parse_args()

def dnsdumpster(domain):
    response = requests.Session().get('https://dnsdumpster.com/').text
    ## 确定token
    csrf_token = re.search(
        r'name=\"csrfmiddlewaretoken\" value=\"(.*?)\"', response).group(1)

    cookies = {'csrftoken': csrf_token}
    headers = {'Referer': 'https://dnsdumpster.com/'}
    data = {'csrfmiddlewaretoken': csrf_token, 'targetip': domain}

    requests.Session().post(
        'https://dnsdumpster.com/', cookies=cookies, data=data, headers=headers)
    try:
        image = requests.get('https://dnsdumpster.com/static/map/%s.png' % domain)
        if image.status_code == 200:
            with open('%s.png' % (domain), 'wb') as f:
                f.write(image.content)
    except Exception as e:
        print(" [-] error %s".format(str(e)))

if __name__=='__main__':
    args = parse_args()
    domain = args.domain
    dnsdumpster(domain)