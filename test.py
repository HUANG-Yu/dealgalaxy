import re
import json
import datetime
import random
import urllib
import urllib2
import datetime
import string

'''Get the webpage body in full plain text'''
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    # print(html)
    return html

