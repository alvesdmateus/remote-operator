# Use the official Debian image from the Docker Hub
FROM debian:stable


# Set the environment variable to suppress warnings
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && apt-get install -y \
    apt-utils \
    sudo \
    openssh-server \
    python3 \
    && mkdir /var/run/sshd 
    

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set the root password (for simplicity, you can change this later)
RUN echo 'root:test123' | chpasswd

# Allow root login via SSH
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Avoids error "PAM: Authentication failure"
RUN sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/' /etc/ssh/sshd_config

#Expose ssh port
EXPOSE 22

#ENTRYPOINT service ssh start && bash

# Start SSH service
CMD ["/usr/sbin/sshd", "-D"]
