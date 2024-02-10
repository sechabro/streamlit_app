FROM python:3.11-slim-bullseye

WORKDIR /app

COPY ./requirements.txt .
COPY ./server.py .
COPY ./app.py .
COPY ./data_sorter.py .
COPY ./docker_run.sh .
COPY ./key.txt .

RUN chmod +x ./docker_run.sh
RUN pip3 install -r requirements.txt
ENV BCSV=$WORKDIR/data.csv
EXPOSE 8501

ENTRYPOINT [ "sh", "./docker_run.sh" ]
