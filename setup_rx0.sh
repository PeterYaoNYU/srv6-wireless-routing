sudo sysctl -w net.ipv4.ip_forward=1

sudo ip route add 10.0.0.0/24 via 10.0.5.1


# update gcc to version 9
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test  
sudo apt-get update  
# install actually
sudo apt-get install -y gcc-9 g++-9  
# set the new version as the default
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 60 --slave /usr/bin/g++ g++ /usr/bin/g++-9  
sudo update-alternatives --config gcc  



cd /mydata  
wget https://github.com/Kitware/CMake/releases/download/v3.27.0/cmake-3.27.0.tar.gz  
tar -xzvf cmake-3.27.0.tar.gz  
cd cmake-3.27.0  
./bootstrap

make -j 8  
sudo make install

export PATH=/users/PeterYao/cmake-3.27.0/bin:$PATH

sudo apt-get install -y libpcre2-dev 

cd /mydata  
git clone https://gitlab.eurecom.fr/mosaic5g/flexric.git  
cd flexric/  
git checkout rc_slice_xapp

# for oai, first git clone the latest version
cd /mydata  
git clone https://gitlab.eurecom.fr/oai/openairinterface5g.git  
cd openairinterface5g  
git checkout rebased-5g-nvs-rc-rf  
cd cmake_targets  

cp /local/repository/etc/modified_oai_code/rc_ctrl_service_style_2.c /mydata/openairinterface5g/openair2/E2AP/RAN_FUNCTION/O-RAN/ 


cd /mydata/openairinterface5g  
cd cmake_targets  
./build_oai -c -C -I -w SIMU --gNB --nrUE --build-e2 --ninja

cd /mydata  
git clone https://github.com/swig/swig.git  
cd swig  
git checkout release-4.1  
./autogen.sh
./configure --prefix=/usr/
make -j8  
sudo make install

cd /mydata/flexric && mkdir build && cd build && cmake .. && make -j8  
sudo make install

cd /mydata  
git clone https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed.git  
cd /mydata/oai-cn5g-fed  

cp /local/repository/etc/core-slice-conf/docker-compose-basic-nrf.yaml /mydata/oai-cn5g-fed/docker-compose

cp /local/repository/etc/core-slice-conf/basic* /mydata/oai-cn5g-fed/docker-compose/conf

cp /local/repository/etc/new_core_network.py /mydata/oai-cn5g-fed/docker-compose  

sudo ethtool -K eth1 gro off
sudo ethtool -K eth1 lro off
sudo ethtool -K eth1 gso off
sudo ethtool -K eth1 tso off