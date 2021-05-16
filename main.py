
"""
Usage:
  main.py <input> <source> <destination> [--route_color=<color name>]
  main.py -h | --help | --version

Example:
    python main.py /path-to-current-folder/test_graph.json A F --route_color=GREEN
    --> A->B->C->G->I->F

    python main.py /path-to-current-folder/test_graph.json A F --route_color=RED
    --> A->B->C->H->F

    python main.py /path-to-current-folder/test_graph.json A F
    --> A->B->C->D->E->F

"""
from docopt import docopt
from pathlib import PurePosixPath, Path
from graph_tools import Color, ColoredGraph


if __name__ == '__main__':
    arguments = docopt(__doc__, version="0.1")
    path_to_json = arguments.get('<input>')
    source = arguments.get('<source>')
    destination = arguments.get('<destination>')
    route_color_name = arguments.get('--route_color', None)
    route_color = Color(name=route_color_name) if route_color_name else None
    colored_graph = ColoredGraph()
    colored_graph.load_from_json(Path(path_to_json))

    source_node = colored_graph.get_node_by_label(source)
    destination_node = colored_graph.get_node_by_label(destination)
    path_from_source_to_dest = colored_graph.get_shortest_path_to_node(
        source=source_node, 
        dest=destination_node, 
        route_color=route_color)
    verbose_path = ('->').join([node.label for node in path_from_source_to_dest ])
    print(verbose_path)
