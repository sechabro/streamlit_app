# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye

# Install SSH
RUN apt-get update && \
    apt-get install -y openssh-client

# Streamlit-related
WORKDIR /app

COPY ./app.py .
COPY ./.streamlit ./.streamlit
COPY ./command.py .
COPY ./data_sorter.py .
COPY ./pages ./pages
COPY ./requirements.txt .
COPY ./__init__.py .

RUN chmod +x ./app.py && chmod +x ./data_sorter.py && chmod +x ./command.py && pip3 install -r requirements.txt

# Set environment variables
ENV BCSV=/data/data.csv
ENV RUNC=/data/server_check.txt
ENV PORT=8501
ENV HOST=0.0.0.0

CMD streamlit run --server.port ${PORT} --server.address ${HOST} ./app.py