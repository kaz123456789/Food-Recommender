"""
CSC111 Project 2: Food Recommender - FOODER

Module Description
==================
This the main file of our project.

===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from recommender_4d_ver import CategoryGraph, load_graph, get_user_input, get_location_from_ip

if __name__ == "__main__":
    restaurant_graph = load_graph("filtered_restaurant_dt_4d.csv")

    print("Welcome!This is the restaurant recommender FOODER. \n")

    user_name = input("Pleaser enter your name: \n")




    address = CategoryGraph.get_rest_address(graph, lst_of_rest[index])

    print('congratulations! You\'ve find your restaurant match! We hope can enjoy the food there!')
    print(f'Your final choice: {lst_of_rest[index]}' + '\n')
    print(f'The the address of the restaurant: {address}')

    CategoryGraph.rating(graph, lst_of_rest, rate_so_far)




    
    
