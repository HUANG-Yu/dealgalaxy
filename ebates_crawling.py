#coding=utf-8
import urllib
import re

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    # print(html)
    return html

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
    for pair in sites_list1 + sites_list2 + sites_list3:
        print pair
        x = x + 1
    print x

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

def cb_increase_websites(html):
    after_re = r'<a href="/coupons/(.+?)/index.htm" class="cb prox-b cb prox-b f-18 nohover">(.+?)\n'
    after_re_obj = re.compile(after_re)
    after_list = re.findall(after_re_obj, html)
    before_re = r'<span class="cb-was prox-r f-12">was (.+?)</span>'
    before_re_obj = re.compile(before_re)
    before_list = re.findall(before_re_obj, html)
    x = 0
    for before in after_list:
        print before
        x = x + 1
    print x



html = getHtml("http://www.ebates.com/stores/all/index.htm?navigation_id=22763")

# get_websites_cb_pairs(html)

cb_increase_websites(html)

''' processing - change whitespace with hyphen
double_cb_html = getHtml("http://www.ebates.com/summer-sales.htm?navigation_id=22763")

get_double_cb_websites(double_cb_html)
'''


# print getImg(html)