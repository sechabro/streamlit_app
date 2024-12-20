# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye
WORKDIR /app

COPY ./app.py .
COPY ./.streamlit .
COPY ./pages .
COPY ./requirements.txt .
COPY ./__init__.py .

RUN chmod +x ./app.py && pip3 install -r requirements.txt

ENV BCSV=/server/data/data.csv
ENV PORT=8501
ENV HOST=0.0.0.0

CMD streamlit run --server.port ${PORT} --server.address ${HOST} ./app.py