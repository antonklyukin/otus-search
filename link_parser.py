#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser

def parse_html_data(file_name):
    with open(file_name) as f:
        return f.read()

html_data = parse_html_data("duckduckgo.txt")


class HtmlLinkParser(HTMLParser):

    link_href = str() # Current found href
    link_data = str() # Current found link data
    links_list = list()
    in_tag_a = False

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.in_tag_a = True
            self.in_tag_a_data = ''
            for attr in attrs:
                if attr[0] == 'href':
                    self.link_href = attr[1]

    def handle_data(self, data):
        if self.in_tag_a:
            data = ' '.join(data.split())
            space = str()
            if self.link_data:
                space = ' '
            self.link_data += space + data


    def handle_endtag(self, tag):
        if tag == 'a':
            self.links_list.append([self.link_href, self.link_data])
            self.in_tag_a = False
            self.link_data = ''


html_parser = HtmlLinkParser()

html_parser.feed(parse_html_data('duckduckgo.txt'))

uniq_links_list = []

# for links in html_parser.links_list:



# for link in html_parser.links_list:
#     uniq_links.add(link)

# for i, link in enumerate(uniq_links):
#     print(f' Ссылка {i}: \n href: {link[0]} \n text: {link[1]}')
