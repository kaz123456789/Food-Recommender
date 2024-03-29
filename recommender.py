"""
CSC111 Project 2: Food Recommender

Module Description
==================
This module contains the Tree class and various methods and functions.

===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from __future__ import annotations
import csv
from typing import Any

import networkx as nx
import requests
from math import radians, sin, cos, sqrt, atan2


def safe_float_convert(input_str: str, default_value: None) -> float | None:
    """Attempt to convert a string to a float. Return a default value if the conversion fails."""
    try:
        return float(input_str)
    except ValueError:
        return default_value


class _Vertex:
    """A vertex in a restaurant graph, used to represent a restaurant.
    Each vertex item is either a restaurant name.

    Instance Attributes:
        - name: The data stored in this vertex, representing the name of the restaurant.
        - category: The region of the restaurant (i.e. Chinese, Japanese...)
        - address: The address of the restaurant.
        - price_range: A range of price of the restaurant.
        - location: The location of the restaurant as a tuple where the first parameter is the latitude
        and the second parameter is the longitude
        - review_rate: A rate range from 0 to 5 of the restaurant.
        0 means the restaurant sucks and 5 means the restaurant is fantastic.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    category: str
    address: str
    name: Any
    price_range: str
    location: tuple[float, float]
    review_rate: float
    neighbours: set[_Vertex]

    def __init__(self, category: str, address: str, name: str, price_range: str, location: tuple[float, float],
                 review_rate: float) -> None:
        """
        Initialize a new vertex with the given name, category, address, price_range,
        location, review_rate, neighbours.
        This vertex is initialized with no neighbours.
        """
        self.category = category
        self.address = address
        self.name = name
        self.price_range = price_range
        self.location = location
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
        """
        Initialize an empty graph (no vertices or edges).
        """
        self._vertices = {}

    def add_vertex(self, category: str, address: str, name: str, price_range: str, location: tuple[float, float],
                   review_rate: float) -> None:
        """
        Add a vertex with the given restaurant details to this graph.
        The new vertex is not adjacent to any other vertices.
        Do nothing if the given restaurant is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _Vertex(category, address, name, price_range, location, review_rate)

    def add_edge(self, name1: Any, name2: Any) -> None:
        """
        Add an edge between the two vertices with the given restaurant names in this graph.
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
        """
        Return whether name1 and name2 are adjacent vertices in this graph.
        Return False if either name1 or name2 do not appear as vertices in this graph.
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            return any(v2.name == name2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, name: Any) -> set:
        """
        Return a set of the neighbours of the given name.
        Note that the *names* are returned, not the _Vertex objects themselves.
        Raise a ValueError if name does not appear as a vertex in this graph.
        """
        if name in self._vertices:
            v = self._vertices[name]
            return {neighbour.name for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, category: str = '') -> set:
        """
        Return a set of all vertex names in this graph.
        If category != '', only return the items of the given vertex kind.
        """
        if category != '':
            return {v.name for v in self._vertices.values() if v.category == category}
        else:
            return set(self._vertices.keys())


class _CategoryVertex(_Vertex):
    """A vertex in a weighted book review graph, used to represent a user or a book.

    Same documentation as _Vertex from Exercise 3, except now neighbours is a dictionary mapping
    a neighbour vertex to the weight of the edge to from self to that neighbour.
    Note that for this exercise, the weights will be integers between 1 and 5.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex, and their corresponding
            edge weights.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'book'}
    """
    category: str
    address: str
    name: Any
    price_range: str
    location: tuple[float, float]
    review_rate: float
    neighbours: dict[_CategoryVertex, str]

    def __init__(self, category: str, address: str, name: str, price_range: str, location: tuple[float, float],
                 review_rate: float) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        super().__init__(category, address, name, price_range, location, review_rate)
        self.neighbours = {}


class CategoryGraph(Graph):
    """A weighted graph used to represent a book review network that keeps track of review scores.

    Note that this is a subclass of the Graph class from Exercise 3, and so inherits any methods
    from that class that aren't overridden here.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _WeightedVertex object.
    _vertices: dict[Any, _CategoryVertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

        # This call isn't necessary, except to satisfy PythonTA.
        Graph.__init__(self)

    def add_vertex(self, category: str, address: str, name: str, price_range: str, location: tuple[float, float],
                   review_rate: float) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if name not in self._vertices:
            self._vertices[name] = _CategoryVertex(category, address, name, price_range, location, review_rate)

    def add_edge(self, name1: Any, name2: Any, category: str = '') -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            v2 = self._vertices[name2]

            # Add the new edge
            v1.neighbours[v2] = category
            v2.neighbours[v1] = category
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_category(self, name1: Any) -> str:
        """Return the category of the edge between the given items.

        Raise ValueError if two vertices have different categories.

        Preconditions:
            - item1 and item2 are vertices in this graph
        """
        return self._vertices[name1].category
        # v1_category = self._vertices[name1].category
        # v2_category = self._vertices[name2].category
        # if v1_category == v2_category:
        #     return v1_category
        # raise ValueError

    def load_graph(self, rest_file: str) -> CategoryGraph:
        """Return a restaurant graph corresponding to the given datasets.

        The CSV file should have the columns 'Category', 'Restaurant Address', 'Name',
        'Restaurant Price Range', 'Restaurant Location' and 'Review Rates'.
        """
        graph = CategoryGraph()

        with open(rest_file, 'r', encoding='cp1252') as file:  # Assuming CP1252 encoding
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                category, address, name, price_range, latitude, longitude, review_rate = row
                # price_min, price_max = map(int, price_range.replace('$', '').split('-'))
                latitude = safe_float_convert(latitude, default_value=None)
                longitude = safe_float_convert(longitude, default_value=None)
                location = (latitude, longitude)
                review_rate = safe_float_convert(review_rate, default_value=None)

                graph.add_vertex(category, address, name, price_range, location, review_rate)

        return graph

    def get_user_preference(self, file_name: str) -> str:
        """Ask the user for their preferred type of cuisine and return it."""
        valid_cuisines = set()

        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                valid_cuisines.add(row[0])

        print("Please enter your preferred type of cuisine (Chinese, Korean etc.): ")
        print(f"Options: {', '.join(valid_cuisines)}")
        desired_cuisine = input().strip()

        if desired_cuisine in valid_cuisines:
            return desired_cuisine
        else:
            print(f"Invalid input. Please choose from the available options.")
            return self.get_user_preference(file_name)

    def is_within_distance(self, restaurant: _Vertex, user_lat: float, user_lon: float, max_distance: float) -> bool:
        """
        Determine if the restaurant is within the maximum distance from the user's location.
        """
        return self.calculate_distance(user_lat, user_lon,
                                       restaurant.location[0], restaurant.location[1]) <= max_distance

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the distance between two points on the earth specified in decimal degrees.
        """
        r = 6371.0  # Earth radius in kilometers

        d_lat = radians(lat2 - lat1)
        d_lon = radians(lon2 - lon1)
        a = sin(d_lat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = r * c
        return distance

    @staticmethod
    def get_location_from_ip() -> tuple[float, float]:
        """
        Retrieve the current location (latitude and longitude) based on the public IP address of the user.
        """
        response = requests.get('https://api64.ipify.org?format=json').json()
        ip_address = response['ip']

        location_response = requests.get(f'https://ipinfo.io/{ip_address}/json').json()
        lat, lon = map(float, location_response.get('loc', '0,0').split(','))
        return lat, lon

    def filter_restaurants(self, max_distance: float, desired_cuisine: str, user_lat: float, user_lon: float) ->\
            list[_Vertex]:
        qualifying_restaurants = []
        for restaurant in self._vertices.values():
            if restaurant.category == desired_cuisine and self.is_within_distance(restaurant, max_distance,
                                                                                  user_lat, user_lon):
                qualifying_restaurants.append(restaurant)
        return qualifying_restaurants


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['csv', 'networkx'],
        'allowed-io': ['load_weighted_review_graph'],
        'max-nested-blocks': 4
    })
