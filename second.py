import cv2
import numpy as np
from customtkinter import *
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox

set_appearance_mode("system")
set_default_color_theme("green")


class ImageProcessing:
    def __init__(self, master):
        self.master = master
        self.master.title(" FEE Image")

        self.image_frame = CTkFrame(master)
        self.image_frame.pack(side=RIGHT, padx=10, pady=10)

        self.button_frame = CTkFrame(master)
        self.button_frame.pack(side=LEFT, padx=10, pady=10)

        self.image_label = CTkLabel(self.image_frame, width=420, height=420)
        self.image_label.pack(padx=10, pady=10)

        self.load_image_button = CTkButton(
            master=self.button_frame, text="Load Image", command=self.load_default_image
        )
        self.load_image_button.pack(pady=6)
        self.add_buttons_and_sliders()

    def load_default_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg; *.jpeg; *.png; *.bmp")]
        )
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.update_image(self.original_image)

    def update_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((320, 320))
        img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img, text="")
        self.image_label.pack()

    def add_buttons_and_sliders(self):
        self.add_button("Apply Roberts Edge Detector", self.apply_roberts)

        self.add_button("Apply Prewitt Edge Detector", self.apply_prewitt)

        self.add_button("Apply Solbel Edge Detector", self.apply_solbel)

    def add_button(self, text, command):
        button = CTkButton(
            master=self.button_frame, text=text, command=command, width=230
        )
        button.pack(pady=10)

    def apply_roberts(self):
        roberts_image = cv2.Canny(self.original_image, 100, 200)
        self.update_image(roberts_image)

    def apply_prewitt(self):
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        prewitt_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        prewitt_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        prewitt_image = np.sqrt(prewitt_x**2 + prewitt_y**2)
        prewitt_image = cv2.normalize(
            prewitt_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )
        self.update_image(prewitt_image)

    def apply_solbel(self):
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        sobel_image = np.sqrt(sobel_x**2 + sobel_y**2)
        sobel_image = cv2.normalize(
            sobel_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )
        self.update_image(sobel_image)


root = CTk()
root.geometry("800x600")
root.resizable(width=False, height=False)
root.title("Image Processing App")
APP = ImageProcessing(root)
root.mainloop()
