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

CMD ["bash", "./entrypoint.sh"]