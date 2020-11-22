#! /usr/bin/env python3
# -*- coding: utf-8 -*-


from urllib.parse import urlparse, urlunsplit
import argparse
import bs4
import requests
import re


# python3 main.py автомобиль yandex.ru 30 -r csv


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'keyword',
        type=str,
        default="Юпитер",
        help="enter search keyword (Default: Юпитер)",
    )
    parser.add_argument(
        'search_engine',
        type=str,
        default="google.com",
        choices=["google.com", "yandex.ru"],
        help="select search engine (Default: wikipedia.org)",
    )
    parser.add_argument(
        'number', type=int, default=30, help="enter number of results (Default: 30)"
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


class HtmlLink:
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
        return 'URL: ' + str(self.get_url()) + '\n' + 'URL Text: ' + str(self.get_text())


class HtmlPage:
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

    def __init__(self, url, html_code):
        self.__url = url
        self.__html_code = html_code


def get_html_page_code(url: HtmlLink) -> str:
    """
    Функция возвращает HTML-код страницы, либо None, если произошла ошибка.
    :param url: экземпляр класса HtmlLink
    :return: HTML-код страницы
    """
    href = url.get_url()
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
    try:
        req = session.get(href, headers=headers_get, timeout=5)
    except requests.exceptions.RequestException.Timeout as e:
        print('Connection timeout: ' + e)
        return
    except requests.exceptions.ConnectionError as e:
        print('Connection error: ' + e)
        return

    req.encoding = req.apparent_encoding

    return req.text


def html_page_builder(url: HtmlLink) -> HtmlPage:
    """
    Функция построения экземпляра класса HtmlPage
    :param url: Экземпляр класса HtmlLink
    :return: Экземпляр класса HtmlPage
    """

    page_html_code = get_html_page_code(url)
    if page_html_code:
        return HtmlPage(url.get_url(), page_html_code)
    else:
        return


def get_page_from_file(page='google_req.html'):
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
        a_is_from_yandex = True if 'yandex.ru' in a_tag_href else False
        if not a_is_from_yandex:
            link = HtmlLink(str.lower(a_tag_href), a_tag.text)
            links_list.append(link)

    return links_list


def urls_reader(page_html_code):
    page = bs4.BeautifulSoup(page_html_code, 'lxml')

    a_tags = page.find_all('a')

    if len(a_tags) < 1:
        raise ValueError('No anchor tags found')

    for a_tag in a_tags:
        yield a_tag


def clear_href_text(href_text):
    clean_href_text = " ".join(href_text.split())
    clean_href_text = clean_href_text.strip()
    return clean_href_text


def get_urls_from_page(page: HtmlPage):
    found_urls_list = list()

    domain = urlparse(page.get_url()).netloc

    for url in urls_reader(page.get_html_code()):
        # Отлавливаем ссылки без адресов, ссылки с адресами-заглушками или ссылки из непечатных символов
        if not ('href' in url.attrs) or (url.attrs['href'] == '#'):
            continue

        url_address = urlparse(url.attrs['href'])

        # Отлавливаем всякие tel: в схеме
        if url_address.scheme and ('http' not in url_address.scheme):
            continue

        scheme = url_address.scheme if url_address.scheme else 'http'
        netloc = url_address.netloc if url_address.netloc else domain

        new_url_address = str()
        # Генерируем новый URL, если в исходном нет схемы и домена
        if (not url_address.netloc) or (not url_address.scheme):
            new_url_address = urlunsplit([scheme, netloc, str.strip(url_address.path),
                                          str.strip(url_address.query), str.strip(url_address.fragment)])

        # Проверка ссылки на ссылку на себя, пропускаем такие ссылки
        url_regex = re.compile(r'^https?://' + domain + r'/?$')
        if url_regex.match(new_url_address):
            continue
        if new_url_address == '':
            continue

        url = HtmlLink(new_url_address, url.text)
        found_urls_list.append(url)

    return found_urls_list


def main():
    args = get_args()

    keyword = args.keyword
    search_engine = args.search_engine
    number = args.number
    recursive = args.recursive
    export_format = args.export_format

    urls_list = parse_yandex_links()

    html_pages_list = list()

    for url in urls_list:
        page = html_page_builder(url)
        if page:
            html_pages_list.append(page)

    urls_list = list()

    for page in html_pages_list:
        page_links = get_urls_from_page(page)
        urls_list.extend(page_links)

    print(urls_list)


if __name__ == "__main__":
    main()

# Александр Телеграм
# +16692138826
