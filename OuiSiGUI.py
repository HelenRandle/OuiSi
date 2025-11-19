import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

root = tk.Tk()
root.title("OuiSi!")
box = Image.open("box.png")  
box = ImageTk.PhotoImage(box)
cardDeck = range(1,210)
cardDeck = np.random.shuffle(cardDeck)

for row in range(6):
    filepath = "../ouisi-nature-"+str(0)*3-len(str(cardDeck[0]))+str(cardDeck[0])
    img = Image.open(filepath)
    img = ImageTk.PhotoImage(img)
    cardDeck.pop()  
    
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
