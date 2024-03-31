"""
CSC111 Project 2: Food Recommender - FOODER

Module Description
==================
This the main file of our project.

===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from recommender_4d_ver import CategoryGraph, AllUsers, User, load_graph, get_user_input, get_location_from_ip
import csv

read_lines = []


def read_latest_input_from_csv(lines: list[str], file: str) -> str:
    """
    Reads the only line in the CSV file, which is the latest user input.
    """
    with open(file, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:  # There should only be one row
            if row not in lines:
                lines.append(row[0])
                return lines[-1]


if __name__ == "__main__":
    restaurant_graph = load_graph("filtered_restaurant_dt_4d.csv")
    quit_game = False

    print("Welcome!This is the restaurant recommender FOODER. \n")

    all_users = AllUsers()
    while not quit_game:
        user_name = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')
        user = User(user_name)

        if user not in all_users.list_of_users:
            all_users.list_of_users.append(user)
            print(f"Welcome to FOODER, {user_name}!")
        else:
            print(f"Welcome back to FOODER, {user_name}! We are confident to find you a "
                  f"matching restaurant this time, too!")

        if not user.last_visited_restaurant:
            you_may_like = restaurant_graph.most_similar_restaurants(user.last_visited_restaurant.name)
            restaurant_graph.most_similar_restaurants_all_connected(user.last_visited_restaurant.name)
        else:
            random_rest = restaurant_graph.get_random_restaurant()
            satisfy_with_first = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')

            if satisfy_with_first.lower() == 'yes':
                quit_game = True
                break
            else:
                random_rests = user.recommend_restaurants(restaurant_graph)
                for res in random_rests:
                    print(res.name)
                satisfy = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')
                user.last_visit(restaurant_graph.vertices()[satisfy])
                user.feedback_on_last_visit(satisfy in restaurant_graph.vertices().keys())

            # Ask user if they want to try again, if no, quit the game, is yes, continue.
            if_quit = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')

        if if_quit == 'yes':
            quit_game = True











    print('Congratulations! You\'ve find your restaurant match! We hope can enjoy the food there!')
    print(f'Your final choice: {lst_of_rest[index]}' + '\n')
    print(f'The the address of the restaurant: {address}')





    
    
