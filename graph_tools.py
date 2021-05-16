from pathlib import Path
from typing import List, Tuple, Optional
import json

class Color:
    def __init__(self, name) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return self.name

    def __eq__(self, o: object) -> bool:
        return self.name == o.name
    
    def __ne__(self, o: object) -> bool:
        return self.name != o.name

class ColoredNode:
    def __init__(self, label: str, color: Color) -> None:
        self.label = label
        self.color = color
    
    def __repr__(self) -> str:
        return f'ColoredNode(label="{self.label}" color="{self.color})"'

class ColoredGraph:
    def __init__(
            self, 
            nodes: List[ColoredNode]=None, 
            edges: List[Tuple[ColoredNode]]=None
            ):
        self.nodes = nodes if nodes else []
        self.edges = edges if edges else []

    def add_node(self, node: ColoredNode):
        '''
        Inserts a ColoredNode instance to the graph nodes.
        '''
        self.nodes.append(node)
        return self
    
    def add_nodes(self, nodes: List[ColoredNode]):
        '''
        Inserts a list of ColoredNode instances to the graph nodes.
        '''
        for node in nodes:
            self.add_node(node)
        return self
    
    def get_node_by_label(self, label: str) -> ColoredNode:
        '''
        Return a ColoredNode object in the graph nodes whose name matches with
        the label argument.
        '''
        for node in self.nodes:
            if node.label == label: return node

    def add_edge(self, n1: ColoredNode, n2: ColoredNode ):
        '''
        Receives two ColoredNode instances and adds a connection in the graph 
        between both nodes. Both of them must be already inserted.
        '''
        if n1 not in self.nodes:
            raise Exception(f'node with label "{n1.label} has not been inserted"')
        if n2 not in self.nodes:
            raise Exception(f'node with label "{n2.label}" has not been inserted')
        edge = (n1, n2)
        self.edges.append(edge)
        return self
    
    def add_edges(self, edges: List[Tuple[ColoredNode]]):
        '''
        Receives a list of paired ColoredNode instances and adds a connection 
        in the graph  between both nodes. All of them must be already inserted.
        '''
        for (n1, n2) in edges:
            self.add_edge(n1, n2)  # --> validates size of edges added
        return self
    
    def load_from_json(self, path: Path):
        '''
        Receives a Path to a json file and will reshape the structure of 
        the graph to the parameters received from the file.

        Json file must follow the following specification:
        {
            "nodes": [
                {"label": (str), "color": (str | null)},
                {"label": (str), "color": (str | null)},
                ...
            ],
            "edges": [
                [(str), (str)],
                [(str), (str)],
                [(str), (str)],
                ...
            ]
        }
        '''
        self.nodes = []
        self.edges = []
        with open(path, 'r') as fp:
            data = json.load(fp)
            nodelist = data['nodes']
            edgelist = data['edges']
            nodes_map = {}
            for obj in nodelist:
                color = Color( obj['color'] ) if obj['color'] else None
                node = ColoredNode(obj['label'], color)
                nodes_map.update({obj['label']: node})
            self.add_nodes([ colored_node for _, colored_node in nodes_map.items() ])
            self.add_edges([ (nodes_map[n1], nodes_map[n2]) for (n1,n2) in edgelist ])
            return self
    
    def get_shortest_paths(self, source: ColoredNode, route_color: Optional[Color]=None):
        '''
        Receives a reference to a 'source' node in the graph and a optional 
        Color object.
        
        Will construct the shortest path to each node from source in the graph
        using an adaptation to the dijkstra algorithm.

        If route_color is a Color object, the algorigthm will 
        consider that the cost of going from a node with color==route_color
        to a node with color!=route_color is zero.

        Returns a dictionary where each node is a key and their values are
        lists of nodes that will take you from the source node to the key node
        standing on the least number of nodes.
        '''
        inf = float('inf')
        best_dist = {node: (inf if node!=source else 0) for node in self.nodes }
        best_prev = {node: None for node in self.nodes}
        unprocessed_nodes = set({node for node in self.nodes})

        while len(unprocessed_nodes) > 0:
            
            # Step 1:
            # Find current node with the least distance to the source node.
            least_distance_node = None
            min_distance = inf
            for unprocessed_node in list(unprocessed_nodes):
                if best_dist[unprocessed_node] < min_distance:
                    min_distance = best_dist[unprocessed_node]
                    least_distance_node = unprocessed_node
            
            # Step 2:
            # Set the nearest unprocessed node as processed so it 
            # will not be processed twice.
            unprocessed_nodes.remove(least_distance_node)

            # Step 3:
            # Find the neighbors of the current node with the least distance to
            # the source node. This way, if <this path> is shorter than a 
            # previous one that reaches the <unprocessed_node> from the 
            # source node, it will set the <this path distance> to the node.
            neighbors: List[ColoredNode] = list()
            for (v, w) in self.edges:
                if least_distance_node in (v, w) and least_distance_node == v:
                    # if edge == (nearest_node_label, w) ==> w is neighbor
                    neighbors.append(w)

                elif least_distance_node in (v, w) and least_distance_node == w:
                    # if edge == (v, nearest_node_label) ==> v is neighbor
                    neighbors.append(v)

            # Step 4:
            # Set the <this path distance> to the neighbor nodes where 
            # this path is the shortest one up to now.
            for neighbor in neighbors:
                
                # Distance between two nodes will be zero if both route_color
                # and the neighbor color are defined and they are not the same.
                # Otherwise, distance to neighbor will be one.
                neighbor_color = neighbor.color
                if  route_color is not None \
                    and neighbor_color is not None \
                    and route_color != neighbor_color:
                    nodes_distance = 0
                else:
                    nodes_distance = 1
                
                alt_distance = best_dist[least_distance_node] + nodes_distance
                if alt_distance  < best_dist[neighbor]:
                    best_dist[neighbor] = alt_distance
                    best_prev[neighbor] = least_distance_node
        
        # Step 5:
        # Re-construct the best path to every node from the source node 
        # in the colored graph.
        best_paths = dict()
        for node in self.nodes:
            prev: ColoredNode = best_prev[node]
            path_construction: List[ColoredNode] = [node]
            while prev:
                if route_color is not None:
                    prev_color = prev.color
                    if prev_color is not None and route_color != prev_color:
                        pass
                    else:
                        path_construction = [prev] + path_construction
                else:
                    path_construction = [prev] + path_construction
                prev = best_prev[prev]
            best_paths[node] = path_construction
        return best_paths

    def get_shortest_path_to_node(
            self, 
            source: ColoredNode, 
            dest: ColoredNode, 
            route_color: Optional[Color]=None
            ):
        '''
        Receives a reference to a 'source' node in the graph, a destination 
        node in the graph and an optional Color object.

        Returns a lists of nodes that will take you from the source node to 
        the destination node standing on the least number of nodes.
        '''
        shortest_paths = self.get_shortest_paths(source, route_color)
        shortest_path_to_node = shortest_paths.get(dest)
        return shortest_path_to_node
