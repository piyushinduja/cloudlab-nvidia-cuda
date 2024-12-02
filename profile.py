import geni.portal as portal
import geni.rspec.pg as pg

# Create a portal context and define parameters
pc = portal.Context()
pc.defineParameter("nodeCount", "Number of Nodes", portal.ParameterType.INTEGER, 1)
pc.defineParameter("phystype",  "Pick a GPU node type",
                   portal.ParameterType.NODETYPE, "",
                   longDescription="Select a GPU node type. Available hardware can be checked under the Docs dropdown in the upper-right corner.")
params = pc.bindParameters()

request = pc.makeRequestRSpec()

lan = request.LAN("lan")

for i in range(params.nodeCount):
    node = request.RawPC("node" + str(i))
    node.disk_image = "urn:publicid:IDN+wisc.cloudlab.us+image+distribml-PG0:python-setup.node0-nvidia-cuda"

    if params.phystype:
      node.hardware_type = params.phystype

    iface = node.addInterface("eth1")
    lan.addInterface(iface)

    node.addService(pg.Execute(shell='sh', command="""\
    echo "MASTER_ADDR=10.10.1.1" | sudo tee -a /etc/environment;
    echo "MASTER_PORT=29500" | sudo tee -a /etc/environment;
    echo "WORLD_SIZE={}" | sudo tee -a /etc/environment;
    echo "RANK={}" | sudo tee -a /etc/environment;
    """.format(params.nodeCount, i)))

pc.printRequestRSpec(request)
