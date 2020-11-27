FROM python:3.8
LABEL maintainer="antonklyukin@gmail.com"

COPY requirements.txt /opt/otus-search/requirements.txt

WORKDIR /opt/otus-search

RUN pip install -r requirements.txt

COPY . /opt/otus-search

CMD ["/bin/bash"]

# Пример запуска приложения внутри контейнера
# python main.py гагарин yandex.ru 3000 -r csv