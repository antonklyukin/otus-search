#! /usr/bin/env python3
# -*- coding: utf-8 -*-


# import urllib.parse
# import urllib.request
# import urllib.error

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def get_google_page():

    driver = webdriver.Firefox('/home/antony/.local/bin/')
    time.sleep(3)
    driver.get('http://www.google.com')

    submit_element = driver.find_element_by_name("q")
    submit_element.send_keys("NASA")
    time.sleep(1)

    submit_element.submit()
    time.sleep(3)
    print(driver.page_source)

    driver.close()


# def get_page_content(req):
#     try:
#         with urllib.request.urlopen(req) as response:
#             content_charset = response.info().get_content_charset()
#             page_content = response.read().decode(content_charset)

#             return page_content

#     except urllib.error.URLError as err:
#         print(err.reason)
#         print(err.code)


# def get_wikipedia_page():

#     url = 'https://ru.wikipedia.org'

#     host = 'ru.wikipedia.org'
#     user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
#     accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#     accept_language = 'ru,en-US;q=0.7,en;q=0.3'

#     values = {'search' : 'автомобиль'}

#     headers = {'Host' : host,
#                'User-Agent' : user_agent,
#                'Accept' : accept,
#                'Accept-Language' : accept_language}

#     data = urllib.parse.urlencode(values)
#     data = data.encode('ascii')
#     req = urllib.request.Request(url, data, headers)

#     return get_page_content(req)


# def get_duckduckgo_page():

#     user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
#     accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#     accept_language = 'ru,en-US;q=0.7,en;q=0.3'

#     request_headers = { 'User-Agent' : user_agent,
#                         'Accept' : accept,
#                         'Accept-Language' : accept_language}

#     request_data = urllib.parse.urlencode({'q' : 'автомобиль'})
#     req = urllib.request.Request('https://duckduckgo.com/html?' + request_data + '&kl=ru-ru&')
#     req.headers = request_headers

#     return get_page_content(req)


# def crawl_urls(url_list, crawled_urls_list, number_of_urls, url, keyword):
#     crawled_urls_list.append()


if __name__ == "__main__":

    get_google_page()

    # url_list = list()
    # crawled_urls_list = list()
    # number_of_urls = 50
    # url = 'wikipedia.org'

    # crawl_urls(url_list, crawled_urls_list, number_of_urls, url)


# print(get_duckduckgo_page())