from tkinter import *

root = Tk()
root.title("Simple Calculator")

e = Entry(root, width=24, borderwidth=6, font=('Arial', 24), justify='right', bg="lightgrey")
e.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


# Functions for calculator operations
def button_add():
    global first_number
    global operation
    first_number = int(e.get())
    operation = "add"
    e.delete(0, END)

def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))

def button_subtract():
    global first_number
    global operation
    first_number = int(e.get())
    operation = "sub"
    e.delete(0, END)

def button_multiply():
    global first_number
    global operation
    first_number = int(e.get())
    operation = "multi"
    e.delete(0, END)

def button_divide():
    global first_number
    global operation
    first_number = int(e.get())
    operation = "divide"
    e.delete(0, END)

def button_clear():
    e.delete(0, END)

def button_equal():
    second_number = e.get()
    e.delete(0, END)
    if operation == "add":
        e.insert(0, first_number + int(second_number))
    if operation == "sub":
        e.insert(0, first_number - int(second_number))
    if operation == "multi":
        e.insert(0, first_number * int(second_number))
    if operation == "divide":
        e.insert(0, first_number / int(second_number))
def button_clrone():
    current = e.get()
    e.delete(0, END)
    e.insert(0, current[:-1])
# Button styling
button_font = ('TimesNewRoman', 18)

# Defining buttons
button_clear = Button(root, text="AC", padx=35, pady=30, command=button_clear, font=button_font, bg="lavender")
button_equal = Button(root, text="=", padx=35, pady=70, command=button_equal, font=button_font, bg="lightblue")
button_add = Button(root, text="+", padx=35, pady=30, command=button_add, font=button_font, bg="lightblue")
button_subtract = Button(root, text="-", padx=37, pady=30, command=button_subtract, font=button_font, bg="lightblue")
button_multiply = Button(root, text="*", padx=37, pady=30, command=button_multiply, font=button_font, bg="lightblue")
button_divide = Button(root, text="/", padx=37, pady=30, command=button_divide, font=button_font, bg="lightblue")
button_clrone = Button(root, text="C", padx=37, pady=30, command=button_clrone, font=button_font, bg="lavender")


button_0 = Button(root, text="0", padx=86, pady=30, command=lambda: button_click(0), font=button_font,fg='maroon')
button_1 = Button(root, text="1", padx=35, pady=30, command=lambda: button_click(1), font=button_font,fg='maroon')
button_2 = Button(root, text="2", padx=35, pady=30, command=lambda: button_click(2), font=button_font,fg='maroon')
button_3 = Button(root, text="3", padx=35, pady=30, command=lambda: button_click(3), font=button_font,fg='maroon')
button_4 = Button(root, text="4", padx=35, pady=30, command=lambda: button_click(4), font=button_font,fg='maroon')
button_5 = Button(root, text="5", padx=35, pady=30, command=lambda: button_click(5), font=button_font,fg='maroon')
button_6 = Button(root, text="6", padx=35, pady=30, command=lambda: button_click(6), font=button_font,fg='maroon')
button_7 = Button(root, text="7", padx=35, pady=30, command=lambda: button_click(7), font=button_font,fg='maroon')
button_8 = Button(root, text="8", padx=35, pady=30, command=lambda: button_click(8), font=button_font,fg='maroon')
button_9 = Button(root, text="9", padx=35, pady=30, command=lambda: button_click(9), font=button_font,fg='maroon')

# Placing buttons on the grid
button_clear.grid(row=1, column=0, sticky="nsew")
button_divide.grid(row=1, column=1, sticky="nsew")
button_multiply.grid(row=1, column=2, sticky="nsew")
button_subtract.grid(row=1, column=3, sticky="nsew")
button_clrone.grid(row=5,column=3,sticky="nsew")

button_7.grid(row=2, column=0, sticky="nsew")
button_8.grid(row=2, column=1, sticky="nsew")
button_9.grid(row=2, column=2, sticky="nsew")
button_add.grid(row=2, column=3, sticky="nsew")

button_4.grid(row=3, column=0, sticky="nsew")
button_5.grid(row=3, column=1, sticky="nsew")
button_6.grid(row=3, column=2, sticky="nsew")
button_equal.grid(row=3, column=3, rowspan=2, sticky="nsew")

button_1.grid(row=4, column=0, sticky="nsew")
button_2.grid(row=4, column=1, sticky="nsew")
button_3.grid(row=4, column=2, sticky="nsew")

button_0.grid(row=5, column=0, columnspan=3, sticky="nsew")


root.mainloop()
