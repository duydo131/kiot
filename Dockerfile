FROM python:3.9
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir /code
WORKDIR /code
COPY ./apps /code/apps
COPY ./config /code/config
COPY ./core /code/core
COPY ./entrypoint.sh /code/entrypoint.sh
COPY ./manage.py /code/manage.py
COPY ./ftechcache-0.1.3.tar.gz /code/ftechcache-0.1.3.tar.gz
RUN pip install ftechcache-0.1.3.tar.gz

CMD ["bash", "./entrypoint.sh"]