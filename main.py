"""
CSC111 Project 2: Restaurant Recommender - FOODER

Module Description
==================
This the main file of our project.

Copyright and Usage Information
===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from recommender_4d_ver import CategoryGraph, AllUsers, User, load_graph, get_location_from_ip

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


def record_last_visited(u: User, g: CategoryGraph, restaurant: str) -> None:
    """
    Record the last visited restaurant based on the recommendation.
    """
    r = CategoryGraph.get_vertex(g, restaurant)
    u.last_visited_restaurant = r


if __name__ == "__main__":
    restaurant_graph = load_graph("filtered_restaurant_dt_4d.csv")

    quit_game = False
    while not quit_game:
        new_game = False
        print("Welcome!This is the restaurant recommender FOODER. \n")
        all_users = AllUsers()

        while not new_game:
            user_name = input('Pleaser enter your name: \n')
            user = User(user_name)

            if user not in all_users.list_of_users:
                all_users.list_of_users.append(user)
                print(f"Welcome to FOODER, {user_name}!\n")
            else:
                print(f"Welcome back to FOODER, {user_name}! We are confident to find you a "
                      f"matching restaurant this time, too!")

            if user.last_visited_restaurant:
                you_may_like = restaurant_graph.most_similar_restaurants(user.last_visited_restaurant.name)
                restaurant_graph.similar_rest_all_connected(user.last_visited_restaurant.name)

            else:
                final_rest = None
                random_rest = restaurant_graph.get_random_restaurant()
                try_random = input(f'Do you want to try: {random_rest.name}? Pleaser enter \'yes\' or \'no\': \n')
                if 'yes' in try_random.lower():
                    final_rest = random_rest
                elif 'no' in try_random.lower():
                    print('Then I\'ll recommend you 5 random resturants: ')
                    random_rests = user.recommend_restaurants(restaurant_graph)
                    for rest in random_rests:
                        print(f'{rest.name}')
                    satisfied_rest = input(
                        'Pick one restaurant from the following that matches with your taste the most:')
                    final_rest = CategoryGraph.get_vertex(restaurant_graph, satisfied_rest)
                    record_last_visited(user, restaurant_graph, satisfied_rest)
                record_last_visited(user, restaurant_graph, random_rest.name)
                price_range = get_price_range(int(final_rest.price_range))
                print(f'\nCongratulations! You\'ve matched with your restaurant: {final_rest.name}!' +
                      '\nDetails about the restaurant:' + f'\nAddress: {final_rest.address}'
                      + f'\nPrice range: {price_range}\n')
                satisfy = input('Are you satisfy with this restaurant? Pleaser enter \'yes\' or \'no\':\n')
                if 'yes' in satisfy:
                    print(f"\nI'm so glad to hear that! I will recommend you more restaurants like "
                          f"{final_rest.name} in future recommendations.\n")
                    user.last_visited_restaurant.calculate_user_feedback('yes')
                else:
                    print("\nWe are sorry to hear that you didn't enjoy it. We will avoid recommending "
                          "it in the future.\n")
                    user.disliked_restaurants.add(user.last_visited_restaurant)
                    user.last_visited_restaurant.calculate_user_feedback('no')
                    user.last_visited_restaurant = None

                again = input('Do you want to get more recommendations? Pleaser enter \'new round\' or \'quit\':\n')
                if again == 'quit':
                    quit_game = True
                    break

    print('\nThank you for choosing the best restaurant recommender FOODER! It\'s our pleasure to assist you!')
