from abc import ABC, abstractmethod

class VisJsNode:
    def __init__(self, id, color):
        self.id = id
        self.display_name = id
        self.color = color

class SourceNode(VisJsNode):
    def __init__(self, id, color):
        super().__init__(id, color)
        self.set_display_name()

    # build name of the source node
    # for example if id is "java.lang.Integer:valueOf" this function set display_name to "Integer:valueOf"
    def set_display_name(self):
        class_name = self.id.split(":")[0].split(".")[-1]
        method_name = self.id.split(":")[1]
        self.display_name = class_name + ":" + method_name

class SinkNode(VisJsNode):

    def __init__(self, id, color):
        super().__init__(id, color)
        self.set_display_name()

    # build name of the sink node
    # for example if id is "java.lang.Integer:valueOf" this function set display_name to "Integer"
    def set_display_name(self):
        class_name = self.id.split(":")[0].split(".")[-1]
        self.display_name = class_name

    def parse_method_name(self):
        return self.id.split(":")[1]

    def edge_label(self):
        return self.parse_method_name()

    def edge_color(self):
        method_name = self.parse_method_name()
        is_write_op = "save" in method_name or "delete" in method_name
        return "red" if is_write_op else "green"

class NodeSelector(ABC):
    def __init__(self, call_graph):
        self.call_graph = call_graph
        self.nodes = call_graph.nodes()

    def source_nodes(self):
        return self.select_source_nodes(list(self.nodes()))

    @abstractmethod
    def select_source_nodes(self, nodes):
        pass

    def sink_nodes(self):
        return self.select_sink_nodes(list(self.nodes()))

    @abstractmethod
    def select_sink_nodes(self, nodes):
        pass


# This is an example for the demo-customer Spring Project
class ApiDBSelector(NodeSelector):
    def select_source_nodes(self, nodes):
        source_nodes = []
        for node_id in nodes:
            if "com.example.democustomer.controller.CustomerController" in node_id:
                source_nodes.append(SourceNode(node_id, 'orange'))
            elif "com.example.democustomer.controller.StatisticController" in node_id:
                source_nodes.append(SourceNode(node_id, 'blue'))
        return source_nodes

    def select_sink_nodes(self, nodes):
        sink_nodes = []
        for node_id in nodes:
            if "com.example.democustomer.repo" in node_id:
                sink_nodes.append(SinkNode(node_id, '#E0E0E0'))
        return sink_nodes


# Implement your custom NodeSelector below
class MyNodeSelector(NodeSelector):
    def select_source_nodes(self, nodes):
        source_nodes = []
        for node_id in nodes:
            # add nodes to source_nodes list
            pass
        return source_nodes

    def select_sink_nodes(self, nodes):
        sink_nodes = []
        for node_id in nodes:
            # add nodes to sink_nodes list
            pass
        return sink_nodes

