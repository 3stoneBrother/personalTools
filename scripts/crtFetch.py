#coding:utf-8

import json
import requests
import argparse
import sys
import os


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")

    parser.add_argument('-d', '--domain', help="Domain name to enumerate it's subdomains", required=True)
    parser.add_argument('-o1', '--output1', help='Save the results to *.jd.com file')
    parser.add_argument('-o2', '--output2', help='Save the results to www.jd.com file')
    return parser.parse_args()

def write_sdin(subdomains):
    for subdomain in subdomains:
        print subdomain

def crtDoamin(domain):
    base_url = "https://crt.sh/?q={}&output=json"

    domain = "%25.{}".format(domain)
    url = base_url.format(domain)
    subdomains = set()
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
    req = requests.get(url, headers={'User-Agent': user_agent}, timeout=30,
                       verify=False)  # times out after 30 seconds waiting (Mainly for large datasets)
    if req.status_code == 200:
        content = req.content.decode('utf-8')
        data = json.loads(content)
        for subdomain in data:
            subdomains.add(subdomain["name_value"].lower())
        return sorted(subdomains)

def iteration_domain(domain):
    domainList = crtDoamin(domain)
    domain_need_append = []
    domain_find = []

    ## 日后考虑三级，四级域名的情况
    for domain_sum in domainList:
        domain_sum = domain_sum.encode('utf-8')
        if ("*" in domain_sum):
            domain_sum_list = domain_sum.split("\n")
            for dm_sub in domain_sum_list:
                if "*" in dm_sub:
                    domain_need_append.append(dm_sub)
                else:
                    domain_find.append(dm_sub)
        else:
            for item in domain_sum.split("\n"):
                domain_find.append(item)

    return list(set(domain_need_append)),list(set(domain_find))


def certspotter_domain(domain):

    subdomains = []

    domain_need_append = []
    domain_find = []

    url = 'https://certspotter.com/api/v0/certs?domain={}'.format(domain)
    json_resp = json.loads(requests.get(url).text)
    doms = [e['dns_names'] for e in json_resp]
    for subs in doms:
        subdomains += subs

    for sub_dom in subdomains:
        sub_dom = sub_dom.encode('utf-8')
        if "*" in sub_dom:
            domain_need_append.append(sub_dom)
        else:
            domain_find.append(sub_dom)

    return list(set(domain_need_append)), list(set(domain_find))

# def threatcrowd_domain(domain):
#
#     url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={}'.format(domain)
#     user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
#     session = requests.session()
#     resp = session.get(url, headers={'User-Agent': user_agent}, timeout=30,
#                        verify=False)
#     response = resp.text
#     res_action = r'action=\"(.*?)\"'
#     actionString =  re.findall(res_action,response)[0]
#     url = 'https://www.threatcrowd.org' + actionString.replace("amp;","")
#
#     res_action = r'name=\"(.*?)\" value=\"(.*?)\"'
#     namaeValueString = re.findall(res_action, response)
#
#     res_action = r'id=\"(.*?)\" name=\"(.*?)\"'
#     key1,value1 = re.findall(res_action, response)[0]
#
#     import collections
#     data = collections.OrderedDict()
#
#
#     for key,value in namaeValueString:
#         data[key] = value
#     data[key1] = value1
#
#     print data
#
#     proxies = {"http": "http://127.0.0.1:8088", "https": "http://127.0.0.1:8088", }
#     headers = {'User-Agent': user_agent,'Origin': 'https://www.threatcrowd.org','Referer': 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=jd.com'}
#
#
#     req = session.post(url,data=data,headers=headers, proxies=proxies,timeout=30,
#                        verify=False)


    # json_resp = json.loads(resp.text)
    # if 'subdomains' in json_resp.keys():
    #     print json_resp['subdomains']


def meg_domain():
    args = parse_args()
    domain = args.domain


    domain_need_append = []
    domain_find = []

    domain_need_append1,domain_find1 =iteration_domain(domain)
    domain_need_append.extend(domain_need_append1)
    domain_find.extend(domain_find1)

    domain_need_append2, domain_find2 = iteration_domain(domain)
    domain_need_append.extend(domain_need_append2)
    domain_find.extend(domain_find2)
    write_sdin(list(set(domain_need_append)))
    print "#"*20
    write_sdin(list(set(domain_find)))



if __name__ == '__main__':
    meg_domain()