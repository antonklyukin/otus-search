#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


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
        choices=["google.com", "yandex.ru", "duckduckgo.org"],
        help="select search engine (Default: duckduckgo.org)",
    )
    parser.add_argument('number',
                        type=int,
                        default=30,
                        help='enter number of results' + ' (Default: 30)')
    parser.add_argument(
        "-r",
        "--recursively",
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