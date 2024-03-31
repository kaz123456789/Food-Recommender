"""
CSC111 Project 2: Food Recommender - FOODER

Module Description
==================
This the main file of our project.

===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from recommender_4d_ver import CategoryGraph, AllUsers, User, load_graph, get_user_input, get_location_from_ip

if __name__ == "__main__":
    restaurant_graph = load_graph("filtered_restaurant_dt_4d.csv")
    quit_game = False

    print("Welcome!This is the restaurant recommender FOODER. \n")

    all_users = AllUsers()
    while not quit_game:
        user_name = input("Please enter your name: \n")
        user = User(user_name)
        if user not in all_users.list_of_users:
            all_users.list_of_users.append(user)
            print(f"Welcome to FOODER, {user_name}!")
        else:
            print(f"Welcome back to FOODER, {user_name}! We are confident to find you a "
                  f"matching restaurant this time, too!")
        







    print('congratulations! You\'ve find your restaurant match! We hope can enjoy the food there!')
    print(f'Your final choice: {lst_of_rest[index]}' + '\n')
    print(f'The the address of the restaurant: {address}')





    
    
