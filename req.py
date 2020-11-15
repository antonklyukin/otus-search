import requests
import bs4

# y = requests.get('https://yandex.ru/search/?lr=213&text=%D0%B0%D0%B2%D1%82%D0%BE%D0%BC%D0%BE%D0%B1%D0%B8%D0%BB%D1%8C')
# g = requests.get('https://google.com/search?q=автомобиль&oq=автомобиль')


headers_get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru_RU,en-US,en,ru;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }


def google(q, number):
    s = requests.Session()
    q = '+'.join(q.split())
    url = 'https://www.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8' + '&num=' + str(number)
    r = s.get(url, headers=headers_get)

    return r.text

print(google('автомобиль', 50))