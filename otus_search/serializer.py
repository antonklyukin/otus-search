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

    file_name = f'urls-{get_file_suffix()}.csv'

    with open(file_name, 'w') as csv_file:

        url_writer = csv.writer(csv_file,
                                delimiter='\t',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)

        for url in urls:
            url_writer.writerow(url)

    create_file_success_message(file_name)

    export_success_message(len(urls), 'csv')

    return True


def save_to_json(urls: int):

    file_name = f'urls-{get_file_suffix()}.json'

    with open(file_name, 'w') as json_file:

        json.dump(urls, json_file, indent=4, ensure_ascii=False)

    create_file_success_message(file_name)

    export_success_message(len(urls), 'json')


def export_success_message(number_of_urls, export_format):

    print(f'Ссылки в количестве {number_of_urls} сохранены' +
          f' в формате {str.upper(export_format)}.')


def create_file_success_message(file_name):
    print(f'Создан файл {file_name}.')


def export_urls(urls, export_format):

    if export_format == 'csv':
        save_to_csv(urls)

    elif export_format == 'json':
        save_to_json(urls)
