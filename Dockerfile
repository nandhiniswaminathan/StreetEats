FROM python:3.8-slim-buster

RUN mkdir /streeteats
COPY requirements.txt /streeteats
WORKDIR /streeteats
RUN pip3 install -r requirements.txt

COPY . /streeteats

RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
