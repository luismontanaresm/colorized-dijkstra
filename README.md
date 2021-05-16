# colorized-dijkstra



## How to use it
````
$ # Get the code
$ git clone blablalba
$ cd django-dashboard-black
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

````
# sample_graph.json 

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