from tkinter import Tk, Button, Label, Frame, filedialog, Entry, PhotoImage
from PIL import Image, ImageTk, ImageDraw, ImageFont




class ImageWatermarkingDesktopApp:
    def __init__(self) -> None:
        self.root: Tk = Tk()
        self.root.title("Image Watermarking Desktop")
        self.root.geometry("700x650")

        self.img_size: tuple[int, int] = (500, 300)  # preview size
        self.default_font_ui: tuple[str, int] = ("Arial", 12)
        self.default_img_path: str = "sayHelloHalloween.png"

        # PIL image you edit on; and a TK image for preview
        self.base_image = None            # type: Image.Image | None
        self.preview_tk = None            # type: PhotoImage | None

        # Text Entry storage
        self.text_entry = None            # type: Entry | None

        # Try to load a truetype font; fallback to default if missing
        try:
            self.draw_font = ImageFont.truetype("comicbd.ttf", 24)
        except Exception:
            self.draw_font = ImageFont.load_default()

        self.main_frame: Frame = Frame(self.root, padx=10, pady=10)
        self.main_frame.grid(sticky="n")

        self.img_label: Label | None = None
        self.setup_ui()

        # Load a default image if it exists
        try:
            self.load_image(self.default_img_path)
            self.update_preview()
        except Exception:
            pass  # no default image is fine

        self.root.mainloop()

    # ---------- UI ----------
    def setup_ui(self) -> None:
        # Preview area
        self.img_label = Label(self.main_frame, text="No image loaded")
        self.img_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        # Load button
        Label(self.main_frame, text="Upload your picture", font=self.default_font_ui)\
            .grid(column=0, row=1, sticky="w", pady=4)
        Button(self.main_frame, text="Open", font=self.default_font_ui, command=self.open_file)\
            .grid(column=1, row=1, sticky="w", pady=4)

        # Text watermark input
        Label(self.main_frame, text="Watermark text:", font=self.default_font_ui)\
            .grid(column=0, row=2, sticky="w", pady=4)
        self.text_entry = Entry(self.main_frame, width=30, font=self.default_font_ui)
        self.text_entry.grid(row=2, column=1, columnspan=3, sticky="w", pady=4)

        # Apply + Save
        Button(self.main_frame, text="Apply Watermark", font=self.default_font_ui,
               command=self.apply_watermark).grid(row=3, column=0, pady=(10, 0), sticky="w")
        Button(self.main_frame, text="Save As…", font=self.default_font_ui,
               command=self.save_as).grid(row=3, column=1, pady=(10, 0), sticky="w")

    # ---------- Image helpers ----------
    def load_image(self, path: str) -> None:
        """Load original PIL image (for editing) and make a preview TK image."""
        self.base_image = Image.open(path).convert("RGBA")  # keep alpha
        # preview copy
        preview = self.base_image.copy()
        preview.thumbnail(self.img_size)
        self.preview_tk = ImageTk.PhotoImage(preview)

    def update_preview(self) -> None:
        """Refresh the preview label with current self.preview_tk."""
        if self.preview_tk and self.img_label:
            self.img_label.config(image=self.preview_tk, text="")
            self.img_label.image = self.preview_tk  # keep reference

    # ---------- Actions ----------
    def open_file(self) -> None:
        file_path: str = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[('Image Files', '*.png *.jpg *.jpeg *.gif *.bmp *.tiff')]
        )
        if not file_path:
            return
        self.load_image(file_path)
        self.update_preview()

    def apply_watermark(self) -> None:
        """Draw the text on a copy of base_image and update the preview."""
        if self.base_image is None:
            return

        text = (self.text_entry.get() if self.text_entry else "").strip()
        if not text:
            return

        # Work on a copy to keep base_image clean
        working = self.base_image.copy()
        draw = ImageDraw.Draw(working)

        # Simple bottom-right placement with margin
        margin: int = 24
        # Measure text
        bbox: tuple[float, float, float, float] = draw.textbbox((0, 0), text, font=self.draw_font)
        text_w: float = bbox[2] - bbox[0]
        text_h: float = bbox[3] - bbox[1]

        x: float = working.size[0] - text_w - margin
        y: float = working.size[1] - text_h - margin

        # Semi-transparent white text
        draw.text((x, y), text, font=self.draw_font, fill=(255, 255, 255, 180))

        # Refresh preview from watermarked image
        preview = working.copy()
        preview.thumbnail(self.img_size)
        self.preview_tk = ImageTk.PhotoImage(preview)
        self.update_preview()

        # Keep the edited image around for saving
        self.base_image = working

    def save_as(self) -> None:
        if self.base_image is None:
            return
        path: str = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg"), ("All Files", "*.*")]
        )
        if not path:
            return
        # Convert to RGB if user chose jpg
        if path.lower().endswith((".jpg", ".jpeg")):
            self.base_image.convert("RGB").save(path, quality=95)
        else:
            self.base_image.save(path)
        # (Optionally) show a small confirmation message, e.g., a label or messagebox
        # messagebox.showinfo("Saved", f"Image saved to:\n{path}")

if __name__ == "__main__":
    app = ImageWatermarkingDesktopApp()
