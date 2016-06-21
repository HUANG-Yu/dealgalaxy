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

    f = open('./data/' + time_string + 'all_ebates.txt', 'w+')
    json_array_len = len(json_array)
    for i in xrange(0, json_array_len):
        cur_json = json_array[i]
        x = cur_json['cb'].encode('ascii','ignore')
        if (x[0] == '$' or x[0] == 'U'):
            line = time_string + ',' + cur_json['name'] + ',5.0,' + 'No Google Links Available\n'
            f.write(line)
        elif (x[0] == 'N' or x[0] == 'C' or x[0] == 'I'):
            line = time_string + ',' + cur_json['name'] + ',0.0,' + 'No Google Links Available\n'
        else:
            line = time_string + ',' + cur_json['name'] + ',' + cur_json['cb'][:-1] + ',No Google Links Available\n'
            f.write(line)
    f.close()

def item_formatter(time_string):
    f = open('./data/' + time_string + 'items.txt', 'w+')
    input_string = './' + time_string + '/' + time_string + 'item_list'
    with open(input_string, 'r') as input:  
        for line in input:
            reg = r'{\"item\":\"(.+?)\", \"price\":\"(.+?)\", \"brand\":\"(.+?)\", \"category\":\"(.+?)\", \"website\":\"(.+?)\"},'
            reg_obj = re.compile(reg)
            reg_list = list(re.findall(reg_obj, line))
            print len(reg_list)
            if (len(reg_list) != 0):
                reg_list = reg_list[0]
                list_len = len(reg_list)
                cur_line = time_string + ','
                for cur in reg_list:
                    cur = cur.replace(',', '')
                    cue_line = cur_line + cur + ','
                f.write(cur_line[:-1] + '\n')
            else:
                continue
    input.close()
    f.close()


# def ebay_formatter(time_string):


'''Entrance function of the program'''
def main():
    # ebates_formatter('2016-06-12')
    # coupon_formatter('2016-06-10')
    item_formatter('2016-06-09')

# Running
if __name__ == '__main__':
    main()
