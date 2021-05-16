# Dijkstra Algorithm adaptation to colored graphs

## How to use it
````
$ # Get the code
$ git clone https://github.com/luismontanaresm/colorized-dijkstra.git
$ cd colorized-dijkstra
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$ 
$ # Install modules
$ # Docopt
$ pip install -r requirements.txt
$
$ # Run the script
$ python main.py <path-to-json-file> <source-station-label> <dest-station-label> --route_color=<metro-route-color>
$
$ # Prints the shortest path from source-station to dest-station
````

#### Example of use
````
$ python main.py <path-to-repository-folder>/test_graph.json A F
A->B->C->D->E->F
$ python main.py <path-to-repository-folder>/test_graph.json A F --route_color=RED
A->B->C->H->F
$ python main.py <path-to-repository-folder>/test_graph.json A F --route_color=GREEN
A->B->C->G->I->F
````


### Usage interface
````

from graph_tools import (
    Color,
    ColoredNode,
    ColoredGraph
)
from pathlib import Path


# Instantiate a graph that implements the colored dijkstra algorithm adaptation
metro_santiago = ColoredGraph()

# Instantiate graph node colors
GREEN = Color('GREEN')
RED = Color('RED')

# Instantiate metro stations
baquedano = ColoredNode('Baquedano', None)
parque_bustamante = ColoredNode('Parque Bustamante', RED)
santa_isabel = ColoredNode('Santa Isabel', GREEN)
irarrazabal = ColoredNode('Irarrazabal', None)

# Add a station to the metro network
metro_santiago.add_node(baquedano)

# Or add multiple stations
metro_santiago.add_nodes([
    parque_bustamante,
    santa_isabel,
    irarrazabal
])

# Connect stations
metro_santiago.add_edge(baquedano, parque_bustamante)

# Or connect multiple stations
metro_santiago.add_edges([
    (parque_bustamante, santa_isabel),
    (santa_isabel, irarrazabal)
])

# You can also retrieve a node object from the graph by its name
retrieved_station_baquedano = metro_santiago.get_node_by_label('Baquedano')
assert id(retrieved_station_baquedano) == id(baquedano)

# The graph will handle errors when adding edges for nodes 
# that are not in the graph
nuble = ColoredNode('Ñuble', None)
try:
    metro_santiago.add_edge(irarrazabal, nuble)
except Exception as e:
    print('Handled exception: "'+str(e)+'"')
    # --> Err: node with label "Ñuble" has not been inserted

# Then you are able to add edges
metro_santiago.add_node(nuble)
metro_santiago.add_edge(irarrazabal, nuble)

# finally, loading the graph as a json file will clean all previous 
# nodes and edges
metro_santiago.load_from_json(Path().absolute() / 'test_graph.json')

````

### Running Tests
````
$ python -m unittest tests
$ ..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
$ 
````


## Graph Specification

````
{
    "nodes": [
        {"label": (str), "color": (str | null)},
        ...
    ],
    "edges": [
        [(str), (str)],
        ...
    ]
}
````


#### Example:

The test_graph.json file implements the structure of a simple metro network
````
# test_graph.json 

{
    "nodes": [
        {
            "label": "A",
            "color": null
        },
        {
            "label": "B",
            "color": null
        },
        {
            "label": "C",
            "color": null
        },
        {
            "label": "D",
            "color": null
        },
        {
            "label": "E",
            "color": null
        },
        {
            "label": "F",
            "color": null
        },
        {
            "label": "G",
            "color": "GREEN"
        },
        {
            "label": "H",
            "color": "RED"
        },
        {
            "label": "I",
            "color": "GREEN"
        }
    ],
    "edges": [
        ["A", "B"],
        ["B", "C"],
        ["C", "D"],
        ["D", "E"],
        ["E", "F"],
        ["C", "G"],
        ["G", "H"],
        ["H", "I"],
        ["I", "F"]
    ]
}
````
![red-metro-simple](https://user-images.githubusercontent.com/38935393/118381652-14f45200-b5bb-11eb-8fbd-c03ee95aa04c.png)




