sudo sysctl -w net.ipv4.tcp_congestion_control=cubic
sudo sysctl -w net.ipv4.tcp_ecn=1

sudo sysctl -w net.ipv4.ip_forward=1

# add static routing
sudo ip route add 10.0.5.0/24 via 10.0.0.2

sudo ethtool -K eth1 gro off
sudo ethtool -K eth1 lro off
sudo ethtool -K eth1 gso off
sudo ethtool -K eth1 tso off