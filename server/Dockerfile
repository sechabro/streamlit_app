# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye
WORKDIR /server

COPY ./ .

RUN chmod +x ./server.py && chmod +x ./data_sorter.py && chmod +x ./utils.py && pip3 install -r requirements.txt

ENV BCSV=/server/data/data.csv
EXPOSE 3000

CMD echo "heeeyyyyyy"