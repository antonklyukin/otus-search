#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import bs4
from urllib.parse import urlparse, urlunsplit
import re

headers_get = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0)" +
    " Gecko/20100101 Firefox/49.0",
    "Accept":
    "text/html,application/xhtml+xml,application/xml;" + "q=0.9,*/*;q=0.8",
    "Accept-Language": "ru_RU,en-US,en,ru;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def get_page_from_file(page='google_req.html'):
    """
    Функция извлечения страниц-заглушек с 'выхлопом' поисковиков для 
    тестирования
    """

    f = open(page)
    page_content = f.read()
    return page_content


def parse_google(keyword):
    req_href = f'https://google.com/search?q={keyword}&oq={keyword}'
    links_dict = list()

    # html_page = get_page_from_file()
    html_page = get_html_page_code(req_href)

    page_html_tree = bs4.BeautifulSoup(html_page, "lxml")
    div_rc_list = page_html_tree.select('div[class="rc"]')

    for div_rc in div_rc_list:
        a_tags = div_rc.find_all("a")
        for a in a_tags:
            a_from_cache = (True if "webcache.googleusercontent.com"
                            not in a.attrs["href"] else False)
            a_not_related = (True if "search?q=related" not in a.attrs["href"]
                             else False)
            a_has_hash = True if "#" in a.attrs["href"] else False

            if not a_has_hash and a_not_related and a_from_cache:
                links_dict.append((a.attrs["href"], a.text))
    return links_dict[:10]


def parse_yandex(keyword):

    req_href = f'https://yandex.ru/search/?lr=213&text={keyword}'
    links_list = list()

    html_page = get_html_page_code(req_href)
    page_html_tree = bs4.BeautifulSoup(html_page, "lxml")
    li_list = page_html_tree.select('li[class="serp-item"]')

    for list_item in li_list:
        a_tag = list_item.find("a")
        a_tag_href = a_tag.attrs["href"]
        a_is_from_yandex = True if 'yandex.ru' in a_tag_href else False
        if not a_is_from_yandex:
            link = (str.lower(a_tag_href), a_tag.text)
            links_list.append(link)

    return links_list[:10]


def get_html_page_code(href: str) -> str:
    """
    Функция возвращает HTML-код страницы, либо None, если произошла ошибка.
    :param url_href: str - валидная ссылка
    :return: str - HTML-код страницы
    """

    session = requests.Session()
    try:
        req = session.get(href, headers=headers_get, timeout=5)
    except requests.exceptions.Timeout as e:
        print('Connection timeout: ' + e)
        return
    except requests.exceptions.ConnectionError as e:
        print('Connection error: ' + e)
        return

    req.encoding = req.apparent_encoding

    return req.text


def clear_a_text(href_text: str) -> str:
    """
    Функция удяляет пробелы из текста тега <a>
    """
    clean_href_text = " ".join(href_text.split())
    clean_href_text = clean_href_text.strip()

    return clean_href_text


def get_urls_from_html(html_text, self_href) -> list:
    """
    Функция собирает все теги <a> на странице и возвращает список кортежей вида
    (url_href, url_text)
    :param html_page: tuple вида (page_href, page_html_text) 
    """

    page_href = self_href
    page_html_text = html_text

    found_urls_list = list()

    domain = urlparse(page_href).netloc

    page = bs4.BeautifulSoup(page_html_text, 'lxml')

    a_tags = page.find_all('a')

    if len(a_tags) < 1:
        return [('', '')]

    for url in a_tags:
        # Отлавливаем ссылки без адресов, ссылки с адресами-заглушками
        if not ('href' in url.attrs) or ('#' in url.attrs['href']):
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
            new_url_address = urlunsplit([
                scheme, netloc,
                str.strip(url_address.path),
                str.strip(url_address.query),
                str.strip(url_address.fragment)
            ])

        # Проверка ссылки на ссылку на себя, пропускаем такие ссылки
        url_regex = re.compile(r'^https?://' + domain + r'/?$')
        if url_regex.match(new_url_address):
            continue
        if (not new_url_address) or (url.text in ['', '↑']):
            continue

        url = (new_url_address, clear_a_text(url.text))

        found_urls_list.append(url)

    print(f'На данной странице найдено {len(found_urls_list)} ссылок.')

    return found_urls_list


def get_urls_by_url(url: tuple):

    print(f'Обрабатывается ссылка URL: {url[0]}')

    page_html = get_html_page_code(url[0])
    url_list = get_urls_from_html(page_html, url[0])

    return url_list


def crawl_urls(urls: list, number_of_urls: int, visited_urls=[]):
    '''
    Функция рекурсивного поиска ссылок.
    :param urls: list of tuples(page_href, page_html_text),
            number_of_urls number of requied urls
    '''

    while len(urls) + len(visited_urls) < number_of_urls:

        urls_to_crawl = urls[:]

        for url in urls_to_crawl:

            del (urls[0])

            visited_urls.append(url)

            found_urls = get_urls_by_url(url)

            urls.extend(found_urls)

            print(f'Посещено {len(visited_urls)} ссылок.')
            print(f'Найдено {len(urls)} ссылок.')

            if len(urls) + len(visited_urls) >= number_of_urls:
                break

        crawl_urls(urls, number_of_urls, visited_urls)

    urls.extend(visited_urls)

    return urls[:number_of_urls]


def test_crawler():
    urls = [('http://pythonz.net/references/named/object.__contains__/',
             'Описание object.__contains__ в Python'),
            ('https://ru.wikipedia.org/wiki/%D0%90%D0%B2%D1%82%D0%BE%D0%BC%D' +
             '0%BE%D0%B1%D0%B8%D0%BB%D1%8C', 'Википедия')]

    new_urls = crawl_urls(urls, 10000)

    print(len(new_urls))


if __name__ == '__main__':
    test_crawler()
