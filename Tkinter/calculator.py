from tkinter import *

root = Tk()
root.title("Simple Calculator")

e = Entry(root, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

color_dict = {
    "number": "#90ee90",  # light green
    "operation": "#add8e6",  # light blue
    "equal": "#f08080",  # light coral
    "clear": "#ffdead",  # navajo white
    "decimal": "#d3d3d3"  # light gray
}


def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, current + str(number))


def button_clear():
    e.delete(0, END)


def button_add():
    first_number = e.get()
    global f_num
    global math
    math = "addition"
    f_num = float(first_number)
    e.delete(0, END)


def button_equal():
    second_number = e.get()
    e.delete(0, END)
    result = None
    try:
        if math == "addition":
            result = f_num + float(second_number)
        if math == "subtraction":
            result = f_num - float(second_number)
        if math == "multiplication":
            result = f_num * float(second_number)
        if math == "division":
            result = f_num / float(second_number)
    except Exception as ex:
        print("An error occurred: ", ex)
        result = "Error"
    try:
        e.insert(0, result)
    except Exception as ex:
        print("An error occurred while trying to display the result: ", ex)


def button_subtract():
    first_number = e.get()
    global f_num
    global math
    math = "subtraction"
    f_num = float(first_number)
    e.delete(0, END)


def button_multiply():
    first_number = e.get()
    global f_num
    global math
    math = "multiplication"
    f_num = float(first_number)
    e.delete(0, END)


def button_divide():
    first_number = e.get()
    global f_num
    global math
    math = "division"
    f_num = float(first_number)
    e.delete(0, END)


button_1 = Button(root, text="1", padx=40, pady=20, command=lambda: button_click(1), bg=color_dict["number"])
button_2 = Button(root, text="2", padx=40, pady=20, command=lambda: button_click(2), bg=color_dict["number"])
button_3 = Button(root, text="3", padx=40, pady=20, command=lambda: button_click(3), bg=color_dict["number"])
button_4 = Button(root, text="4", padx=40, pady=20, command=lambda: button_click(4), bg=color_dict["number"])
button_5 = Button(root, text="5", padx=40, pady=20, command=lambda: button_click(5), bg=color_dict["number"])
button_6 = Button(root, text="6", padx=40, pady=20, command=lambda: button_click(6), bg=color_dict["number"])
button_7 = Button(root, text="7", padx=40, pady=20, command=lambda: button_click(7), bg=color_dict["number"])
button_8 = Button(root, text="8", padx=40, pady=20, command=lambda: button_click(8), bg=color_dict["number"])
button_9 = Button(root, text="9", padx=40, pady=20, command=lambda: button_click(9), bg=color_dict["number"])
button_0 = Button(root, text="0", padx=40, pady=20, command=lambda: button_click(0), bg=color_dict["number"])
button_add = Button(root, text="+", padx=39, pady=20, command=button_add, bg=color_dict["operation"])
button_equal = Button(root, text="=", padx=41, pady=20, command=button_equal, bg=color_dict["equal"])
button_clear = Button(root, text="Clear", padx=79, pady=20, command=button_clear, bg=color_dict["clear"])
button_deci = Button(root, text=".", padx=40, pady=20, command=lambda: button_click("."), bg=color_dict["decimal"])
button_subtract = Button(root, text="-", padx=41, pady=20, command=button_subtract, bg=color_dict["operation"])
button_multiply = Button(root, text="*", padx=40, pady=20, command=button_multiply, bg=color_dict["operation"])
button_divide = Button(root, text="/", padx=41, pady=20, command=button_divide, bg=color_dict["operation"])

button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)

button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)

button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)

button_0.grid(row=4, column=0)
button_clear.grid(row=4, column=1, columnspan=2)
button_add.grid(row=5, column=0)
button_deci.grid(row=5, column=1)
button_equal.grid(row=5, column=2)

button_subtract.grid(row=6, column=0)
button_multiply.grid(row=6, column=1)
button_divide.grid(row=6, column=2)

root.mainloop()
