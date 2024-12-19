# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye
WORKDIR /app

COPY ./ .

#RUN chmod +x ./server.py 
RUN chmod +x ./app.py
#RUN chmod +x ./utils.py
RUN pip3 install -r requirements.txt

#ENV BCSV=/app/data.csv
ENV PORT=8501
ENV HOST=0.0.0.0

CMD streamlit run --server.port ${PORT} --server.address ${HOST} ./app.py