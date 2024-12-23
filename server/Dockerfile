# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye


# Install OpenSSH with -y flag
RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd

# Create a user (optional)
#RUN useradd -m -s /bin/bash sean
#RUN passwd -d sean # Set empty passwork

# Set the root password (important to change this in production)
RUN echo "root:streamlit" | chpasswd 

# Set root-accessible environment variable
RUN echo "export BCSV=/server/data/data.csv" >> /root/.bashrc

# Allow root login via SSH
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Expose the SSH port
EXPOSE 22

# SSH unrelated bit
WORKDIR /server
COPY ./ .
RUN chmod +x ./server.py && chmod +x ./data_sorter.py && chmod +x ./utils.py && pip3 install -r requirements.txt

# Start SSH server
CMD ["/usr/sbin/sshd", "-D"]