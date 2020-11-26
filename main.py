#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# ЗАДАНИЕ 01
# Консольная утилита по сбору ссылок с сайтов
# -------------------------------------------

# Пример использования:
# python main.py гагарин yandex.ru 3000 -r csv
# python main.py синхрофазотрон google.com 1000 json

from otus_crawler.argparser import get_args
from otus_crawler.webparser import (parse_yandex, parse_google,
                                    get_urls_by_url, crawl_urls)
from otus_crawler.serializer import export_urls


def process_urls(urls: list, number_of_urls: int, recursively: bool) -> list:
    """
    Функция сбора ссылок
    """

    found_urls = list()
    if not recursively:
        #"Добор" ссылок с поисковиков в случае нехватки нужного количества
        # ссылок не реализован, лучше воспользоваться ключом -r

        # Добавляем ссылки, найденные в поисковиках
        found_urls.extend(urls)

        for url in urls:

            urls_from_url = get_urls_by_url(url)

            found_urls.extend(urls_from_url)
            # Останавливаем сбор ссылок, если их число больше нужного
            if len(found_urls) >= number_of_urls:
                break
        # Отсекаем излишек ссылок
        found_urls = found_urls[:number_of_urls]

    else:
        # Начинаем рекурсивный сбор
        found_urls = crawl_urls(urls, number_of_urls)

    return found_urls


def main():

    args = get_args()

    keyword = args.keyword
    search_engine = args.search_engine
    number_of_urls = args.number
    recursively = args.recursively  # True or False
    export_format = args.export_format

    urls = list()

    if search_engine == 'yandex.ru':
        # Ограничиваем количество запросов к поисковикам одной страницей выдачи
        urls = parse_yandex(keyword)

    elif search_engine == 'google.com':
        urls = parse_google(keyword)

    urls = process_urls(urls, number_of_urls, recursively)

    export_urls(urls, export_format)


if __name__ == "__main__":
    main()
