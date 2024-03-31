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
from typing import Any, Union

import requests
import math


def get_location_from_ip() -> tuple[float, float]:
    """
    Retrieve the current location (latitude and longitude) based on the public IP address of the user.
    """
    response = requests.get('https://api64.ipify.org?format=json').json()
    ip_address = response['ip']

    location_response = requests.get(f'https://ipinfo.io/{ip_address}/json').json()
    lat, lon = map(float, location_response.get('loc', '0,0').split(','))
    return lat, lon


def calculate_euclidean_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the Euclidean distance between two points.
    """
    p1 = (lat1, lon1)
    p2 = (lat2, lon2)

    distance = math.dist(p1, p2)
    return distance


class _Vertex:
    """
    Each vertex item is a restaurant, a string.

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
        - self.category in {'chinese', 'fast food', 'italian', 'japanese', 'indian',
                            'american', 'thai', 'mexican', 'korean', 'vietnamese', 'vegan', 'french'}
        - self.price_range in {'1', '2', '3', '4'}
    """
    category: str
    address: str
    name: Any
    price_range: int
    review_rate: float
    location: tuple[float, float]
    neighbours: set[_Vertex]

    def __init__(self, category: str, address: str, name: str,
                 price_range: int, review_rate: float, location: tuple[float, float]) -> None:
        """
        Initialize a new vertex with the category, address, given name, price range,
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
    A graph used to represent a categorized/price-ranged restaurants network.
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

    def add_vertex(self, category: str, address: str, name: str, price_range: int,
                   review_rate: float, location: tuple[float, float]) -> None:
        """
        Add a vertex with the given restaurant details to this graph.
        The new vertex is not adjacent to any other vertices.
        Do nothing if the given restaurant is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _Vertex(category, address, name, price_range, review_rate, location)

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
            # If either vertex is not in the graph, raise an error
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
    """A vertex in a categorized/price-ranged restaurant graph, used to represent a restaurant.

    Same documentation as _Vertex from above, except now neighbours is a dictionary mapping
    a neighbour vertex to the category or price range of the edge to from self to that neighbour.

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
        - self.category in {'chinese', 'fast food', 'italian', 'japanese', 'indian',
                            'american', 'thai', 'mexican', 'korean', 'vietnamese', 'vegan', 'french'}
        - self.price_range in {'1', '2', '3', '4'}
        - 0 <= self.review rate <= 5
    """
    category: str
    address: str
    name: Any
    price_range: int
    review_rate: float
    location: tuple[float, float]
    neighbours: dict[_CategoryVertex, Union[str, int]]

    def __init__(self, category: str, address: str, name: Any, price_range: int,
                 review_rate: float, location: tuple[float, float]) -> None:
        """Initialize a new vertex with the given category, address, name, price_range, review_rate,
        and location.

        This vertex is initialized with no neighbours.

        Preconditions:
            - category in {'chinese', 'fast food', 'italian', 'japanese', 'indian',
                            'american', 'thai', 'mexican', 'korean', 'vietnamese', 'vegan', 'french'}
            - price_range in {'1', '2', '3', '4'}
            - 0 <= review rate <= 5
        """
        super().__init__(category, address, name, price_range, review_rate, location)
        self.neighbours = {}

    def similarity_score(self, other: _Vertex) -> float:
        """Calculate the similarity score between this vertex and another vertex."""
        similarity = 0.0

        print('Sort by the factor you value from the most to the least, in order, separate by \',\'.\n'
              'You may choose from the following: category, prince range, and maximum distance.')
        ans3 = input('Your answer: ')
        sorted_factors = [factor.strip() for factor in ans3.split(',')]
        valid_factors = {'category', 'price range', 'maximum distance'}
        while not (set(sorted_factors) == valid_factors and len(sorted_factors) == len(valid_factors)):
            print('This is not a valid option, please enter a valid sorting of the factors:')
            ans3 = input('Your answer: ')
            sorted_factors = [factor.strip() for factor in ans3.split(',')]

        weights = [0.5, 0.3, 0.2]  # Priority: 1st, 2nd, 3rd
        pref_weights = {pref: weight for pref, weight in zip(sorted_factors, weights)}

        # Compare category (assuming 'category' directly maps to 'category')
        if self.category == other.category:
            similarity += pref_weights['category']

        # Compare price range
        if self.price_range == other.price_range:
            similarity += pref_weights['price range']

        # Compare review rate (assuming this factors into 'maximum distance' for simplicity)
        rating_difference = abs(self.review_rate - other.review_rate)
        review_similarity = 1 - (rating_difference / 5.0)
        similarity += pref_weights['maximum distance'] * review_similarity

        return similarity

    def is_within_distance(self, user_lat: float, user_lon: float, max_distance: float) \
            -> bool:
        """
        Determine if the restaurant is within the maximum distance from the user's location.
        """
        res_lat, res_lon = self.location
        return calculate_distance(user_lat, user_lon, res_lat, res_lon) <= max_distance


class CategoryGraph(Graph):
    """A graph used to represent a categorized/price-ranged restaurants network.

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

    def vertices(self):
        # This allows the outside code to read the vertices
        return self._vertices.values()

    def add_vertex(self, category: str, address: str, name: str, price_range: int,
                   review_rate: float, location: tuple[float, float]) -> None:
        """Add a vertex with the given attributes to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _CategoryVertex(category, address, name, price_range, review_rate, location)

    def add_edge(self, name1: Any, name2: Any, edge_type: Union[str, int] = '') -> None:
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
            v1.neighbours[v2] = edge_type
            v2.neighbours[v1] = edge_type
        else:
            # We didn't find an existing vertex for both items.
            raise ValueError

    def get_similarity_score(self, name1: Any, name2: Any) -> float:
        """
        Return the similarity score between the two given items in this graph.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.
        """

        if name1 not in self._vertices or name2 not in self._vertices:
            raise ValueError
        v1 = self._vertices[name1]
        v2 = self._vertices[name2]
        return v1.similarity_score(v2)

    def top_restaurant(self) -> str:
        """
        Run the recommender and return the top restaurant based on user preference:
        type of cuisine, maximum acceptable distance, and the price range.
        """
        restaurants_type = {'chinese', 'fast food', 'italian', 'japanese', 'indian',
                            'american', 'thai', 'mexican', 'korean', 'vietnamese', 'vegan', 'french'}

        rest_questions = ['What is your preferred type of cuisine?',
                          'What is the maximum distance of restaurants you are looking for (in km)?',
                          'What price range are you looking for?']

        user_input = get_user_input(rest_questions, restaurants_type)
        category, distance_range, price_range = user_input
        player_lat, player_lon = get_location_from_ip()
        top_res = self.top_reviewed_restaurant(category, player_lat, player_lon, distance_range, price_range)

        return top_res.name

    def top_reviewed_restaurant(self, desired_cuisine: str, user_lat: float, user_lon: float,
                                max_distance: float, price: int) -> _CategoryVertex:
        """
        Recommend the top restaurant (as a _CategoryVertex, not the name of the restaurant)
        based on user location and user's preference of cuisine type, maximum acceptable distance,
        and acceptable price range.
        """
        qualifying_restaurants = []
        for restaurant in self._vertices.values():
            if (restaurant.category == desired_cuisine
                    and restaurant.is_within_distance(max_distance, user_lat, user_lon)
                    and restaurant.price_range == price):
                if (restaurant.review_rate, restaurant) not in qualifying_restaurants:
                    qualifying_restaurants.append((restaurant.review_rate, restaurant))

        sorted_recommendations = sorted(qualifying_restaurants, reverse=True)
        res_recommendations = [score[1] for score in sorted_recommendations]

        return res_recommendations[0]

    def final_recommend_restaurants(self, restaurant: str, number: int) -> list[str]:
        """
        Recommend the top number (i.e. 3, 4, etc.) restaurants by calculating the similarity scores
        between restaurant and the restaurants with the same category/price range and return a list
        of length number.
        """
        recommendations = []
        for res in self._vertices.values():
            if res.name != restaurant:
                sim_score = self.get_similarity_score(res, restaurant)
                if (res.review_rate, restaurant) not in recommendations:
                    recommendations.append((sim_score, restaurant))

        sorted_recommendations = sorted(recommendations, reverse=True)
        final_recommendations = [score[1] for score in sorted_recommendations]

        return final_recommendations[:number]

    def modify_review_rate(self, rest: list[str], rates: list[int]) -> None:
        """
        Mutates the graph based on the likes and dislikes the user inputted.
        This will help the recommender generate a more accurate answer next time based
        on user's preference on the restaurants.
        """
        for i in range(len(rates)):
            if not rates[i]:
                self._vertices[rest[i]] -= 0.2
            else:
                self._vertices[rest[i]] += 0.2

    # fqy
    def get_rest_address(self, name: str) -> str:
        """
        Return the address of the input restaurant.
        """
        return self._vertices[name].address


# fqy
def get_user_input(questions: list[str], rest_types: set[str]) -> list[str | int]:
    """ Return a list of answers the user input."""

    answer_so_far = []

    print(questions[0])
    print('(Available options: Chinese, Fast food, Italian, American, '
          'Thai, Mexican, Korean, Vietnamese, Vegan, or French)')
    ans1 = input('Your answer: ')
    while ans1.lower() not in rest_types:
        print('This is not a valid option, please enter another answer:')
        ans1 = input('Your answer: ')
    answer_so_far.append(ans1)

    print(questions[1])
    ans2 = input('Your answer: ')
    while not ans2.isdigit():
        print('This is not a number, please enter a correct distance:')
        ans2 = input('Your answer: ')
    answer_so_far.append(int(ans2))

    print(questions[2])
    print('Enter 1 for under $10, 2 for $11-30, 3 for $31-60, or 4 for above $61')
    ans3 = input('Your answer: ')
    while ans3 not in {'1', '2', '3', '4'}:
        print('This is not a valid option, please enter another answer:')
        ans3 = input('Your answer: ')
    answer_so_far.append(int(ans3))

    return answer_so_far


# Load the graph of all the restaurants, where the edge is either category or price range.
def load_graph(rest_file: str, edge_type: str) -> CategoryGraph:
    """Return a restaurant graph corresponding to the given datasets.

    The CSV file should have the columns 'Category', 'Restaurant Address', 'Name',
    'Restaurant Price Range', 'Restaurant Location' and 'Review Rates'.
    """
    graph = CategoryGraph()

    with open(rest_file, 'r', encoding='cp1252') as file:  # Assuming CP1252 encoding
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row
        for row in reader:
            category, address, name, price_range, review_rate, loc = row
            # price_min, price_max = map(int, price_range.replace('$', '').split('-'))
            location = tuple(float(val.strip()) for val in loc.split(','))
            latitude = float(location[0])
            longitude = float(location[1])
            location = (latitude, longitude)
            review_rate = float(review_rate)

            graph.add_vertex(category, address, name, price_range, review_rate, location)

    vertices = list(graph.vertices())  # Assuming _vertices stores vertex objects.
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            vertex1 = vertices[i]
            vertex2 = vertices[j]
            if edge_type == 'category' and vertex1.category == vertex2.category:
                graph.add_edge(vertex1, vertex2, vertex1.category)
            elif edge_type == 'price_range' and vertex1.price_range == vertex2.price_range:
                graph.add_edge(vertex1, vertex2, vertex1.price_range)

    return graph


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
