from pyvis.network import Network
import networkx as nx
import sys
import os

if len(sys.argv) != 2:
    print('Error: Missing file')
    print('Usage: call-graph-plotter.py <call-graph file path>')
    sys.exit()

# Get file path from argument
call_graph_file_path = sys.argv[1]

# Open and read input file
print('Reading file:', call_graph_file_path)
call_graph_file = open(call_graph_file_path, 'r')
lines = call_graph_file.readlines()

# Get filename
call_graph_file_name = os.path.basename(os.path.splitext(call_graph_file_path)[0])

# Create Networkx Directed Graph
G = nx.DiGraph()
for line in lines:
    if line.startswith("M:"):
        tokens = line.strip().split(":")
        middle_tokens = tokens[2].split(" ")
        source = tokens[1] + ":" + middle_tokens[0].split("(")[0]
        target = middle_tokens[1].split(")")[1] + ":" + tokens[3].split("(")[0]

########

        # If it is a Controller (API) tag it
        if ".controller" in source:
            G.add_node(source, type="CONTROLLER")
        else:
            G.add_node(source)

        # If it is a Repo (Interface to the database)
        if ".repo" in target:
            G.add_node(target, type="REPO")
        else:
            G.add_node(target)
#########
        G.add_edge(source, target)


# Create a list of all the source nodes (Controller/API) and all the sink nodes (Database)
source_nodes = []
sink_nodes = []
for node, type in list(G.nodes(data='type')):
    if type:
        if "CONTROLLER" in type:
            source_nodes.append(node)
        elif "REPO" in type and G.out_degree(node) == 0:
            sink_nodes.append(node)

# Set a color for a package or class name
def get_color_for(class_name):
    if "Customer" in class_name:
        color = "orange"
    elif "Statistic" in class_name:
        color = "blue"
    else:
        # Default red
        color = "red"
    return color


def is_write_op(method_name):
    return "save" in method_db_name or "delete" in method_db_name


# Create Visjs graph
net = Network(height='550px', width='700px', directed=True)

# build name of the source node
def get_source_node_name(source):
    source_class_name = source.split(":")[0].split(".")[-1]
    source_method_name = source.split(":")[1].split("(")[0]
    return source_class_name + ":" + source_method_name

# build name of the sink node
def get_sink_node_name(sink):
    return sink.split(":")[0].split(".")[-1]

for source in source_nodes:
    for sink in sink_nodes:
        for path in nx.all_simple_paths(G, source=source, target=sink):
            # add source node
            source_node_name = get_source_node_name(source)
            print("Source node name: ", source_node_name)
            net.add_node(source_node_name, title=source_node_name, color=get_color_for(source))

            # build name of the sink node
            sink_node_name = get_sink_node_name(sink)
            method_db_name = sink.split(":")[1]
            # Add sink node with grey color
            net.add_node(sink_node_name, title=sink_node_name, color="#E0E0E0")
            print("Sink node name: ", sink_node_name)

            # Add the edge: green is a read operation, red is a write operation
            if is_write_op(method_db_name):
                net.add_edge(source_node_name, sink_node_name, color="red", title=method_db_name)
            else:
                net.add_edge(source_node_name, sink_node_name, color="green", title=method_db_name)

# Visualization
net.show_buttons()
output_file = 'output/'+call_graph_file_name+'.html'
net.write_html(output_file)
# Or if you want to open the file immediately uncomment the following line
# net.show(output_file)