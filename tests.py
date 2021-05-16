from unittest import TestCase
from pathlib import Path
from graph_tools import (
    Color,
    ColoredNode,
    ColoredGraph
)

class ColoredGraphTest(TestCase):
    RED = Color('RED')
    GREEN = Color('GREEN')
    
    def test_colored_graph_shortest_path(self):
        A = ColoredNode('A', None)
        B = ColoredNode('B', None)
        C = ColoredNode('C', None)
        D = ColoredNode('D', None)
        E = ColoredNode('E', None)
        F = ColoredNode('F', None)
        G = ColoredNode('G', self.GREEN)
        H = ColoredNode('H', self.RED)
        I = ColoredNode('I', self.GREEN)

        a_colored_graph = ColoredGraph()

        # add nodes
        a_colored_graph.add_nodes([
            A, B, C, 
            D, E, F, 
            G ,H, I
        ])
        # add edges
        a_colored_graph.add_edges([
            (A, B), (B, C), (C, D),
            (D, E), (E, F), (C, G),
            (G, H), (H, I), (I, F)
            ])

        shortest_path_from_A_to_F_with_no_route_color = a_colored_graph.get_shortest_path_to_node(
            source=A, dest=F)
        self.assertEqual(
            shortest_path_from_A_to_F_with_no_route_color, 
            [A, B, C, D, E, F])

        shortest_path_from_A_to_F_with_red_route = a_colored_graph.get_shortest_path_to_node(
            source=A, dest=F, route_color=self.RED)
        self.assertEqual(
            shortest_path_from_A_to_F_with_red_route,
            [A, B, C, H, F])
        
        shortest_path_from_A_to_F_with_green_route = a_colored_graph.get_shortest_path_to_node(
            source=A, dest=F, route_color=self.GREEN
        )
        self.assertIn(
            shortest_path_from_A_to_F_with_green_route,
            [
                [A, B, C, D, E, F],
                [A, B, C, G, I, F]
            ])
    
    def test_load_graph_from_json(self):
        colored_graph = ColoredGraph()
        json_filename = 'test_graph.json'
        path_to_json = Path().absolute() / json_filename
        colored_graph.load_from_json(path_to_json)
        A = colored_graph.get_node_by_label('A')
        B = colored_graph.get_node_by_label('B')
        C = colored_graph.get_node_by_label('C')
        D = colored_graph.get_node_by_label('D')
        E = colored_graph.get_node_by_label('E')
        F = colored_graph.get_node_by_label('F')
        G = colored_graph.get_node_by_label('G')
        H = colored_graph.get_node_by_label('H')
        I = colored_graph.get_node_by_label('I')
        
        shortest_path_from_A_to_F_with_no_route_color = colored_graph.get_shortest_path_to_node(
            source=A, dest=F)
        self.assertEqual(
            shortest_path_from_A_to_F_with_no_route_color, 
            [A, B, C, D, E, F])
        
        shortest_path_from_A_to_F_with_red_route = colored_graph.get_shortest_path_to_node(
            source=A, dest=F, route_color=self.RED)
        self.assertEqual(
            shortest_path_from_A_to_F_with_red_route,
            [A, B, C, H, F])

        shortest_path_from_A_to_F_with_green_route = colored_graph.get_shortest_path_to_node(
            source=A, dest=F, route_color=self.GREEN)
        self.assertIn(
            shortest_path_from_A_to_F_with_green_route,
            [
                [A, B, C, D, E, F],
                [A, B, C, G, I, F]
            ])
