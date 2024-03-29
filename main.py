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
    graph = CategoryGraph.load_graph(g, "filtered_restaurant_full.csv")
