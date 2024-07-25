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

# tx0
node_tx0 = request.XenVM("tx0")
node_tx0.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
node_tx0.cores = 4
node_tx0.ram = 32
node_tx0.addService(pg.Execute('/bin/bash', 'sudo apt-get update'))
node_tx0.addService(pg.Execute('/bin/bash', 'sudo apt-get install -y iperf3 net-tools moreutils'))

#router
node_router = request.XenVM("tx0")
node_router.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
node_router.cores = 4
node_router.ram = 32
node_router.addService(pg.Execute('/bin/bash', 'sudo apt-get update'))
node_router.addService(pg.Execute('/bin/bash', 'sudo apt-get install -y iperf3 net-tools moreutils'))

#delay
node_delay = request.XenVM("tx0")
node_delay.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD'
node_delay.cores = 4
node_delay.ram = 32
node_delay.addService(pg.Execute('/bin/bash', 'sudo apt-get update'))
node_delay.addService(pg.Execute('/bin/bash', 'sudo apt-get install -y iperf3 net-tools moreutils'))

# Network configuration
net_conf = [
    {"name": "net-tx", "subnet": "10.0.0.0/24", "nodes": [{"name": "tx0", "addr": "10.0.0.100"}, {"name": "delay", "addr": "10.0.0.2"}]},
    {"name": "net-delay-router", "subnet": "10.0.2.0/24", "nodes": [{"name": "delay", "addr": "10.0.2.2"}, {"name": "router", "addr": "10.0.2.1"}]},
    {"name": "net-rx", "subnet": "10.0.5.0/24", "nodes": [{"name": "router", "addr": "10.0.5.1"}, {"name": "rx0", "addr": "10.0.5.100"}]}
]

# Create interfaces and links
for net in net_conf:
    link = request.Link(net["name"])
    link.routable = True
    for node_info in net["nodes"]:
        iface = nodes[node_info["name"]].addInterface(f'{net["name"]}-{node_info["addr"]}')
        iface.addAddress(pg.IPv4Address(node_info["addr"], net["subnet"]))
        iface.bandwidth = 1000
        link.addInterface(iface)


# Print the generated rspec
pc.printRequestRSpec(request)