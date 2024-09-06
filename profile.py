"""
## e2e low latency test with static routing and vm
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

request = pc.makeRequestRSpec()

# Function to add services to install packages
def add_install_services(node):
    node.addService(pg.Execute('/bin/sh', 'sudo apt-get update'))
    node.addService(pg.Execute('/bin/sh', 'sudo apt-get install -y iperf3 net-tools moreutils'))


# Function to configure the rx0 node at startup, since the configuration each time is relly getting more and more annoyting
# and the link state of the stupid idiotic powder testbed changes after a few hours. 
def add_install_services_rx0(node):
    node.addService(pg.Execute('/bin/bash', '/local/repository/setup_rx0.sh'))

# Node definitions
nodes = {
    "tx0": request.XenVM( "tx0" ),
    "router0": request.XenVM("router0"),
    "router1": request.XenVM("router1"),
}

# Set disk images and add install services
for node in nodes.values():
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
    add_install_services(node)


rx0 = request.XenVM("rx0")
rx0.disk_image = "urn:publicid:IDN+emulab.net+image+mww2023:oai-cn5g-rfsim"
bs = rx0.Blockstore("bs", "/mydata")
bs.size = "50GB"
add_install_services_rx0(rx0)
rx0.startVNC()

nodes["rx0"] = rx0

# Network configuration
net_conf = [
    {"name": "net-tx", "subnet": "255.255.255.0", "nodes": [{"name": "tx0", "addr": "10.0.0.100"}, {"name": "router0", "addr": "10.0.0.2"}]},
    {"name": "net-delay-router", "subnet": "255.255.255.0", "nodes": [{"name": "router0", "addr": "10.0.2.2"}, {"name": "router1", "addr": "10.0.2.1"}]},
    {"name": "net-rx", "subnet": "255.255.255.0", "nodes": [{"name": "router1", "addr": "10.0.5.1"}, {"name": "rx0", "addr": "10.0.5.100"}]}
]

# Create interfaces and links
for net in net_conf:
    link = request.Link(net["name"])
    link.routable = True
    for node_info in net["nodes"]:
        iface = nodes[node_info["name"]].addInterface('{0}-{1}'.format(net["name"], node_info["addr"]))
        iface.addAddress(pg.IPv4Address(node_info["addr"], net["subnet"]))
        iface.bandwidth = 1000000
        link.addInterface(iface)


# Print the generated rspec
pc.printRequestRSpec(request)