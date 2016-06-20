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
import unicodedata

def get_time():
    time  = datetime.datetime.now()
    # round to the next full hour
    time -= datetime.timedelta(minutes = time.minute, seconds = time.second, microseconds =  time.microsecond)
    time += datetime.timedelta(hours = 1)
    time_string = time.strftime("%Y-%m-%d_%H-%M")
    # print time_string
    return time_string

def ebates_formatter(time_string):
    input_string = './' + time_string + '/' + time_string + 'all_ebates'
    json_data=open(input_string).read()
    json_array = json.loads(json_data)

    f = open('./data/' + time_string + 'ebates.txt', 'w+')
    json_array_len = len(json_array)
    for i in xrange(0, json_array_len):
        cur_json = json_array[i]
        x = cur_json['cb'].encode('ascii','ignore')
        if (x[0] == '$' or x[0] == 'U'):
            line = time_string + ',' + cur_json['name'] + ',5.0,' + cur_json['link'] + '\n'
            f.write(line)
        elif (x[0] == 'N' or x[0] == 'C' or x[0] == 'I'):
            line = time_string + ',' + cur_json['name'] + ',0.0,' + cur_json['link'] + '\n'
        else:
            line = time_string + ',' + cur_json['name'] + ',' + cur_json['cb'][:-1] + ',' + cur_json['link'] + '\n'
            f.write(line)
    f.close()

def coupon_formatter(time_string):
    input_string = './2016-06-10/' + time_string + 'coupon.txt'
    json_data=open(input_string).read()
    json_array = json.loads(json_data)

    f = open('./data/' + time_string + 'coupon', 'w+')
    json_array_len = len(json_array)
    for i in xrange(0, json_array_len/10):
        cur_json = json_array[i]
        line = time_string + ',' + cur_json['name'] + ',' + cur_json['coupon'] + ', ' + cur_json['category'] + cur_json['discount'] + cur_json['start'] + cur_json['end'] + '\n'
        f.write(line)
    f.close()



# def ebay_formatter(time_string):


'''Entrance function of the program'''
def main():
    ebates_formatter('2016-06-09')
    # coupon_formatter('2016-06-10')

# Running
if __name__ == '__main__':
    main()
