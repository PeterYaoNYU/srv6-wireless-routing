sudo apt-get update
sudo apt -y install git gcc make bison flex libdb-dev libelf-dev pkg-config libbpf-dev libmnl-dev libcap-dev libatm1-dev selinux-utils libselinux1-dev
sudo git clone https://github.com/L4STeam/iproute2.git
cd iproute2
sudo chmod +x configure
sudo ./configure
sudo make
sudo make install

sudo modprobe sch_dualpi2

sudo sysctl -w net.ipv4.ip_forward=1

sudo ip route add 10.0.0.0/24 via 10.0.2.2

sudo ethtool -K eth1 gro off
sudo ethtool -K eth1 lro off
sudo ethtool -K eth1 gso off
sudo ethtool -K eth1 tso off

sudo ethtool -K eth2 gro off
sudo ethtool -K eth2 lro off
sudo ethtool -K eth2 gso off
sudo ethtool -K eth2 tso off