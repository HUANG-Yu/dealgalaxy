#coding=utf-8
import re
import json
import datetime
import random
import urllib
import urllib2
import datetime
import string
from random import randint
from pprint import pprint
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding

'''Get the webpage body in full plain text'''
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
    res = list()
    for pair in sites_list1 + sites_list2 + sites_list3:
        url = 'https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=%s' % pair[0]
        cur_list = list(pair)
        cur_list.append(url)
        res.append(cur_list)
    return res


'''get the gift card information from ebay api'''
def ebay_api_data(input_list, time_string, real = 1):
    if (real == 1):
        f = open('./data/' + time_string[:-6] + 'ebay_gc', 'w+')
    else:
        f = open('./data/' + time_string[:-6] + 'all_ebay_gc', 'w+')
    f.write("[")
    res = dict()
    size = len(input_list)
    try:
        api = Finding(appid="YuHUANG-insightd-PRD-04d8cb02c-4739185d")
        for i in xrange(0, size):
            cur_list = input_list[i]
            # print cur_list[0]
            if (cur_list[0] != 'soak-&-sleep'):
                response = api.execute('findItemsAdvanced', {'keywords': cur_list[0] + ' Gift Card'})
                join_string = str(response.dict())
            if (i != size - 1):
                f.write(json.dumps(response.dict()))
                f.write(",\n")
            else:
                f.write(json.dumps(response.dict()))
                f.write("\n")
        f.close()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

'''convert full lists with three parameters to json object to store them in s3/spark'''
def lists_to_json(cb_lists, time_string, real = 1):
    if (real == 1):
        f = open('./data/' + time_string[:-6] + 'ebates.txt', 'w+')
    else:
        f = open('./data/' + time_string[:-6] + 'all_ebates', 'w+')
    list_len = len(cb_lists)
    for i in xrange(0, list_len):
        cur_list = cb_lists[i]
        if (cur_list[1][0] == '$' or cur_list[1][0] == 'U'):
            cur_item = time_string[:-6] + ',' + cur_list[0] + ',' + '5.0,' + cur_list[2] + '\n'
        elif (cur_list[1][0] == 'N' or cur_list[1][0] == 'C' or cur_list[1][0] == 'I'):
            cur_item = time_string[:-6] + ',' + cur_list[0] + ',' + '0.0,' + cur_list[2] + '\n'
        else:
            cur_item = time_string[:-6] + ',' + cur_list[0] + ',' + cur_list[1][:-1] + ',' + cur_list[2] + '\n'
        f.write(cur_item)
    f.close()

'''generate the brand list by crawling the data from brand names websites - 2060 in total'''
def get_brand_list():
    html = getHtml("http://www.namedevelopment.com/brand-names.html")
    reg = r'<li>(.+?)</li>'
    reg_obj = re.compile(reg)
    brand_list = list()
    brand_tuples = re.findall(reg_obj, html)
    for cur_brand in brand_tuples:
        if (len(cur_brand) >= 4 and cur_brand[-4:] != '</a>'):
            cur_brand = cur_brand.replace(" ", "-")
            brand_list.append(cur_brand)
    return brand_list

'''generate the category from the json file converted from the exel template offered by Google'''
def get_categories():
    with open('walmart_categories_json') as data_file:    
        data = json.load(data_file)
    json_array = data['categories']
    array_len = len(json_array)
    category_list = list()
    for i in xrange(0, array_len):
        cur_json = json_array[i]
        category_list.append(cur_json['name'])
        sub_json_array = cur_json['children']
        sub_len = len(sub_json_array)
        for j in xrange(0, sub_len):
            sub_cur_json = sub_json_array[j]
            category_list.append(sub_cur_json['name'])
    return category_list

'''generate the coupon code which consists of uppercase letter and digts in random order'''
def coupon_code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

'''generate the coupon for given websites - format: websites, coupon code, category, brands, start dates, expire dates'''
def coupon_generator(cb_lists, category_list, brand_list, time_string):
    f = open('./data/' + time_string[:-6] + 'coupon.txt', 'w+')
    cb_len = len(cb_lists)
    for j in xrange(0, 14):
        for i in range(0, cb_len):
            time_pair1 = get_time_pair()
            time_pair2 = get_time_pair()
            category = random.choice(category_list)
            category = category.replace(',','-')
            category = category.replace('$','')
            cur_item1 = time_string[:-6] + ',' + random.choice(cb_lists)[0] + ',' + coupon_code_generator() + ',' + category + ',' + str(int((round(random.random()/4, 2) + 0.05)*100)) + ',' + time_pair1[0] + ',' + time_pair1[1] + '\n'
            cur_item2 = time_string[:-6] + ',' + random.choice(cb_lists)[0] + ',' + coupon_code_generator() + ',' + category + ',' + str(int((round(random.random()/4, 2) + 0.05)*100)) + ',' + time_pair1[0] + ',' + time_pair1[1] + '\n'
            f.write(cur_item1)
            f.write(cur_item2)
    f.close()
    # print coupon_list_json


def get_time():
    time  = datetime.datetime.now()
    # round to the next full hour
    time -= datetime.timedelta(minutes = time.minute, seconds = time.second, microseconds =  time.microsecond)
    time += datetime.timedelta(hours = 1)
    time_string = time.strftime("%Y-%m-%d_%H-%M")
    # print time_string
    return time_string

def round_time_to_day():
    time  = datetime.datetime.now()
    # round to the next full hour
    time -= datetime.timedelta(hours = time.hour, minutes = time.minute, seconds = time.second, microseconds =  time.microsecond)
    time_string = time.strftime("%Y-%m-%d")
    return time

''' generate the coupon starting date and end date '''
def get_time_pair():
    start_time = round_time_to_day()
    end_time = start_time + datetime.timedelta(randint(1,9))
    time_pair = list()
    time_pair.append(start_time.strftime("%Y-%m-%d"))
    time_pair.append(end_time.strftime("%Y-%m-%d"))
    return time_pair

'''get the item and price from 6pm websites'''
def get_item_list():
    link_prev = 'http://www.6pm.com/null-page1453/.zso?p='
    item_list = list()
    for i in xrange(1, 1452):
        cur_link = getHtml(link_prev + str(i))
        cur_link_re = r'<span class="brandName" itemprop="brand">(.+?)</span>\n<span class="productName" itemprop="name">(.+?)</span>\n<span class="price-6pm">(.+?)</span>'
        cur_link_re_obj = re.compile(cur_link_re)
        tuples = re.findall(cur_link_re_obj, cur_link)
        if (len(tuples) > 0):
            print tuples[0]
            item_list.extend(list(tuples))
    return item_list

'''generate the item list - format: item, source websites, category, brand, price, lowest price'''
def get_item_json(item_list, category_list, cb_lists, time_string):
    f = open('./data/' + time_string[:-6] + 'item_list', 'w+')
    for i in xrange(0, 10):
        list_len = len(item_list)
        for j in xrange(0, list_len):
            cur_item = item_list[j]
            category = random.choice(category_list)
            cur_item[1] = cur_item[1].replace(',','')
            cur_item[1] = cur_item[1].replace('$','')
            cur_item[2] = cur_item[1].replace(',','')
            cur_item[2] = cur_item[2].replace('$', '')
            cur_string1 = time_string[:-6] + ',' + cur_item[1] + ',' + cur_item[2] + ',' + cur_item[0] + ',' + category + ',' + random.choice(cb_lists)[0] + '\n'
            cur_string2 = time_string[:-6] + ',' + cur_item[1] + ',' + cur_item[2] + ',' + cur_item[0] + ',' + category + ',' + random.choice(cb_lists)[0] + '\n'
            cur_string3 = time_string[:-6] + ',' + cur_item[1] + ',' + cur_item[2] + ',' + cur_item[0] + ',' + category + ',' + random.choice(cb_lists)[0] + '\n'
            cur_string4 = time_string[:-6] + ',' + cur_item[1] + ',' + cur_item[2] + ',' + cur_item[0] + ',' + category + ',' + random.choice(cb_lists)[0] + '\n'
            f.write(cur_string1)
            f.write(cur_string2)
            f.write(cur_string3)
            f.write(cur_string4)
    f.close()

def get_change_price(before_price):
    portion = before_price * 0.1
    return str(round(before_price + random.uniform(-portion, portion), 2))

def item_price_fluctuation(time_string):
    f = open('./data/' + time_string[:-6] + 'item_list', 'w+')
    with open('item_json', 'r') as input:    
        for line in input:
            temp_s = "\"price\":\"$"
            start = line.find(temp_s)
            len_s = len(temp_s)
            temp_e = "\", \""
            end = line.find(temp_e, start, len(line))
            num_string = line[start + len_s: end]
            num_string = num_string.replace(",", "")
            res_string = get_change_price(float(num_string))
            line = line.replace(num_string, res_string)
            f.write(line)
    input.close()
    f.close()


def item_formatter(time_string):
    f = open('./data/' + time_string[:-6] + 'items.txt', 'w+')
    with open('./data/' + time_string[:-6] + 'item_list', 'r') as input:  
        for line in input:
            reg = r'{\"item\":\"(.+?)\", \"price\":\"(.+?)\", \"brand\":\"(.+?)\", \"category\":\"(.+?)\", \"website\":\"(.+?)\"},'
            reg_obj = re.compile(reg)
            reg_list = list(re.findall(reg_obj, line))
            if (len(reg_list) != 0):
                reg_list = reg_list[0]
                list_len = len(reg_list)
                cur_line = time_string[:-6] + ','
                for cur in reg_list:
                    cur = cur.replace(',', '')
                    cur = cur.replace('$', '')
                    cur_line = cur_line + cur + ','
                f.write(cur_line[:-1] + '\n')
            else:
                continue
    input.close()
    f.close()

'''get the gift card information from ebay api'''
def ebay_api_data(input_list, time_string, real = 1):
    if (real == 1):
        f = open('./data/' + time_string[:-6] + 'ebay_gc.txt', 'w+')
    else:
        f = open('./data/' + time_string[:-6] + 'all_ebay_gc', 'w+')
    res = dict()
    size = len(input_list)
    try:
        api = Finding(appid="YuHUANG-insightd-PRD-04d8cb02c-4739185d")
        print size
        for i in xrange(0, size):
            print i
            if (i == 50):
                continue
            cur_list = input_list[i]
            if (cur_list[0] != 'soak-&-sleep'):
                response = api.execute('findItemsAdvanced', {'keywords': cur_list[0] + ' Gift Card'})
                json_data1 = json.dumps(response.dict(), ensure_ascii=True)
                json_data = json.loads(json_data1)
                if (json_data['searchResult']['_count'] == '0'):
                    continue
                json_array = json_data['searchResult']['item']
                array_len = len(json_array)
                for j in xrange(0, array_len):
                    cur_obj = json_array[j]
                    list_info = cur_obj['listingInfo']
                    selling_status = cur_obj['sellingStatus']
                    half1 = time_string[:-6] + ',' + cur_obj['itemId'].replace(',','') + ',' + cur_obj['title'].replace(',','') + ',' + cur_obj['viewItemURL'] + ',' + list_info['buyItNowAvailable'] + ',' + list_info['startTime'] + ','
                    half2 =  list_info['endTime'] + ',' + selling_status['currentPrice']['value'] + ',' + selling_status['currentPrice']['value'] + ',' +cur_obj['autoPay'] + '\n'
                    f.write(half1.encode('utf-8') + half2.encode('utf-8'))
        f.close()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

'''Entrance function of the program'''
def main():

    time_string = get_time()

    brand_list = get_brand_list()
    print 'brand list finished'

    category_list = get_categories()
    print 'category list finished'
    
    html = getHtml("http://www.ebates.com/stores/all/index.htm?navigation_id=22763")
    cb_lists = get_websites_cb_pairs(html)
    print 'cash back list finised'

    ebay_api_data(cb_lists, time_string)
    print 'ebay json get'

    lists_to_json(cb_lists, time_string)
    print 'cash back json get'

    # coupon_generator(cb_lists, category_list, brand_list, time_string)
    # print 'coupon generator finished'

    # item_price_fluctuation(time_string)
    # print 'price fluctuation finished'

    # item_formatter(time_string)
    # print 'clean item data finished'
    
# Running
if __name__ == '__main__':
    main()
