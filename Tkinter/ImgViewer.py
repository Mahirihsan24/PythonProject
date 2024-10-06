from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Image Viewer")

# Load images
img1 = Image.open('wp9606137-jujutsu-kaisen-desktop-hd-wallpapers.jpg')
img1 = img1.resize((420,420))
my_img1 = ImageTk.PhotoImage(img1)

img2 = Image.open('wp8799159-jujutsu-kaisen-computer-wallpapers.jpg')
img2 = img2.resize((420,420))
my_img2 = ImageTk.PhotoImage(img2)

img3 = Image.open("wp9242291-gojo-saturu-wallpapers.jpg")
img3 = img3.resize((420,420))
my_img3 = ImageTk.PhotoImage(img3)

img4 = Image.open('wp8369541-sukuna-ryomen-desktop-wallpapers.jpg')
img4 = img4.resize((420,420))
my_img4 = ImageTk.PhotoImage(img4)

img5 = Image.open('wp9583412-gojo-4k-wallpapers.jpg')
img5 = img5.resize((420,420))
my_img5 = ImageTk.PhotoImage(img5)

img6 = Image.open('wp9273580-jujutsu-kaisen-4k-pc-wallpapers.jpg')
img6 = img6.resize((420,420))
my_img6 = ImageTk.PhotoImage(img6)

my_list = [my_img1, my_img2, my_img3, my_img4, my_img5, my_img6]

status = Label(root, text="Image 1 of " + str(len(my_list)), bd=1, relief=SUNKEN)
status.grid(row=2, column=0, columnspan=3, sticky=W+E)

my_label = Label(image = my_img1)
my_label.grid(row=0, column=0, columnspan=3)

img_num = 0

def forward():
    global my_label
    global img_num
    global button_forward
    global button_back

    img_num = (img_num + 1) % len(my_list)

    my_label.grid_forget()
    my_label = Label(image = my_list[img_num])
    my_label.grid(row=0, column=0, columnspan=3)

    button_forward = Button(root, text= ">>", command=forward)
    button_back = Button(root, text="<<", command=back)

    if img_num == len(my_list) - 1:
        button_forward = Button(root, text=">>", state=DISABLED)

    button_forward.grid(row=1, column=2)
    button_back.grid(row=1, column=0)

    status = Label(root, text="Image " + str(img_num + 1) + " of " + str(len(my_list)))
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)

def back():
    global my_label
    global img_num
    global button_forward
    global button_back

    img_num = (img_num - 1) % len(my_list)

    my_label.grid_forget()
    my_label = Label(image = my_list[img_num])
    my_label.grid(row=0, column=0, columnspan=3)

    button_forward = Button(root, text= ">>", command=forward)
    button_back = Button(root, text="<<", command=back)

    if img_num == 0:
        button_back = Button(root, text="<<", state=DISABLED)

    button_forward.grid(row=1, column=2)
    button_back.grid(row=1, column=0)

    status = Label(root, text="Image " + str(img_num + 1) + " of " + str(len(my_list)))
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)

button_back = Button(root, text= "<<", command=back)
button_exit = Button(root, text= "Exit", command=root.quit)
button_forward = Button(root, text= ">>", command=forward)

button_back.grid(row=1, column=0)
button_exit.grid(row=1, column=1)
button_forward.grid(row=1, column=2)

root.mainloop()