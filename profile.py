"""
## Static routing

In this experiment, you will observe how routing principles apply when packets are forwarded by a router from one network segment to the next.

It should take about 60-120 minutes to run this experiment.
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Optional physical type for all nodes.
pc.defineParameter("phystype",  "Optional hardware type",
                   portal.ParameterType.STRING, "d430",
                   longDescription="Specify hardware type (d430 or d820)")

# Retrieve the values the user specifies during instantiation.
params = pc.bindParameters()
pc.verifyParameters()

# Function to add services to install packages
def add_install_services(node):
    node.addService(pg.Execute('/bin/sh', 'sudo apt-get update'))
    node.addService(pg.Execute('/bin/sh', 'sudo apt-get install -y iperf3 net-tools moreutils'))

# Node definitions
nodes = {
    "tx0": request.RawPC( "tx0" ),
    "router0": request.RawPC("router0"),
    "router1": request.RawPC("router1"),
    "rx0": request.RawPC( "rx0" )
}

# Set disk images and add install services
for node in nodes.values():
    node.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
    add_install_services(node)
    node.cores = 4
    node.ram = 32

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