#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from urllib.parse import urlparse
import argparse
import bs4
import requests
import re

# python3 main.py автомобиль yandex.ru 30 -r csv


def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "keyword",
        type=str,
        default="Юпитер",
        help="enter search keyword (Default: Юпитер)",
    )
    parser.add_argument(
        "searchengine",
        type=str,
        default="google.com",
        choices=["google.com", "yandex.ru"],
        help="select search engine (Default: wikipedia.org)",
    )
    parser.add_argument(
        "number", type=int, default=30, help="enter number of results (Default: 30)"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="recursive search (Default: False)",
    )
    parser.add_argument(
        "export_format",
        type=str,
        default="csv",
        choices=["csv", "xml", "json"],
        help="enter export format (Default: csv)",
    )

    return parser.parse_args()

class Link:
    """
    Класс гиперссылки
    """
    __text = str()
    __url = str()

    def set_text(self, text):
        self.__text = text

    def get_text(self):
        return self.__text

    def set_url(self, url):
        self.__url = url

    def get_url(self):
        return self.__url

    def __init__(self, url, text):
        self.__url = url
        self.__text = text

    def __repr__(self):
        print('URL: ' + str(self.get_url()) + '\n' + 'URL Text: ' + str(self.get_text()))


class Page:
    """
    Класс страницы
    """
    __html_code = str()
    __url = str()

    def set_html_code(self, html_code):
        self.__html_code = html_code

    def get_html_code(self):
        return self.__html_code

    def set_url(self, url):
        self.__url = url

    def get_url(self):
        return self.__url

    def __init__(self, url):
        self.__url = url
        self.get_page_html_code()

    def get_page_html_code(self):
        headers_get = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru_RU,en-US,en,ru;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }

        session = requests.Session()
        req = session.get(self.__url, headers=headers_get)
        req.encoding = req.apparent_encoding

        self.__html_code = req.text



def get_page_from_file(page="google_req.html"):
    """
    Функция извлечения страницы по ссылке
    """

    f = open(page)
    page_content = f.read()
    return page_content


def parse_google_links():
    links_dict = list()
    html_page = get_page_from_file()
    page_html_tree = bs4.BeautifulSoup(html_page, "lxml")
    div_rc_list = page_html_tree.select('div[class="rc"]')

    for div_rc in div_rc_list:
        a_tags = div_rc.find_all("a")
        for a in a_tags:
            a_from_cache = (
                True
                if "webcache.googleusercontent.com" not in a.attrs["href"]
                else False
            )
            a_not_related = True if "search?q=related" not in a.attrs["href"] else False
            a_has_hash = True if "#" in a.attrs["href"] else False

            if not a_has_hash and a_not_related and a_from_cache:
                links_dict.append([a.attrs["href"], a.text])
    return links_dict


def parse_yandex_links():
    links_list = list()
    html_page = get_page_from_file("yandex_req.html")
    page_html_tree = bs4.BeautifulSoup(html_page, "lxml")
    li_list = page_html_tree.select('li[class="serp-item"]')

    for list_item in li_list:
        a_tag = list_item.find("a")
        a_tag_href = a_tag.attrs["href"]
        a_is_from_yandex = True if "yandex.ru" in a_tag_href else False
        if not a_is_from_yandex:
            link = Link(str.lower(a_tag_href), a_tag.text)
            links_list.append(link)

    return links_list


def urls_reader(page_html_code):
    page = bs4.BeautifulSoup(page_html_code, "lxml")

    a_tags = page.find_all("a")

    # if len(a_tags) < 1:
    #     raise ValueError('No anchor tags found')

    for a_tag in a_tags:
        yield a_tag


def get_domain_from_url(url):
    return urlparse(url).netloc


def get_urls_from_page(page):

    domain = get_domain_from_url(page.get_url())

    reg = re.compile(r"[^\s\n]+")

    for url in urls_reader(page.get_page_html_code()):
        if not ('href' in url.attrs):
            next
        if url.attrs['href'].startswith("/"):
            url.attrs['href'] = domain + url.attrs['href']
        if (reg.match(url.attrs['href'])) and ("#" not in url.attrs['href']):
            print(url.text, url.attrs['href'], "\n")


def main():
    args = get_args()

    keyword = args.keyword
    searchengine = args.searchengine
    number = args.number
    recursive = args.recursive
    export_format = args.export_format

    urls_list = parse_yandex_links()

    print(urls_list)

    # test_page = Page(urls_list[1][0])

    # get_urls_from_page(test_page)




if __name__ == "__main__":
    main()

# Александр Телеграм
# +16692138826 