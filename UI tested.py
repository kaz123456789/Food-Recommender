#scratch 1
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Buttons in Rows")

    # Create a frame for the first row of buttons
    frame1 = tk.Frame(root)
    frame1.pack(side=tk.TOP, padx=10, pady=10)

    # Create and pack buttons in the first row frame
    button1 = tk.Button(frame1, text="Option1!",
                        fg="black", bg="blue",  # Text and background color
                        font=("Times New Roman", 12),  # Font family and size
                        relief=tk.RAISED, bd=3,  # Border style and width
                        padx=20, pady=10,)
    button1.pack(side=tk.LEFT, padx=5, pady=5)

    button2 = tk.Button(frame1, text="Button 2")
    button2.pack(side=tk.LEFT, padx=5, pady=5)

    # Create a frame for the second row of buttons
    frame2 = tk.Frame(root)
    frame2.pack(side=tk.TOP, padx=10, pady=10)

    # Create and pack a button in the second row frame
    button3 = tk.Button(frame2, text="Button 3")
    button3.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

#scratch 2
import tkinter as tk
from tkinter import messagebox

def get_string_and_show_buttons():
    input_text = entry.get()
    messagebox.showinfo("String Input", f"You entered: {input_text}")

    # Clear the input entry
    entry.delete(0, tk.END)

    # Hide the string input widgets
    label.pack_forget()
    entry.pack_forget()
    submit_button.pack_forget()

    # Show the buttons
    button1 = tk.Button(popup, text="Button 1", command=action_button1)
    button2 = tk.Button(popup, text="Button 2", command=action_button2)
    button3 = tk.Button(popup, text="Button 3", command=action_button3)

    # Pack buttons for the button window
    button1.pack(padx=10, pady=5)
    button2.pack(padx=10, pady=5)
    button3.pack(padx=10, pady=5)

def show_popup():
    global popup

    # Create a pop-up window to get string input
    popup = tk.Toplevel(root)
    popup.title("String Input")
    popup.geometry("300x150")

    global label
    label = tk.Label(popup, text="Enter a string:")
    label.pack(pady=5)

    global entry
    entry = tk.Entry(popup)
    entry.pack(pady=5)

    global submit_button
    submit_button = tk.Button(popup, text="Submit", command=get_string_and_show_buttons)
    submit_button.pack(pady=5)

def action_button1():
    messagebox.showinfo("Button 1", "Button 1 was clicked")

def action_button2():
    messagebox.showinfo("Button 2", "Button 2 was clicked")

def action_button3():
    messagebox.showinfo("Button 3", "Button 3 was clicked")

def main():
    global root
    root = tk.Tk()
    root.title("Transition Example")

    # Create a button to show the pop-up window for string input
    popup_button = tk.Button(root, text="Get String Input", command=show_popup)
    popup_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

#scratch 3
import tkinter as tk
from tkinter import simpledialog, messagebox


def append_to_file(text):
    """
    Function to append text to a file
    """
    with open("user_input.txt", "a") as file:
        file.write(text + "\n")


def show_buttons(root, entry, submit_button):
    """
    Function to show the buttons after getting user input
    """
    user_input = entry.get()
    messagebox.showinfo("Input", f"You entered: {user_input}")

    # Clear the input entry
    entry.delete(0, tk.END)

    # Hide the string input widgets
    # label.pack_forget()
    entry.pack_forget()
    submit_button.pack_forget()

    # Show the buttons
    button1 = tk.Button(root, text="Button 1", command=action_button1)
    button2 = tk.Button(root, text="Button 2", command=action_button2)
    button3 = tk.Button(root, text="Button 3", command=action_button3)

    # Pack buttons for the button window
    button1.pack(padx=10, pady=5)
    button2.pack(padx=10, pady=5)
    button3.pack(padx=10, pady=5)


def save_input(root, entry, submit_button):
    """
    Function to get user input and save it in a file
    """
    user_input = simpledialog.askstring("Input", "Enter your Name:")
    if not user_input:
        messagebox.showwarning("Warning", "Input cannot be empty. Please enter your name.")
    else:
        messagebox.showinfo("Success", "Thank you!")
        append_to_file(user_input)
        show_buttons(root, entry, submit_button)


def action_button1():
    """
    append user option (button1) to user_input file
    """
    append_to_file('option1')


def action_button2():
    """
    append user option (button 2) to user_input file
    """
    append_to_file('option2')
    # messagebox.showinfo("Button 2", "Button 2 was clicked")


def action_button3():
    """
    append user option (button 3) to user_input file
    """
    append_to_file('option3')
    # messagebox.showinfo("Button 3", "Button 3 was clicked")


def main():
    """
    Main function
    """
    root = tk.Tk()
    root.minsize(200, 100)  # set the size of pop-up
    root.title("Restaurant Recommender!")

    # label = tk.Label(root, text="Enter your preference:")
    # label.pack(pady=5)

    entry = tk.Entry(root)
    entry.pack(pady=5)

    submit_button = tk.Button(root, text="Begin", command=lambda: save_input(root, entry, submit_button))
    submit_button.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()

#scratch 4
import tkinter as tk
from tkinter import messagebox
import csv


# def record_choice(option):
#     messagebox.showinfo("Choice Recorded", f"You selected {option}")
def append_to_file(text):
    """
    Function to append text to a file
    """
    with open("user_input.txt", "a") as file:
        file.write(text + "\n")


def save_choice(option):
    if option:
        with open("choices.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([option])
        messagebox.showinfo("Choice", f"You selected option {option}")
    else:
        messagebox.showwarning("Warning", "Please select an option.")


def main():
    root = tk.Tk()
    root.title("Customized Window")
    # root.minsize(400, 300)
    # root.maxsize(800, 600)

    # Define the functions to record the choice when the button is clicked
    def option1_selected():
        save_choice("jiner")

    def option2_selected():
        save_choice("fanyanting")

    def option3_selected():
        save_choice("auntie")

    frame1 = tk.Frame(root)
    frame1.pack(side=tk.TOP, padx=10, pady=10)
    # Create buttons for each option

    button1 = tk.Button(frame1, text="Option1!",
                        fg="black", bg="blue",  # Text and background color
                        font=("Times New Roman", 12),  # Font family and size
                        relief=tk.RAISED, bd=3,  # Border style and width
                        padx=20, pady=10,
                        command=option1_selected)
    button1.pack(side=tk.LEFT, padx=5, pady=5)

    button2 = tk.Button(frame1, text="Option 2", command=option2_selected)
    button2.pack(side=tk.LEFT, padx=10, pady=5)

    frame2 = tk.Frame(root)
    frame2.pack(side=tk.TOP, padx=10, pady=10)

    button3 = tk.Button(frame2, text="Option 3", command=option3_selected)
    button3.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()

#scratch 5
import tkinter as tk
from tkinter import simpledialog, messagebox
import csv

def save_choice(var):
    choice = var.get()
    if choice:
        with open("choices.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([choice])
        messagebox.showinfo("Choice", f"You selected option {choice}")
    else:
        messagebox.showwarning("Warning", "Please select an option.")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    var = tk.StringVar()

    # Create a pop-up window
    popup = tk.Toplevel(root)
    popup.title("Options")

    # Add radio buttons for options
    tk.Radiobutton(popup, text="Option 1", variable=var, value="test").pack(anchor=tk.W)
    tk.Radiobutton(popup, text="Option 2", variable=var, value="2").pack(anchor=tk.W)
    tk.Radiobutton(popup, text="Option 3", variable=var, value="3").pack(anchor=tk.W)

    # Add a button to record the choice
    button = tk.Button(popup, text="Record Choice", command=lambda: save_choice(var))
    button.pack(pady=10)

    popup.mainloop()

if __name__ == "__main__":
    main()
