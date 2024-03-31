"""
CSC111 Project 2: Food Recommender

Module Description
==================
This module contains the mainfunction of our UI.

===============================

This file is Copyright (c) Kathleen Wang, Jiner Zhang, Kimberly Fu, and Yanting Fan.
"""
# from prompt_toolkit import prompt

import tkinter as tk
from tkinter import simpledialog, messagebox


def save_input():
    """
    save user input in 'user_input.txt'
    """

    with open("user_input.txt", "w") as file:
        for i in range(1, 4):
            file.write(get_user_input(i))


def get_user_input(n: int) -> str:
    """
    get user inputs
    """
    while True:
        user_input = simpledialog.askstring("Input", f"Enter your input{n}:") + '\n'
        if user_input == '\n':
            messagebox.showwarning("Warning", "Input cannot be empty. Please enter your input.")
        else:
            messagebox.showinfo("Success", f"Input{n} saved successfully!")
            break
    return user_input


def main():
    """
    main function
    """
    root = tk.Tk()
    root.title("Please input your preference!")

    button = tk.Button(root, text="Enter Input", command=save_input)
    button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()
