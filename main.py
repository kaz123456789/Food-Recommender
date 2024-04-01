"""
CSC111 Project 2: Food Recommender - FOODER

Module Description
==================
This the main file of our project.

===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from recommender_4d_ver import CategoryGraph, AllUsers, User, load_graph, get_location_from_ip
import csv

read_lines = []

# The cuisine type each number represents in the csv data file.
cuisine_type = {1: 'american', 2: 'chinese', 3: 'fast food', 4: 'french', 5: 'indian', 6: 'italian',
                    7: 'japanese', 8: 'korean', 9: 'mexican', 10: 'thai', 11: 'vegan', 12: 'vietnamese'}

price_range = {1: 'Under $10', 2: '$11-30', 3: '$31-60', 4: 'Above $61'}


def get_price_range(num: int) -> str:
    """
    Return the corresponding price range according to the dictionary mapping
    cuisine type.
    """
    return price_range[num]


def get_category(num: int) -> str:
    """
    Return the corresponding category according to the dictionary mapping
    price_range.
    """
    return cuisine_type[num]


def record_last_visit(u: User, g: CategoryGraph, restaurant: str) -> None:
    """
    Record the last visited restaurant based on the recommendation.
    """
    r = CategoryGraph.get_vertex(g, restaurant)
    u.last_visited_restaurant = r


if __name__ == "__main__":
    restaurant_graph = load_graph("filtered_restaurant_dt_4d.csv")
    new_game = False
    while not new_game:
        quit_game = False

        print("Welcome!This is the restaurant recommender FOODER. \n")

        all_users = AllUsers()
        while not quit_game:
            user_name = input('Pleaser enter your name: ')
            user = User(user_name)

            if user not in all_users.list_of_users:
                all_users.list_of_users.append(user)
                print(f"Welcome to FOODER, {user_name}!")
            else:
                print(f"Welcome back to FOODER, {user_name}! We are confident to find you a "
                      f"matching restaurant this time, too!")

            if user.last_visited_restaurant:
                you_may_like = restaurant_graph.most_similar_restaurants(user.last_visited_restaurant.name)
                restaurant_graph.most_similar_restaurants_all_connected(user.last_visited_restaurant.name)
            else:
                random_rest = restaurant_graph.get_random_restaurant()
                price_range = get_price_range(random_rest.price_range)
                satisfy_with_first = input('Are you satisfy with this restaurant? Pleaser enter \'yes\' or \'no\': ')

                if satisfy_with_first.lower() == 'no':
                    random_rests = user.recommend_restaurants(restaurant_graph)
                    for rest in random_rests:
                        print(f'{rest}')
                    satisfied_rest = input('Pick one restaurant from the following that matches with your taste the most:')
                    record_last_visit(user, restaurant_graph, satisfied_rest)

                print(f'Congratulations! You\'ve matched with your restaurant: {random_rest.name}!' +
                      '\n Details about the restaurant:' + f'\n Address: {random_rest.address}'
                      + f'\n Price range: {price_range}')
                satisfy = input('Are you satisfy with this restaurant? Pleaser enter \'yes\' or \'no\':')
                user.feedback_on_last_visit(satisfy)

                again = input('Do you want to start a new game or end the game? Pleaser enter \'new game\' or \'quit\':')
                if again == 'quit':
                    new_game = True
                else:
                    quit_game = True




