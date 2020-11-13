#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def get_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('-k','--keyword', type=str, default='Юпитер',
                        help='enter search keyword (Default: Юпитер)')
    parser.add_argument('-s','--searchengine', type=str,
                        default='wikipedia.org',
                        choices=['wikipedia.org',
                        'duckduckgo.com'],
                        help='select search engine (Default: wikipedia.org)')
    parser.add_argument('-n','--number', type=int, default=30,
                        help='enter number of results (Default: 30)')
    parser.add_argument('-r', '--recursive', action="store_true",
                        help='recursive search (Default: False)')
    parser.add_argument('-e','--export', type=str, default='csv',
                        choices=['csv', 'xml', 'json'],
                        help='enter export format (Default: csv)')

    return parser.parse_args()


def main():
    args = get_args()

    keyword = args.keyword
    searchengine = args.searchrngine
    number = args.number
    recursive = args.recursive
    export_format = args.export_format


if __name__ == "__main__":
    main() 
