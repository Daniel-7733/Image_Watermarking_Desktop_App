from tkinter import Tk, Button, Label, Frame, Button, PhotoImage, filedialog
from tkinter.filedialog import FileDialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


def open_the_file():
    """This function will open file path that let user pick the picture"""
    filedialog.askopenfile(initialdir="",
                           title="Select a File",
                           filetypes=[('Picture Files', '*.png')])


def usable_img(img_route: str, img_size_wl: tuple[int, int]):
    """This function take the raw picture and turn it to usable picture with desired size"""
    raw_img = Image.open(img_route)
    resized_image = raw_img.resize(img_size_wl)
    image = ImageTk.PhotoImage(resized_image)
    return image


if __name__ == "__main__":
    font: tuple[str, int] = ("Ariel", 14)
    img_path: str = "sayHelloHalloween.png"
    img_size: tuple[int, int] = (400, 200)

    root: Tk = Tk()
    root.title("Image Watermarking Desktop")
    root.geometry("600x600")
    main_fram: Frame = Frame(root, padx=10, pady=10)
    main_fram.grid()

    img = usable_img(img_path, img_size)

    Label(main_fram, image=img).grid(row=0, column=0, columnspan=3, rowspan=1)
    Label(main_fram, text="Upload your picture here", font=font).grid(column=0, row=5)
    Button(main_fram, text="Open", font=font, command=open_the_file).grid(column=3, row=5)

    root.mainloop()