from tkinter import Tk, Frame, Label, Button, Entry
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

FONT: tuple[str, int] = ("Arial", 12)


root: Tk = Tk()
root.title("Image Watermarking Desktop App")
root.geometry("500x500")
main_fram: Frame = Frame(root)
main_fram.grid()


Label(main_fram, text="Add you text for picture: ", font=FONT).grid(column=0, row=3)
Entry(main_fram).grid(column=1, row=3)
Button(main_fram, text="Submit", font=FONT).grid(column=2, row=3)
root.mainloop()