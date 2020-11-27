FROM python:3.8
LABEL maintainer="antonklyukin@gmail.com"

COPY requirements.txt /opt/otus-search/requirements.txt

WORKDIR /opt/otus-search

RUN pip install -r requirements.txt

COPY . /opt/otus-search

CMD ["/bin/bash"]