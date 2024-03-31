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


def read_inputs(lines: list[str], new_line: str) -> None:
    """
    Keep track of the read lines.
    """
    if new_line not in lines:
        lines.append(new_line)


def read_latest_input_from_csv(lines: list[str], file: str) -> str:
    """
    Reads the only line in the CSV file, which is the latest user input.
    """
    with open(file, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:  # There should only be one row
            if row not in lines:
                return row


if __name__ == "__main__":
    restaurant_graph = load_graph("filtered_restaurant_dt_4d.csv")
    quit_game = False

    print("Welcome!This is the restaurant recommender FOODER. \n")

    all_users = AllUsers()
    while not quit_game:
        user_input = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')
        read_inputs(read_lines, user_input)
        user = User(user_input)
        if user not in all_users.list_of_users:
            all_users.list_of_users.append(user)
            print(f"Welcome to FOODER, {user_input}!")
        else:
            print(f"Welcome back to FOODER, {user_input}! We are confident to find you a "
                  f"matching restaurant this time, too!")

        # category, price range, max distance acceptable
        first_filter = []
        user_input = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')
        read_inputs(read_lines, user_input)
        first_filter.append(user_input)

        user_input = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')
        read_inputs(read_lines, user_input)
        first_filter.append(user_input)

        user_input = read_latest_input_from_csv(read_lines, 'data/user_inputs.csv')
        read_inputs(read_lines, user_input)
        first_filter.append(user_input)













    print('Congratulations! You\'ve find your restaurant match! We hope can enjoy the food there!')
    print(f'Your final choice: {lst_of_rest[index]}' + '\n')
    print(f'The the address of the restaurant: {address}')





    
    
