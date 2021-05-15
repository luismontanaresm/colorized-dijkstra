from typing import List

def colored_dijkstra(nodes: List, edges: List, source: str, train_color=None):
    '''
    @params:
        nodes: a List of tuples with label and color name
        edges: a List of tuples with labels of two nodes
        root: Label of a node
        train_color
    
    @returns:
        a List where, for each node, the shortest path from the root node
    '''
    inf = float('inf')
    
    colors = {label: color for label, color in nodes}
    best_dist = {label: (inf if label!=source else 0) for label, _ in nodes}
    best_prev = {label: None for label, _ in nodes}
    unprocessed_nodes = set({label for label, _ in nodes })

    #return best_dist, best_prev

    while len(unprocessed_nodes) > 0:
        # current unprocessed node with the least distance to the source node
        
        nearest_node_label = min(best_dist, key=best_dist.get)

        min_distance = inf
        for unprocessed_node_label in list(unprocessed_nodes):
            if best_dist[unprocessed_node_label] < min_distance:
                min_distance = best_dist[unprocessed_node_label]
                nearest_node_label = unprocessed_node_label
        
        # remove the selected node from the unprocessed_nodes set
        unprocessed_nodes.remove(nearest_node_label)

        # find the neighbors of the current node with the least dist. to source
        neighbors = list()
        for (v, w) in edges:
            if nearest_node_label in (v, w) and nearest_node_label == v:
                # if edge == (nearest_node_label, w) ==> w is neighbor
                neighbors.append(w)
            elif nearest_node_label in (v, w) and nearest_node_label == w:
                # if edge == (v, nearest_node_label) ==> v is neighbor
                neighbors.append(v)
        
        for neighbor_label in neighbors:
            # Distance to neighbor node will be zero if they both have color
            # and its not the same. Otherwise, distance will be one.

            nearest_node_color = colors[nearest_node_label]
            neighbor_color = colors[neighbor_label]
            
            
            if  train_color is not None \
                and neighbor_color is not None \
                and train_color != neighbor_color:
                nodes_distance = 0
            else:
                nodes_distance = 1
                        
            alt_distance = best_dist[nearest_node_label] + nodes_distance
            if alt_distance  < best_dist[neighbor_label]:
                best_dist[neighbor_label] = alt_distance
                best_prev[neighbor_label] = nearest_node_label
    
    best_path = {}
    for node_label, _ in nodes:
        prev = best_prev[node_label]
        path_construction = [node_label]
        while prev:
            if train_color:
                prev_color = colors[prev]
                if prev_color is not None and train_color != prev_color:
                    pass
                else:
                    path_construction = [prev] + path_construction
            else:
                path_construction = [prev] + path_construction
            prev = best_prev[prev]
        best_path[node_label] = path_construction
    return best_path
