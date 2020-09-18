#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import urllib.parse
import urllib.request

def get_yandex_result():

    url = 'https://yandex.ru/search/'

    host = 'yandex.ru'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    accept_language = 'ru,en-US;q=0.7,en;q=0.3'
    accept_encoding = 'gzip, deflate, br'
    connection = 'keep-alive'
    upgrade_insecure_requests = '1'

    values = {'text' : 'автомобиль' }

    headers = {'Host' : host,
               'User-Agent' : user_agent,
               'Accept' : accept,
               'Accept-Language' : accept_language,
               'Accept-Encoding' : accept_encoding,
               'Connection' : connection,
               'Upgrade-Insecure-Requests' : upgrade_insecure_requests}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
        the_page = response.read().decode('utf-8')
        print(the_page)


get_yandex_result()