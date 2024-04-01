"""
CSC111 Project 2: Restaurant Recommender - FOODER

Module Description
==================
This Python module contains new classes to represent *category graphs and vertices*,
which we'll use to represent a restaurant recommender system with scores of restaurant
similarity as well.

Copyright and Usage Information
===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from __future__ import annotations
import csv
from typing import Any

import math
import random


def calculate_euclidean_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points using the Euclidean distance formula.
    """
    p1 = (lat1, lon1)
    p2 = (lat2, lon2)

    distance = math.dist(p1, p2)
    return distance


class _Vertex:
    """
    Each vertex item is a restaurant, represented by their name (str).

    Instance Attributes:
        - name: The data stored in this vertex, representing the name of the restaurant.
        - category: The region of the restaurant belongs to (i.e. Chinese, Japanese...)
        - address: The address of the restaurant.
        - price_range: A number that represents the range of price of the restaurant.
        - location: The location of the restaurant as a tuple where the first parameter is the latitude
        and the second parameter is the longitude.
        - review_rate: A rate range from 0 to 5 of the restaurant, where 0 means the restaurant sucks
        and 5 means the restaurant is fantastic.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - (c in range(1, 13) for c in self.category)
        - (p in range(1, 5) for p in self.price_range)
    """
    category: int
    address: str
    name: Any
    price_range: int
    review_rate: float
    location: tuple[float, float]
    neighbours: set[_Vertex]

    def __init__(self, category: int, address: str, name: str,
                 price_range: int, review_rate: float, location: tuple[float, float]) -> None:
        """
        Initialize a new vertex with the category, address, name, price range,
        review rate, location (latitude, longitude).
        This vertex is initialized with no neighbours.
        """
        self.category = category
        self.address = address
        self.name = name
        self.price_range = price_range
        self.review_rate = review_rate
        self.location = location
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class Graph:
    """
    A graph used to represent a restaurant system.
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

    def add_vertex(self, category: int, address: str, name: str, price_range: int,
                   review_rate: float, location: tuple[float, float]) -> None:
        """
        Add a vertex with the given restaurant details to this graph.
        The new vertex is not adjacent to any other vertices.
        Do nothing if the given restaurant is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _Vertex(category, address, name, price_range, review_rate, location)

    def add_whole_vertex(self, item: _CategoryVertex) -> None:
        """
        Add the whole vertex into the graph
        """
        self._vertices[item.name] = item

    def add_edge(self, name1: Any, name2: Any) -> None:
        """
        Add an edge with a similarity score between the two vertices with the given items in this graph.

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
    """A vertex that represent a restaurant in a restaurant system graph.

    Same documentation as _Vertex from above, except now neighbours is a dictionary mapping
    a neighbour vertex to the similarity score of the edge to from self to that neighbour.

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
        - (c in range(1, 13) for c in self.category)
        - (p in range(1, 5) for p in self.price_range)
        - 0 <= self.review_rate <= 5
    """
    category: int
    address: str
    name: Any
    price_range: int
    review_rate: float
    location: tuple[float, float]
    neighbours: dict[_CategoryVertex, float]

    def __init__(self, category: int, address: str, name: Any, price_range: int,
                 review_rate: float, location: tuple[float, float]) -> None:
        """Initialize a new vertex with the given category, address, name, price_range, review_rate,
        and location.

        This vertex is initialized with no neighbours.

        Preconditions:
            - category in range(1, 13)
            - price_range in range(1, 4)
            - 0 <= review rate <= 5
        """
        super().__init__(category, address, name, price_range, review_rate, location)
        self.neighbours = {}

    def is_within_distance(self, user_lat: float, user_lon: float, max_distance: float) \
            -> bool:
        """
        Determine if the restaurant is within the maximum distance from the user's location.
        """
        res_lat, res_lon = self.location
        return calculate_euclidean_distance(user_lat, user_lon, res_lat, res_lon) <= max_distance

    def similarity_score(self, other: _CategoryVertex, ip: tuple[float, float]) -> float:
        """
        Calculate the Euclidean distance between two restaurants in 4-dimensions such that
        the coordinates are represented as category, prince range, review rate, and the Euclidean
        distance between the restaurant and the user. The value returned is the similarity_score.
        """
        p0_lat, p0_lon = ip
        p1_lat, p1_lon = self.location
        p2_lat, p2_lon = other.location
        p1 = (self.category, self.price_range, self.review_rate,
              calculate_euclidean_distance(p0_lat, p0_lon, p1_lat, p1_lon))
        p2 = (other.category, other.price_range, other.review_rate,
              calculate_euclidean_distance(p0_lat, p0_lon, p2_lat, p2_lon))

        distance = math.sqrt(sum((float(p1[i]) - float(p2[i])) ** 2 for i in range(4)))
        return distance

    def calculate_user_feedback(self, feedback: str) -> None:
        """
        Calculate the user feedback / review rate.
        """
        if 'yes' in feedback.lower():
            if self.review_rate < 3.0:
                self.review_rate += 0.5
            elif self.review_rate < 5.0:
                self.review_rate += 0.2
        else:
            if self.review_rate <= 0.5:
                self.review_rate = 0.0
            else:
                self.review_rate -= 0.2


class CategoryGraph(Graph):
    """A graph used to represent a restaurant system.

    Note that this is a subclass of the Graph class, and so inherits any methods
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

    def get_vertex(self, item: str) -> _CategoryVertex:
        """
        Get the vertex of that has the input item name.
        """
        return self._vertices[item]

    def add_vertex(self, category: int, address: str, name: str, price_range: int,
                   review_rate: float, location: tuple[float, float]) -> None:
        """Add a vertex with the given attributes to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _CategoryVertex(category, address, name, price_range, review_rate, location)

    def add_edge(self, name1: Any, name2: Any, similarity_score: float = 1.0) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given similarity score.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.

        Preconditions:
            - name1 != name2
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            v2 = self._vertices[name2]

            # Add the new edge
            v1.neighbours[v2] = similarity_score
            v2.neighbours[v1] = similarity_score
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_similarity_score(self, v1: Any, v2: Any, ip: tuple[float, float]) -> float:
        """
        Return the similarity score between the two given items in this graph.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.
        """

        return v1.similarity_score(v2, ip)

    def get_sim_rest(self, restaurant: str) -> list[str]:
        """
        Return a list of resturants based on the similarity scores.
        """

        v = self._vertices[restaurant]
        return [key.name for key in v.neighbours]

    def similar_rest_all_connected(self, restaurant: str, ip: tuple[float, float]) -> None:
        """
        Connects restaurant to its top 5 most similar restaurants based on similarity scores.
        """
        similar_res_names = self.most_similar_restaurants(restaurant)

        for res in similar_res_names:
            s_score = self.get_similarity_score(res, restaurant, ip)
            if s_score <= 0.1:
                self.add_edge(res, restaurant, s_score)

    def most_similar_restaurants(self, base_restaurant: str, ip: tuple[float, float]) -> list[str]:
        """
        Recommend the top 5 most similar restaurants by calculating the similarity score
        between the restaurant and the rest of the restaurants, then return a list of
        the names of the top 5 similar restaurants.
        """
        recommendations = []

        for res in self._vertices:
            v = self._vertices[res]
            if v.name != base_restaurant:
                sim_score = self.get_similarity_score(base_restaurant, v.name, ip)
                if (sim_score, res) not in recommendations:
                    recommendations.append((sim_score, v.name))

        recommendations.sort()
        recommendations.reverse()

        lst_of_res = [score[1] for score in recommendations]

        return lst_of_res[:5]

    def get_all_restaurants(self) -> list[_CategoryVertex]:
        """Return a list of all restaurant vertices in the graph."""
        # Ensure that _vertices.values() are actually instances of _CategoryVertex
        return list(self._vertices.values())

    def get_random_restaurant(self) -> _CategoryVertex:
        """Return a random restaurant from the graph."""
        if self._vertices:
            return random.choice(list(self._vertices.values()))
        else:
            raise ValueError

    @property
    def vertices(self):
        return self._vertices


class User:
    """
    Represents a user in the restaurant recommender system.

    Instance Attributes:
        - name (str): The name of the user.
        - last_visited_restaurant (_CategoryVertex): The last restaurant visited by the user based
        on the recommendation system.
        - disliked_restaurants (set[_CategoryVertex]): A set of restaurants that the user did not like.
    """
    name: str
    last_visited_restaurant: _CategoryVertex | None
    disliked_restaurants: set[_CategoryVertex]

    def __init__(self, name: str) -> None:
        """Initialize a user with their name, the latest restaurant they visited and a set of restaurants they dislike.
        """
        self.name = name
        self.last_visited_restaurant = None
        self.disliked_restaurants = set()

    def recommend_restaurants(self, graph: CategoryGraph) -> list[_CategoryVertex]:
        """
        Recommend restaurants based on user's history and feedback if exists.
        Otherwise, randomly generate a recommendation from the entire graph.
        """
        if self.last_visited_restaurant and self.last_visited_restaurant not in self.disliked_restaurants:
            similar_restaurants = graph.most_similar_restaurants(self.last_visited_restaurant.name)
            return [self.last_visited_restaurant] + similar_restaurants
        else:
            all_restaurants = graph.get_all_restaurants()
            filtered_restaurants = [r for r in all_restaurants if r not in self.disliked_restaurants]
            return random.sample(filtered_restaurants, min(5, len(filtered_restaurants)))


def load_graph(rest_file: str, ip: tuple[float, float]) -> CategoryGraph:
    """Return a restaurant graph corresponding to the given datasets.

    The CSV file should have the columns 'Category', 'Restaurant Address', 'Name',
    'Restaurant Price Range', 'Restaurant Location' and 'Review Rates'.
    """
    graph = CategoryGraph()
    index = 0

    with open(rest_file, 'r', encoding='cp1252') as file:  # Assuming CP1252 encoding
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        for row in reader:
            category, address, name, price, review_rate, loc = row
            location = tuple(val.strip() for val in loc.split(','))
            latitude = float(location[0])
            longitude = float(location[1])
            location = (latitude, longitude)
            if review_rate == 'NA':
                review_rate = 0
            else:
                review_rate = float(review_rate)
            curr_v = _CategoryVertex(category, address, name, price, review_rate, location)
            graph.add_whole_vertex(curr_v)
            if index != 0:
                sim_score = graph.get_similarity_score(curr_v, pre_v, ip)
                if sim_score <= 0.1:
                    graph.add_edge(curr_v.name, pre_v.name, sim_score)

            pre_v = curr_v
            index += 1

    # names = list(graph.vertices.keys())  # Get all the names (identifiers) of the vertices
    # for i in range(len(names)):
    #     for j in range(i + 1, len(names)):
    #         # No need to check for similarity score threshold here as per your instruction, connect all
    #         try:
    #             score = graph.get_similarity_score(names[i], names[j])
    #             graph.add_edge(names[i], names[j], score)
    #         except ValueError as e:
    #             print(f"Error adding edge: {e}")

    return graph


class AllUsers:
    """
    Represents all the users in the food recommender. No instance objects share the same name.

    Instance Attributes:
        - list_of_users (User): A list of users that have used the FOODER
    """
    list_of_users: dict[str, User]

    def __init__(self) -> None:
        """Initialize AllUsers with an empty list of users."""
        self.list_of_users = {}

    def add_new_user(self, name: str, u: User) -> None:
        """
        Add a new user to the list.
        """
        self.list_of_users[name] = u

    def existing_user(self, user_name: str) -> User:
        """
        return the existing user form the list.
        """
        return self.list_of_users[user_name]


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
