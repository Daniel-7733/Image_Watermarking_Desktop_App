from tkinter import Tk, Button, Label, Frame, filedialog, Entry, PhotoImage
from PIL import Image, ImageTk, ImageDraw, ImageFont


class ImageWatermarkingDesktopApp:
    def __init__(self) -> None:
        self.root: Tk = Tk()
        self.root.title("Image Watermarking Desktop")
        self.root.geometry("600x600")

        self.img_size: tuple[int, int] = (400, 200)
        self.default_font: tuple[str, int] = ("Arial", 14)
        self.default_img_path: str = "sayHelloHalloween.png"

        self.main_frame: Frame = Frame(self.root, padx=10, pady=10)
        self.main_frame.grid()

        self.img_label: Label | None = None

        self.setup_ui()
        self.root.mainloop()

    def setup_ui(self) -> None:
        """Set up the GUI components."""
        img = self.load_image(self.default_img_path)
        self.img_label = Label(self.main_frame, image=img)
        self.img_label.image = img  # Keep a reference
        self.img_label.grid(row=0, column=0, columnspan=3, rowspan=1)

        Label(self.main_frame, text="Upload your picture here", font=self.default_font).grid(column=0, row=5)
        Button(self.main_frame, text="Open", font=self.default_font, command=self.open_file).grid(column=3, row=5)
        Label(self.main_frame, text="Add your text", font=self.default_font).grid(column=0, row=6)
        Entry(self.main_frame, width=20, font=self.default_font).grid(row=6, column=1, columnspan=3) # I need to save this text for displaying it on the picture.

    def load_image(self, path) -> PhotoImage:
        """Load and resize image from the given path."""
        raw_img = Image.open(path)
        resized = raw_img.resize(self.img_size)
        return ImageTk.PhotoImage(resized)

    def open_file(self) -> None:
        """Open file dialog and update the image."""
        file_path: str = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[('Picture Files', '*.png *.jpg *.jpeg *.gif')]
        )

        if file_path:
            new_img = self.load_image(file_path)
            self.img_label.config(image=new_img)
            self.img_label.image = new_img  # Keep reference


if __name__ == "__main__":
    app: ImageWatermarkingDesktopApp = ImageWatermarkingDesktopApp()