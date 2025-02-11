# syntax=docker/dockerfile:1.2

FROM python:3.11-slim-bullseye

# Install OpenSSH with -y flag
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# Set environment variables
RUN echo "export BCSV=/server/data/data.csv" >> /etc/environment
RUN echo "export RUNC=/server/data/server_check.txt" >> /etc/environment

# Allow password authentication login via SSH
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

WORKDIR /server
COPY ./ .

# Create a user and set password.
RUN useradd -m -s /bin/bash streamlit
RUN echo "streamlit:$(cat ./streamlit.txt | base64 -d)" | chpasswd

# Setting directory permissions for the user
RUN chown -R streamlit:streamlit ./data
RUN chmod +x ./server.py && chmod +x ./utils.py && pip3 install -r requirements.txt

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]