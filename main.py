#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import bs4


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


def get_page_from_file(page="google_req.html"):
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
    return(links_dict)


def main():
    args = get_args()

    keyword = args.keyword
    searchengine = args.searchengine
    number = args.number
    recursive = args.recursive
    export_format = args.export_format

    print(parse_google_links())


if __name__ == "__main__":
    main()
