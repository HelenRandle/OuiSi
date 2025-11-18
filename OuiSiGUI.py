import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("OuiSi!")
root.minsize(1920,1080)

img = Image.open("../OuiSiImages/ouisi-nature-099-inaê-guion-6-a.jpg")  
img = ImageTk.PhotoImage(img)
label = tk.Label(root, image=img)
label.pack(expand=True)

root.mainloop()
