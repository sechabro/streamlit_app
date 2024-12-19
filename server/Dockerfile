# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye
WORKDIR /process

COPY ./ .

RUN chmod +x ./server.py && chmod +x ./data_sorter.py && chmod +x ./utils.py
RUN pip3 install -r requirements.txt

ENV BCSV=/app/data.csv
EXPOSE 3000

CMD export FINN=$(cat key.txt) && \
    rm key.txt