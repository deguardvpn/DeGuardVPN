#!/bin/bash
echo "Today is " `date`

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

echo "Make folder /opt/wireguard_alpine/config/..."

mkdir /opt/wireguard_alpine/config/

echo "Change directory..."

cd /opt/wireguard_alpine/config/

echo -e "\n\n\n" | ssh-keygen -t rsa
cat .ssh/id_rsa.pub

echo "Input ssh key in github?"
echo -n "Y/N"
read VAR1


if [[ VAR1 -ge "Y"]]
then
    git clone git@github.com:deguardvpn/wireguard_alpine.git
    docker-compose up -d
fi