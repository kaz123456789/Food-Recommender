"""
CSC111 Project 2: Food Recommender

Module Description
==================
This module contains the Tree class and various methods and functions.

===============================

his file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from __future__ import annotations
import csv
from typing import Any

import networkx as nx


class _Vertex:
    """A vertex in a restaurant graph, used to represent a restaurant.
    Each vertex item is either a restaurant name..
    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: ''.
        - neighbours: The vertices that are adjacent to this vertex.
    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    name: Any
    kind: str
    price: int
    latitude: float
    longitude: float
    review_rate: float
    neighbours: set[_Vertex]

    def __init__(self, category: str, address: str, name: str, price_range: str, latitude: float, longitude: float,
                 review_rate: float) -> None:
        """Initialize a new vertex with the given item and kind.
        This vertex is initialized with no neighbours.
        """
        self.category = category
        self.address = address
        self.name = name
        self.price_range = price_range
        self.latitude = latitude
        self.longitude = longitude
        self.review_rate = review_rate
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class Graph:
    """A graph used to represent .
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, category: str, address: str, name: str, price_range: str, latitude: float, longitude: float,
                   review_rate: float) -> None:
        """Add a vertex with the given restaurant details to this graph.
        The new vertex is not adjacent to any other vertices.
        Do nothing if the given restaurant is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _Vertex(category, address, name, price_range, latitude, longitude, review_rate)

    def add_edge(self, name1: Any, name2: Any) -> None:
        """Add an edge between the two vertices with the given restaurant names in this graph.
        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.
        Preconditions:
            - name1 != name2
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            v2 = self._vertices[name2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, name1: Any, name2: Any) -> bool:
        """Return whether name1 and name2 are adjacent vertices in this graph.
        Return False if name1 or name2 do not appear as vertices in this graph.
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            return any(v2.name == name2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, name: Any) -> set:
        """Return a set of the neighbours of the given name.
        Note that the *names* are returned, not the _Vertex objects themselves.
        Raise a ValueError if name does not appear as a vertex in this graph.
        """
        if name in self._vertices:
            v = self._vertices[name]
            return {neighbour.name for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex names in this graph.
        If kind != '', only return the items of the given vertex kind.
        """
        if kind != '':
            return {v.name for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.
        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)
        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.name, kind=v.kind, price=v.price, latitude=v.latitute, longitude=v.longitude)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.name, kind=u.kind, price=u.price, latitude=u.latitute, longitude=u.longitude)

                if u.name in graph_nx.nodes:
                    graph_nx.add_edge(v.name, u.name)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def load_graph(self, rest_file: str) -> Graph:
        """Return a restaurant graph corresponding to the given datasets.

        The CSV file should have the columns 'Category', 'Restaurant Address', 'Name',
        'Restaurant Price Range', 'Restaurant Latitude', 'Restaurant Longitude'
        and 'Review Rates'.
        """
        graph = Graph()

        with open(rest_file, 'r') as file:
            next(file)
            reader = csv.reader(file)
            for row in reader:
                category, address, name, price_range, latitude, longitude, review_rate = row
                price_min, price_max = map(int, price_range.replace('$', '').split('-'))
                latitude = float(latitude)
                longitude = float(longitude)
                review_rate = float(review_rate)

                graph.add_vertex(category, address, name, price_range, latitude, longitude, review_rate)

        return graph
