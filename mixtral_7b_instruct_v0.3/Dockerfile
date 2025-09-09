FROM nvidia/cuda:12.8.0-devel-ubuntu22.04

# Install python and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-dev \
        curl

# Install SSH server and other necessary packages
RUN apt-get install -y openssh-server && \
    apt-get clean

# Set up SSH
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

EXPOSE 22

WORKDIR /src

RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

# Make the entrypoint script executable
RUN chmod +x /src/scripts/entrypoint.sh

# Clean up any existing Jupyter runtime files
RUN rm -rf /root/.local/share/jupyter/runtime/*

EXPOSE 8888
EXPOSE 7860

ENTRYPOINT ["/src/scripts/entrypoint.sh"]