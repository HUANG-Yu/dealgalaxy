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
    x = 0
    res = list()
    for pair in sites_list1 + sites_list2 + sites_list3:
        url = 'https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=%s' % pair[0]
        cur_list = list(pair)
        # uncomment to change hyphen to space for more readability
        # cur_list[0] = cur_list[0].replace("-", " ")
        # print cur_list[0]
        cur_list.append(url)
        # print x
        # print cur_list
        res.append(cur_list)
        x = x + 1
    # print x
    return res

'''Get thos websites tuples whose cash back doubles'''
def get_double_cb_websites(html):
    sites_reg = r'title="Get a great deal from (.+?) plus (.+?)% Cash Back from Ebates!"'
    sites_re_obj = re.compile(sites_reg)
    sites_list = re.findall(sites_re_obj, html)
    i = 0
    unique_sites = set(sites_list)
    for double_cb in unique_sites:
        # print double_cb
        i = i + 1
    print i

# method broken because of Google encryption
def get_website_links(cur_html):
    link_re = r',event\)" data\-href="(.+?)">'
    link_re_obj = re.compile(link_re)
    link_list = re.findall(link_re_obj, cur_html)
    x = 0
    for link in link_list:
        # print link
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
    res = list()
    for each in tuple1 + tuple2:
        url = 'https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=%s' % each[0]
        cur_list = list(each)
        # uncomment to change hyphen to space for more readability
        # cur_list[0] = cur_list[0].replace("-", " ")
        cur_list.append(url)
        # print cur_list
        res.append(cur_list)
        x = x + 1
    # res.append(x)
    # print x
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
        f.write("]")
        f.close()
    except ConnectionError as e:
        print(e)
        print(e.response.dict())

'''enlarge the cash back links dataset'''
def create_duplicates_cb_links(cb_lists):
    new_list = list()
    i = len(cb_lists) // 2
    for x in xrange(0, i):
        for cur_list in cb_lists:
            cur_list[0] = link_generator()
            cur_list[2] = cur_list[2] + random.choice(string.letters)
            # print cur_list
            new_list.append(cur_list)
    new_list = cb_lists + new_list
    # print len(new_list)
    return new_list

'''generate website links'''
def link_generator(size=40, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

'''enlarge the cash back increase websites'''
def create_duplicates_increase_cb_links(cb_increase_lists):
    new_list = list()
    i = len(cb_increase_lists)
    for x in range(0, i):
        for cur_list in cb_increase_lists:
            # skip the last info, which contain just one number
            if (type(cur_list) != int):
                cur_list[0] = 'www' + link_generator()
                cur_list[3] = cur_list[3] + random.choice(string.letters)
                # print cur_list
                new_list.append(cur_list)
    new_list = cb_increase_lists + new_list
    # print len(new_list)
    return new_list


'''convert full lists with three parameters to json object to store them in s3/spark'''
def lists_to_json(cb_lists, time_string, real = 1):
    if (real == 1):
        f = open('./data/' + time_string[:-6] + 'ebates', 'w+')
    else:
        f = open('./data/' + time_string[:-6] + 'all_ebates', 'w+')
    f.write("[")
    list_len = len(cb_lists)
    for i in xrange(0, list_len):
        cur_list = cb_lists[i]
        if (i != list_len - 1):
            cur_item = "{\"name\":\"" + cur_list[0] + "\", \"cb\":\"" + cur_list[1] + "\", \"link\":\"" + cur_list[2] + "\"}, \n"
            f.write(cur_item)
        else:
            cur_item = "{\"name\":\"" + cur_list[0] + "\", \"cb\":\"" + cur_list[1] + "\", \"link\":\"" + cur_list[2] + "\"}] \n"
            f.write(cur_item)
    f.close()

'''convert increase cash back websites lists with four parameters into json object to store them in s3/spark'''
def increase_lists_to_json(increase_lists, time_string, real = 1):
    if (real == 1):
        f = open('./data/' + time_string[:-6] + 'ebates_increase', 'w+')
    else:
        f = open('./data/' + time_string[:-6] + 'all_ebates_increase', 'w+')
    f.write("[")
    list_len = len(increase_lists)
    for i in xrange(0, list_len):
        cur_list = increase_lists[i]
        if (i != list_len - 1):
            cur_item = "{\"name\":\"" + cur_list[0] + "\", \"cur_cb\":\"" + str(cur_list[1]) + "\", \"past_cb\":\"" + str(cur_list[2]) + "\", \"link\":\"" + cur_list[3] + "\"}, \n"
            f.write(cur_item)
        else:
            cur_item = "{\"name\":\"" + cur_list[0] + "\", \"cur_cb\":\"" + str(cur_list[1]) + "\", \"past_cb\":\"" + str(cur_list[2]) + "\", \"link\":\"" + cur_list[3] + "\"] \n"
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
            # print cur_brand
    # print len(brand_list)
    # print brand_list
    return brand_list

'''generate the category from the json file converted from the exel template offered by Google'''
def get_categories():
    with open('walmart_categories_json') as data_file:    
        data = json.load(data_file)
    # pprint(data)
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
            # print sub_cur_json['name']
        # print cur_json['name']
    # print len(category_list)
    return category_list

'''generate the coupon code which consists of uppercase letter and digts in random order'''
def coupon_code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

'''generate the coupon for given websites - format: websites, coupon code, category, brands, start dates, expire dates'''
def coupon_generator(cb_lists, category_list, brand_list, time_string):
    f = open('./data/' + time_string[:-6] + 'coupon', 'w+')
    f.write("[")
    cb_len = len(cb_lists)
    for j in xrange(0, 6):
        for i in range(0, cb_len):
            if (j != 9 and i != cb_len - 1):
                time_pair1 = get_time_pair()
                time_pair2 = get_time_pair()
                cur_item1 = "{\"name\":\"" + random.choice(cb_lists)[0] + "\", \"coupon\":\"" + coupon_code_generator() + "\", \"category\":\"" + random.choice(category_list) + "\", \"discount\":\"" + str(round(random.random()/4, 2) + 0.05) + "\", \"start\":\""  + time_pair1[0] + "\", \"end\":\"" + time_pair1[1] + "\"},\n "
                cur_item2 = "{\"name\":\"" + random.choice(cb_lists)[0] + "\", \"coupon\":\"" + coupon_code_generator() + "\", \"category\":\"" + random.choice(category_list) + "\", \"discount\":\"" + str(round(random.random()/4, 3) + 0.05) + "\", \"start\":\""  + time_pair2[0] + "\", \"end\":\"" + time_pair2[1] + "\"},\n "
                # + "{\"name\":\"" + cur_list[0] + "\", \"cb\":\"" + cur_list[1] + "\", \"link\":\"" + cur_list[2] + "\"},\n "
                f.write(cur_item1)
                f.write(cur_item2)
            else:
                time_pair1 = get_time_pair()
                time_pair2 = get_time_pair()
                cur_item1 = "{\"name\":\"" + random.choice(cb_lists)[0] + "\", \"coupon\":\"" + coupon_code_generator() + "\", \"category\":\"" + random.choice(category_list) + "\", \"discount\":\"" + str(round(random.random()/4, 2) + 0.05) + "\", \"start\":\""  + time_pair1[0] + "\", \"end\":\"" + time_pair1[1] + "\"},\n "
                cur_item2 = "{\"name\":\"" + random.choice(cb_lists)[0] + "\", \"coupon\":\"" + coupon_code_generator() + "\", \"category\":\"" + random.choice(category_list) + "\", \"discount\":\"" + str(round(random.random()/4, 3) + 0.05) + "\", \"start\":\""  + time_pair2[0] + "\", \"end\":\"" + time_pair2[1] + "\"}]\n "
                # + "{\"name\":\"" + cur_list[0] + "\", \"cb\":\"" + cur_list[1] + "\", \"link\":\"" + cur_list[2] + "\"},\n "
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
    # print start_time
    # print end_time
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
    # print item_list
    return item_list

'''generate the item list - format: item, source websites, category, brand, price, lowest price'''
def get_item_json(item_list, category_list, cb_lists, time_string):
    f = open('./data/' + time_string[:-6] + 'item_list', 'w+')
    f.write("[")
    for i in xrange(0, 30):
        list_len = len(item_list)
        for j in xrange(0, list_len):
            cur_item = item_list[j]
            category = random.choice(category_list)
            # print cur_item
            if (i != 1 and j != list_len - 1):
                cur_string1 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"}, \n"
                cur_string2 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"}, \n"
                cur_string3 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"}, \n"
                cur_string4 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"}, \n"
                f.write(cur_string1)
                f.write(cur_string2)
                f.write(cur_string3)
                f.write(cur_string4)
            else:
                cur_string1 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"}, \n"
                cur_string2 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"}, \n"
                cur_string3 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"}, \n"
                cur_string4 = "{\"item\":\"" + cur_item[1] + "\", \"price\":\"" + cur_item[2] + "\", \"brand\":\"" + cur_item[0] + "\", \"category\":\"" + category + "\", \"website\":\"" + random.choice(cb_lists)[0] + "\"} ]\n"
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
            # print line
            # print start
            # print end
            num_string = line[start + len_s: end]
            # print num_string
            num_string = num_string.replace(",", "")
            # print num_string
            res_string = get_change_price(float(num_string))
            line = line.replace(num_string, res_string)
            f.write(line)
    input.close()
    f.close()

'''Entrance function of the program'''
def main():
    time_string = get_time()

    item_price_fluctuation(time_string)
    
    brand_list = get_brand_list()
    print 'brand list finished'

    category_list = get_categories()
    print 'category list finished'

    html = getHtml("http://www.ebates.com/stores/all/index.htm?navigation_id=22763")
    cb_lists = get_websites_cb_pairs(html)
    print 'cash back list finised'

    lists_to_json(cb_lists, time_string)
    print 'cash back json get'

    duplicates_lists = create_duplicates_cb_links(cb_lists)
    print 'duplicate list finished'

    lists_to_json(duplicates_lists, time_string, 2)
    print 'duplicates cash back list finished'

    cb_increase_lists = cb_increase_websites(html)
    increase_lists_to_json(cb_increase_lists, time_string)
    print 'increase cash back json get'

    ebay_api_data(cb_lists, time_string)
    print 'ebay json get'

    # ebay_api_data(duplicates_lists, time_string)
    # print 'duplicates ebay json get'    

    coupon_generator(duplicates_lists, category_list, brand_list, time_string)
    print 'coupon generator finished'
    

    '''
    needed only for first time
    item_list = get_item_list()
    print 'item list finished'

    get_item_json(item_list, category_list, cb_lists, time_string)
    print 'item json finished'
    '''

# Running
if __name__ == '__main__':
    main()
