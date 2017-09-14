# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import re
def QSearch(string):
    non_chi_pat = u'[^\u4e00-\u9fff]'
    values = {
        'key' : 'a48c58912414b2b1fa65ccf74aff5ef03fceeb543ec306cc0f6debdb37159c04',
        'message' : string,
        'format' : 'json',
        }

    url = 'http://api.qsearch.cc/api/tokenizing/v1/segment?'
    url_values = urllib.parse.urlencode(values)
    response = urllib.request.Request(url+url_values)
    response_body = urllib.request.urlopen(response).read().decode('utf-8')
    words = ''
    line = ''
    string = ''
    for i in response_body:
        if i == '[' or i == '\"':
            continue
        elif i == ']':
            if string == ' \\n':
                string = '\n'
            line = line.strip() + string
            words += line
            break
        elif i == ',':
            if string == ' \\n':
                string = '\n'
                line = line.strip() + string
                words += line
                line = ''
            line += string
            string = ''
        else:
            string += i
    return words                

if __name__ == '__main__':
    f = open('GG.txt','r')
    QSearch(f.read())
