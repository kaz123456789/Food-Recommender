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

import requests
import math
import random

restaurants_type = {1: 'american', 2: 'chinese', 3: 'fast food', 4: 'french', 5: 'indian', 6: 'italian',
                    7: 'japanese', 8: 'korean', 9: 'mexican', 10: 'thai', 11: 'vegan', 12: 'vietnamese'}


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

    def add_vertex(self, category: int, address: str, name: str, price_range: int,
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
        return calculate_euclidean_distance(user_lat, user_lon, res_lat, res_lon) <= max_distance


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

    def vertices(self) -> dict:
        # This allows the outside code to read the vertices
        return self._vertices

    def add_vertex(self, category: int, address: str, name: str, price_range: int,
                   review_rate: float, location: tuple[float, float]) -> None:
        """Add a vertex with the given attributes to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if name not in self._vertices:
            self._vertices[name] = _CategoryVertex(category, address, name, price_range, review_rate, location)

    def add_edge(self, name1: Any, name2: Any, edge_4d: float = 1.0) -> None:
        """Add an edge between the two vertices with the given items in this graph,
        with the given weight.

        Raise a ValueError if name1 or name2 do not appear as vertices in this graph.

        Preconditions:
            - name1 != name2
        """
        if name1 in self._vertices and name2 in self._vertices:
            v1 = self._vertices[name1]
            v2 = self._vertices[name2]

            # Add the new edge
            v1.neighbours[v2] = edge_4d
            v2.neighbours[v1] = edge_4d
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
        restaurants_type = {1: 'american', 2: 'chinese', 3: 'fast food', 4: 'french', 5: 'indian', 6: 'italian',
                            7: 'japanese', 8: 'korean', 9: 'mexican', 10: 'thai', 11: 'vegan', 12: 'vietnamese'}

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

    def get_all_restaurants(self) -> list[_CategoryVertex]:
        """Return a list of all restaurant vertices in the graph."""
        # Ensure that _vertices.values() are actually instances of _CategoryVertex
        return list(self._vertices.values())

    def get_random_restaurant(self) -> _CategoryVertex:
        """Return a random restaurant from the graph."""
        if self._vertices:
            return random.choice(list(self._vertices.values()))

    def calculate_edge(self, restaurant1: _CategoryVertex, restaurant2: _CategoryVertex) -> float:
        """
        Calculate a weighted "distance" between two restaurants considering their
        category, price range, review rate, and geographical distance to the user.
        """
        category_similarity = 1 if restaurant1.category == restaurant2.category else 0

        price_similarity = 1 - abs(restaurant1.price_range - restaurant2.price_range) / max_price_range_difference
        review_similarity = 1 - abs(
            restaurant1.review_rate - restaurant2.review_rate) / 5  

        user_lat, user_lon = get_location_from_ip()
        geo_distance1 = calculate_euclidean_distance(user_lat, user_lon, restaurant1.location[0],
                                                     restaurant1.location[1])
        geo_distance2 = calculate_euclidean_distance(user_lat, user_lon, restaurant2.location[0],
                                                     restaurant2.location[1])

        edge_weight = 0.25 * category_similarity + 0.25 * price_similarity + 0.25 * review_similarity + 0.25 * (
                    geo_distance1 + geo_distance2) / 2

        return edge_weight


class User:
    """
    Represents a user in the restaurant recommender system.

    Attributes:
        name (str): The name of the user.
        last_visited_restaurant (_CategoryVertex): The last restaurant visited by the user based on the system's
        recommendation.
        disliked_restaurants (set[_CategoryVertex]): A set of restaurants that the user did not like.
    """

    def __init__(self, name: str):
        self.name = name
        self.last_visited_restaurant = None
        self.disliked_restaurants = set()

    def visit_restaurant(self, restaurant: _CategoryVertex):
        """
        Record the last visited restaurant based on the recommendation.
        """
        self.last_visited_restaurant = restaurant

    def feedback_on_last_visit(self, is_satisfied: bool):
        """Ask user if they are satisfied with the last visited restaurant."""
        if is_satisfied:
            print(f"I'm so glad to hear that! I will recommend more restaurants like "
                  f"{self.last_visited_restaurant.name} in future recommendations.")
        else:
            print(f"We are sorry you didn't enjoy it. We will avoid recommending it in the future.")
            self.disliked_restaurants.add(self.last_visited_restaurant)
            self.last_visited_restaurant = None

    def recommend_restaurants(self, graph: CategoryGraph) -> list[_CategoryVertex]:
        """
        Recommend restaurants based on user's history and feedback if exists.
        Otherwise, randomly generate a recommendation from the entire graph.
        """
        if not self.last_visited_restaurant:
            all_restaurants = graph.get_all_restaurants()
            filtered_restaurants = [r for r in all_restaurants if r not in self.disliked_restaurants]
            return [random.choice(filtered_restaurants)] if filtered_restaurants else []

        neighbours = graph.get_neighbours(self.last_visited_restaurant.name)
        recommendations = [self.last_visited_restaurant] + list(neighbours)
        filtered_recommendations = [rest for rest in recommendations if rest not in self.disliked_restaurants]

        return filtered_recommendations


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


# Load the graph of all the restaurants, where each restaurant is connected to
# the rest of the restaurants by the .
def load_graph(rest_file: str) -> CategoryGraph:
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
            location = tuple(float(val.strip()) for val in loc.split(','))
            review_rate = float(review_rate)

            graph.add_vertex(category, address, name, price_range, review_rate, location)

    vertex_names = list(graph.vertices().keys())
    for i, name1 in enumerate(vertex_names):
        for name2 in vertex_names[i + 1:]:  # Avoid connecting a vertex with itself and duplicate edges
            if name1 != name2:  # Additional check to avoid self-loop, might be redundant
                edge_weight = graph.calculate_edge(graph.vertices[name1], graph.vertices[name2])
                graph.add_edge(name1, name2, edge_weight)

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
