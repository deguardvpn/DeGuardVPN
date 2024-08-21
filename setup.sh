#!/bin/bash
echo '
     _                                  _   _         
    | |                                | | (_)        
  __| |_____  ____ _   _ _____  ____ __| |  _  ___    
 / _  | ___ |/ _  | | | (____ |/ ___) _  | | |/ _ \   
( (_| | ____( (_| | |_| / ___ | |  ( (_| |_| | |_| |  
 \____|_____)\___ |____/\_____|_|   \____(_)_|\___/   
            (_____|                                                                                                                                                                                                                                                                                                                                                                                                                                   
'

echo $'\n'                                                        

# Add Docker's official GPG key:
sudo apt-get -y update
sudu apt-get -y upgrade
sudo apt-get -y install ca-certificates curl gnupg
sudo install -y -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update

sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

echo "Change directory..."
# shellcheck disable=SC2164
cd /opt/


#echo -e "\n"|ssh-keygen -t rsa -N ""
#
#echo $'\n'
#echo ssh-key is done
#echo $'\n'
#cat ~/.ssh/id_rsa.pub
#echo $'\n'
#echo "Input ssh key in github?"
#echo -n "Y/N"
#echo $'\n'
#read VAR1
#
#ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts
#git clone git@github.com:deguardvpn/wireguard_alpine.git
git clone https://github.com/deguardvpn/DeGuardVPN

# shellcheck disable=SC2164
cd DeGuardVPN/
echo $'\n'
docker compose up -d --build
echo $'\n'
echo "DeGuardVPN done"
echo $'\n'
echo "Install 3x-ui"

git clone https://github.com/MHSanaei/3x-ui.git
# shellcheck disable=SC2164
cd 3x-ui
docker compose up -d

