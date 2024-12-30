# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye

# Install SSH
RUN apt-get update && \
    apt-get install -y openssh-client

# Set environment variables
RUN echo "export RUNC=/app/data/server_check.txt" >> /etc/environment

# Streamlit-related
WORKDIR /app

COPY ./app.py .
COPY ./.streamlit ./.streamlit
COPY ./pages ./pages
COPY ./requirements.txt .
COPY ./__init__.py .

RUN chmod +x ./app.py && pip3 install -r requirements.txt

ENV PORT=8501
ENV HOST=0.0.0.0
ENV RUNC=/data/server_check.txt

CMD streamlit run --server.port ${PORT} --server.address ${HOST} ./app.py