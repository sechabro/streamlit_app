# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye


# Install OpenSSH with -y flag
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# Create a user (optional) and set its password. Secure this in production environments
RUN useradd -m -s /bin/bash streamlit
RUN echo "streamlit:streamlit" | chpasswd 

# Set environment variables
RUN echo "export BCSV=/server/data/data.csv" >> /etc/environment
RUN echo "export RUNC=/server/data/server_check.txt" >> /etc/environment

# Allow password authentication login via SSH
#RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

WORKDIR /server
COPY ./ .

# Setting permissions for the user
RUN chown -R streamlit:streamlit ./data
RUN chmod +x ./server.py && chmod +x ./utils.py && pip3 install -r requirements.txt


# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]