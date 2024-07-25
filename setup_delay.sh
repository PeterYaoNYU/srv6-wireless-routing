sudo sysctl -w net.ipv4.ip_forward=1

sudo ip route add 10.0.5.0/24 via 10.0.2.1

sudo ethtool -K eth1 gro off
sudo ethtool -K eth1 lro off
sudo ethtool -K eth1 gso off
sudo ethtool -K eth1 tso off

sudo ethtool -K eth2 gro off
sudo ethtool -K eth2 lro off
sudo ethtool -K eth2 gso off
sudo ethtool -K eth2 tso off