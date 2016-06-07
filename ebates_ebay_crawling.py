#coding=utf-8
import re
import json
import random
import urllib
import urllib2
import datetime
import string
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding

# --TODO-- appending time info to the store names, saving them all to file

'''Define some user agents to wrap the scraper as some kind of browsers sending requests'''
def get_user_agent():
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
    (KHTML, like Gecko) Element Browser 5.0', \
    'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
    Version/6.0 Mobile/10A5355d Safari/8536.25', \
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/28.0.1468.0 Safari/537.36', \
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
    return user_agents

'''Get the webpage body in fully plain text'''
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    # print(html)
    return html

'''Getting websites and their relevant cash back values in pairs'''
def get_websites_cb_pairs(html):
    sites_reg1 = r'<a href="/coupons/(.+?)/index.htm" class="cb prox-b f-18 nohover">(.+?)\n'
    sites_re_obj1 = re.compile(sites_reg1)
    sites_list1 = re.findall(sites_re_obj1, html)
    sites_reg2 = r'<a href="/coupons/(.+?)/index.htm" class="cb prox-b f-14">(.+?)</a'
    sites_re_obj2 = re.compile(sites_reg2)
    sites_list2 = re.findall(sites_re_obj2, html)
    sites_reg3 = r'<a href="/coupons/(.+?)/index.htm" class="cb prox-b cb prox-b f-18 nohover">(.+?)\n'                                        
    sites_re_obj3 = re.compile(sites_reg3)
    sites_list3 = re.findall(sites_re_obj3, html)
    x = 0
    res = list()
    for pair in sites_list1 + sites_list2 + sites_list3:
        url = 'https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=%s' % pair[0]
        cur_list = list(pair)
        # uncomment to change hyphen to space for more readability
        # cur_list[0] = cur_list[0].replace("-", " ")
        # print cur_list[0]
        cur_list.append(url)
        print cur_list
        res.append(cur_list)
        x = x + 1
    print x
    return res

'''Get thos websites tuples whose cash back doubles'''
def get_double_cb_websites(html):
    sites_reg = r'title="Get a great deal from (.+?) plus (.+?)% Cash Back from Ebates!"'
    sites_re_obj = re.compile(sites_reg)
    sites_list = re.findall(sites_re_obj, html)
    i = 0
    unique_sites = set(sites_list)
    for double_cb in unique_sites:
        print double_cb
        i = i + 1
    print i

# method broken because of Google encryption
def get_website_links(cur_html):
    link_re = r',event\)" data\-href="(.+?)">'
    link_re_obj = re.compile(link_re)
    link_list = re.findall(link_re_obj, cur_html)
    x = 0
    for link in link_list:
        print link
        x = x + 1
    print x
    
'''Get the websites whose cash back values increases and their old cash back values in a tuples, representing them in a list format'''
def cb_increase_websites(html):
    re1 = r'<a href="/coupons/(.+?)/index.htm" class="cb prox-b cb prox-b f-18 nohover">(.+?)\n\t+<span class="cb-was prox-r f-12">was (.+?)</span>'
    re_obj1 = re.compile(re1)
    tuple1 = re.findall(re_obj1, html)
    re2 = r'<a href="/coupons/(.+?)/index.htm" class="cb prox-b f-18 nohover">(.+?)\n +<span class="cb-was prox-r f-12">was (.+?)</span>'
    re_obj2 = re.compile(re2)
    tuple2 = re.findall(re_obj2, html)
    x = 0
    for each in tuple1 + tuple2:
        url = 'https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=%s' % each[0]
        cur_list = list(each)
        # uncomment to change hyphen to space for more readability
        # cur_list[0] = cur_list[0].replace("-", " ")
        cur_list.append(url)
        # print cur_list
        x = x + 1
    print x

'''Setting up user agents'''
def agents():
    url = 'http://www.server.com/login'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
    values = {'username' : 'yh1456@nyu.edu',  'password' : 'Yu//910503' }  
    headers = { 'User-Agent' : user_agent }  
    data = urllib.urlencode(values)  
    request = urllib2.Request(url, data, headers)  
    response = urllib2.urlopen(request)  
    page = response.read()

'''get the gift card information from ebay api'''
def ebay_api_data(input_list):
    try:
        api = Finding(appid="YuHUANG-insightd-PRD-04d8cb02c-4739185d")
        for cur_list in input_list:
            response = api.execute('findItemsAdvanced', {'keywords': cur_list[0] + 'Gift Card'})
            print(response.dict())
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

'''enlarge the cash back links dataset'''
def create_duplicates_cb_links(cb_lists):
    new_list = list()
    i = len(cb_lists)
    for x in range(0, i):
        for cur_list in cb_lists:
            cur_list[2] = cur_list[2] + random.choice(string.letters)
            # print cur_list
            new_list.append(cur_list)
    new_list = cb_lists + new_list
    print len(new_list)

'''enlarge the ebay api dataset'''
def create_duplicates_ebay(ebay_lists):
    new_list = list()
    i = len(ebay_lists)
    for x in range(0, i):
        for cur_list in ebay_lists:
            cur_list = cur_list
            # -- TODO --
    print i

'''convert lists to json object to store them in s3/spark'''
def lists_to_json(cb_lists):
    # -- TODO --
    return cb_lists

'''Entrance function of the program'''
def main():
    html = getHtml("http://www.ebates.com/stores/all/index.htm?navigation_id=22763")
    cb_lists = get_websites_cb_pairs(html)
    duplicates_list = create_duplicates_cb_links(cb_lists)
    # ebay_api_data(cb_lists)
    # get_double_cb_websites(html)
    # cb_increase_websites(html)


# Running
if __name__ == '__main__':
    main()

''' processing - change whitespace with hyphen
double_cb_html = getHtml("http://www.ebates.com/summer-sales.htm?navigation_id=22763")

get_double_cb_websites(double_cb_html)

get_websites_cb_pairs(html)
'''