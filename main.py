"""
CSC111 Project 2: Food Recommender

Module Description
==================
This the main file of our project.

===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
from recommender import CategoryGraph

if __name__ == "__main__":
    g = CategoryGraph()
    graph = CategoryGraph.load_graph(g, "filtered_restaurant_dt.csv")

    print("Welcome!This is the food recommender FOODER. ")

    lst_of_rest = CategoryGraph.run_recommender(graph)
    rate_so_far = []
    ans = 0
    index = 0
    while ans == 0 and index < len(lst_of_rest):
        if index == 0:
            print(f'Based on your answers, this is the restaurant we recommend: {lst_of_rest[index]}')
        else:
            print('Sorry to hear that you didn\'t like the restaurant, here is another restaurant '
                  f'that satisfied your request: {lst_of_rest[index]}')
        print('Are you satisfied with this result?')
        ans = input('Y/N (Type N to get another recommendation): ')
        if ans.lower() == 'y':
            ans = 1
        else:
            ans = 0
        rate_so_far.append(ans)
        index += 1

    if index == len(lst_of_rest) - 1:
        print('Sorry, we run out of the restaurants that matches with your request. You can try with'
              'a different choice.')

    address = CategoryGraph.get_rest_address(graph, lst_of_rest[index])

    print('congratulations! You\'ve find your restaurant match! We hope can enjoy the food there!')
    print(f'Your final choice: {lst_of_rest[index]}' + '\n')
    print(f'The the address of the restaurant: {address}')

    CategoryGraph.rating(graph, lst_of_rest, rate_so_far)
