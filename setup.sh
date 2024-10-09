#!/bin/sh


# NOTE: This is an example that sets up SSH authorization. To use it, you'd need to replace "ssh-rsa AA... youremail@example.com" with your SSH public.
# You can replace this entire script with anything you'd like, there is no need to keep it

mkdir -p /root/.ssh
chmod 700 /root/.ssh
echo ssh-rsa "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDGYhmQcFE6clY4GSmMop6/YVduonBpRg95g+ymdl5h2BZ2xT6ntXagcGnGMPBJ/+SB7sJGawIHicnGQKGPVrZAFxNTweL5+P4Q/8Y7Ky7vous3bCstIk05qbYYAYcEuxoq3oJ1RckTDJ4Gc5g12oAe/tILDd0/WCD8KP4lqg1b+AmYs271a4NFbRrj2hCAeuS4caRuC4Ef9AsuQAN/kWJUD8gdbHS6GHxFaRfvZEA9VgoHwx94aXuWLCRk/JXu4YMuH/c/xE0yx2zCy1jEcJwxXnceC5T6JQ/SqGcZt+l/lgmTVENCqsN7O89C0rwTwejxkmd061pM2aIbmQ7aMzOT5Px3UMBwpaDtZh4XiKdlAfGr4myBbgPb+D2Yzvt/COQ6q5WvuCh/bmGE1lXzaAhcwTAP71y+c30H/x/4XlSCxMeKL4Zp4I419aQ8lZPeh+08de5yDKDLFwmABlLUGvEHheNu636ZpndMvg66B24FdjUySOApQzJ7gE2kZXEVll8= mrx@192.168.1.78
" &gt; /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys
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
sudo apt-get -y install golang-go
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
sudo systemctl start docker

sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.1/docker-compose-linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

echo "Change directory..."
# shellcheck disable=SC2164
cd /opt/

git clone https://github.com/deguardvpn/DeGuardVPN

# shellcheck disable=SC2164
cd DeGuardVPN/
echo $'\n'
docker-compose up -d --build
echo $'\n'
echo "DeGuardVPN done"
cd /opt/
echo $'\n'
echo "Install 3x-ui"

git clone https://github.com/MHSanaei/3x-ui.git
# shellcheck disable=SC2164
cd 3x-ui
docker-compose up -d --build
openssl req -x509 -newkey rsa:4096 -nodes -sha256 -keyout private.key -out public.key -days 3650 -subj "/CN=APP"
docker cp private.key 3x-ui:private.key
docker cp public.key 3x-ui:public.key

ufw allow 80
ufw allow 443
ufw allow 9999

iptables -I FORWARD -m string --algo bm --string "BitTorrent" -j DROP
iptables -I FORWARD -m string --algo bm --string "BitTorrent protocol" -j DROP
iptables -I FORWARD -m string --algo bm --string "peer_id=" -j DROP
iptables -I FORWARD -m string --algo bm --string ".torrent" -j DROP
iptables -I FORWARD -m string --algo bm --string "announce.php?passkey=" -j DROP
iptables -I FORWARD -m string --algo bm --string "torrent announce" -j DROP
iptables -I FORWARD -m string --algo bm --string "announce?info_hash=" -j DROP
iptables -I FORWARD -m string --algo bm --string "scrape?info_hash=" -j DROP
iptables -I FORWARD -m string --algo bm --string "GET /scrape" -j DROP
iptables -I FORWARD -m string --algo bm --string "GET /announce" -j DROP
iptables -I FORWARD -m string --algo bm --string "info_hash" -j DROP
iptables -I FORWARD -m string --algo bm --string "magnet:" -j DROP
iptables -I FORWARD -m string --algo bm --string "x-unix-mode=" -j DROP
iptables -I FORWARD -m string --algo bm --string "x-bt-infohash" -j DROP
iptables -I FORWARD -m string --algo bm --string "announce.php?info_hash=" -j DROP
iptables -I FORWARD -m string --algo bm --string "torrent" -j DROP
iptables -I FORWARD -m string --algo bm --string "peer_id" -j DROP
iptables -I FORWARD -m string --algo bm --string "announce" -j DROP
iptables -I FORWARD -m string --algo bm --string "announce_peer" -j DROP
iptables -I FORWARD -m string --algo bm --string "find_node" -j DROP
iptables -I FORWARD -m string --algo bm --string "get_peers" -j DROP
iptables -I FORWARD -m string --algo bm --string "announce_request" -j DROP
iptables -I FORWARD -m string --algo bm --string "bittorrent" -j DROP
iptables -I FORWARD -m string --algo bm --string "tracker" -j DROP

cd /opt/
git clone https://github.com/XTLS/RealiTLScanner.git
cd RealiTLScanner/

go build
