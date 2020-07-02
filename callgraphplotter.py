from pyvis.network import Network
import networkx as nx
import sys
import os
import nodeselectors

if len(sys.argv) != 3:
    print('Error: Missing file')
    print('Usage: callgraphplotter.py <call-graph file path> <node selector class name>')
    sys.exit()

# Get file path from input
call_graph_file_path = sys.argv[1]

# Get node selector class name from input
ns_class_name = sys.argv[2]

# Open and read input file
print('Reading file:', call_graph_file_path)
call_graph_file = open(call_graph_file_path, 'r')
# If the call graph file uses utf-16 then use the following
#call_graph_file = open(call_graph_file_path, 'r', encoding='utf-16')
lines = call_graph_file.readlines()

# Get call graph filename
call_graph_file_name = os.path.basename(os.path.splitext(call_graph_file_path)[0])

def extract_nx_source_name(line):
    tokens = line.strip().split(":")
    class1 = tokens[1]
    middle_tokens = tokens[2].split(" ")
    method1 = middle_tokens[0].split("(")[0]
    return class1 + ":" + method1

def extract_nx_target_name(line):
    tokens = line.strip().split(":")
    middle_tokens = tokens[2].split(" ")
    class2 = middle_tokens[1].split(")")[1]
    method2 = tokens[3].split("(")[0]
    return class2 + ":" + method2

# Create Networkx Directed Graph
G = nx.DiGraph()
for line in lines:
    # Consider only the method calls
    if line.startswith("M:"):
        # Add source node
        source = extract_nx_source_name(line)
        G.add_node(source)
        # Add target node
        target = extract_nx_target_name(line)
        G.add_node(target)
        # Add edge
        G.add_edge(source, target)


# Instantiate the node selector
klass = getattr(nodeselectors, ns_class_name)
node_selector = klass(G)

# Select the source and sink nodes
source_nodes = node_selector.source_nodes()
sink_nodes = node_selector.sink_nodes()

# Create a new graph (Visjs) with only the nodes that we selected before
# The selected nodes are in the lists source_nodes and sink_nodes
net = Network(height='550px', width='700px', directed=True)

# One source node can point to many sink nodes
for source in source_nodes:
    for sink in sink_nodes:
        for path in nx.all_simple_paths(G, source=source.id, target=sink.id):
            # add source node
            #print("Visjs Source node: ", source_node_name)
            net.add_node(source.display_name, title=source.display_name, color=source.color)

            # Add sink node with grey color
            net.add_node(sink.display_name, title=sink.display_name, color=sink.color)
            #print("Visjs Sink node: ", sink_node_name)

            # Add the edge: green is a read operation, red is a write operation
            net.add_edge(source.display_name, sink.display_name, color=sink.edge_color(), title=sink.edge_label())

# Visualization
net.show_buttons()
output_file = 'output/'+call_graph_file_name+'.html'
net.write_html(output_file)
# If you want to open the file immediately use the following line instead
# net.show(output_file)
print('File generated:',output_file)