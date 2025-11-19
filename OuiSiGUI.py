import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("OuiSi!")
img = Image.open("099.jpg")  
img = ImageTk.PhotoImage(img)
box = Image.open("box.png")  
box = ImageTk.PhotoImage(box)

for row in range(6):
    for col in range(12):
        tk.Button(
                root,
                image=box,
                width=80,
                height=80
        ).grid(row=row, column=col, padx=1, pady=1)

for column in range(0,10,2):
    tk.Button(
        root,
        image=img,
        width=160,
        height=160
    ).grid(row=6, column=column, padx=1, pady=1, columnspan=2, rowspan=2) 


root.mainloop()
