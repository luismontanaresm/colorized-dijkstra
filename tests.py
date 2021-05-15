from unittest import TestCase as TC
from colored_dijkstra import colored_dijkstra
from pprint import pprint

class ColoredDijkstraTest(TC):
    def test_colored_dijkstra(self):

        colored_nodes = (
            ('A', None),
            ('B', None),
            ('C', None),
            ('D', None),
            ('E', None),
            ('F', None),
            ('G', 'GREEN'),
            ('H', 'RED'),
            ('I', 'GREEN')
        )

        edges = (
            ('A', 'B'),
            ('B', 'C'),
            ('C', 'D'),
            ('D', 'E'),
            ('E', 'F'),
            ('C', 'G'),
            ('G', 'H'),
            ('H', 'I'),
            ('I', 'F')
        )

        source = 'A'

        best_paths = colored_dijkstra(colored_nodes, edges, source, train_color='RED')
        pprint(best_paths)
