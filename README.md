# Streamlit Cryptocurrency Live Data Feed #

## Dockerfile Specs ##
_Dockerfile not included. Should look like this:_

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

## Deploying to Heroku via CLI ##
_Heroku cli installation, and heroku app, need to be created first_
heroku login
heroku container:login
heroku container:push web -a <image_name>
heroku container:release web -a <image_name>
heroku open -a <image_name>