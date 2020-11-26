#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import datetime


def get_file_suffix():

    date_today = datetime.datetime.today()
    t_data = date_today.timetuple()
    file_suffix = (f'{t_data[0]}-{t_data[1]}-{t_data[2]-t_data[3]}:'
                   f'{t_data[4]}:{t_data[5]}')

    return file_suffix


def save_to_csv(urls: int):

    with open(f'urls-{get_file_suffix()}.csv', 'w') as csv_file:

        url_writer = csv.writer(csv_file,
                                delimiter='\t',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

        for url in urls:
            url_writer.writerow(url)

    return True


def save_to_json(urls: int):

    with open(f'urls-{get_file_suffix()}.json', 'w') as json_file:

        json.dump(urls, json_file, indent=4, ensure_ascii=False)

    return True


def export_success_message(number_of_urls, export_format):

    print(f'Ссылки в количестве {number_of_urls} сохранены' +
          f' в формате {str.upper(export_format)}.')


def export_urls(urls, export_format):

    number_of_urls = len(urls)

    if export_format == 'csv':

        if save_to_csv(urls):
            export_success_message(number_of_urls, export_format)

    elif export_format == 'json':
        if save_to_json(urls):
            export_success_message(number_of_urls, export_format)
