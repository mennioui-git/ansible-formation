# Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Mise à jour + installation de SSH + sudo
RUN apt update && apt install -y openssh-server sudo python3

# Configuration de SSH
RUN mkdir /var/run/sshd

# Création de l'utilisateur "ansible"
RUN useradd -m ansible && \
    echo "ansible:ansible" | chpasswd && \
    echo "ansible ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Autoriser login par mot de passe
RUN sed -i 's/^#\?PasswordAuthentication .*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/^#\?PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config

# Expose port SSH
EXPOSE 22 80

# Lancement du service SSH
CMD ["/usr/sbin/sshd", "-D"]
