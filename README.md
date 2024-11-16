# Streamlit Websocket Application

Dockerfile not included. Environment variable "FINN" contains Finnub API key.

```
FROM python:3.11-slim-bullseye

WORKDIR /app

COPY ./ .

RUN chmod +x ./server.py
RUN chmod +x ./app.py
RUN chmod +x ./utils.py
RUN pip3 install -r requirements.txt

ENV FINN="<API KEY HERE>"
ENV BCSV=/app/data.csv
ENV PORT=8501
ENV HOST=0.0.0.0

CMD streamlit run --server.port ${PORT} --server.address ${HOST} ./app.py
```

The Dockerfile also moves a "key.txt" file into its container image. This file contains the Finnhub API key. You'll need to create this file with your own API key in order to run this app at all.

Deploying to Heroku via CLI:
heroku login
heroku container:login
heroku container:push web -a <image_name>
heroku container:release web -a <image_name>
heroku open -a <image_name>