import cv2
from customtkinter import *
from PIL import Image, ImageTk
import numpy as np

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
        self.add_buttons_andsliders()

        # Create IntVar for slider value
        self.close_kernel_size_var = IntVar(value=5)
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

    def add_buttons_andsliders(self):
        # Hough Circle
        self.add_button("Apply Hough Circle Transform", self.apply_hough_circle)

    def add_button(self, text, command):
        button = CTkButton(
            master=self.button_frame, text=text, command=command, width=100
        )
        button.pack(pady=10)

    def apply_hough_circle(self):
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(
            gray_image,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=20,
            param1=50,
            param2=30,
            minRadius=0,
            maxRadius=0,
        )
        if circles is not None:
            circles = np.uint16(np.around(circles))
            hough_image = self.original_image.copy()
            for i in circles[0, :]:
                cv2.circle(hough_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(hough_image, (i[0], i[1]), 2, (0, 0, 255), 3)
            self.update_image(hough_image)

    def add_buttons_and_sliders(self):
        # Close:
        self.close_slider_label = CTkLabel(
            self.button_frame,
            text=f"Close Kernel Size: {self.close_kernel_size_var.get()}",
        )
        self.close_slider_label.pack()

        self.close_slider = CTkSlider(
            self.button_frame,
            from_=1,
            to=20,
            command=self.update_close_slider_label,
            variable=self.close_kernel_size_var,
            orientation=HORIZONTAL,
        )
        self.close_slider.set(5)
        self.close_slider.pack()
        self.add_button(text="Apply Close", command=self.apply_close)

    def update_close_slider_label(self, event):
        self.close_slider_label.configure(
            text=f"Close Kernel Size: {self.close_kernel_size_var.get()}"
        )

    def apply_close(self):
        kernel_size = int(self.close_kernel_size_var.get())
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        close_image = cv2.morphologyEx(self.original_image, cv2.MORPH_CLOSE, kernel)
        self.update_image(close_image)


root = CTk()
root.geometry("800x600")
root.resizable(width=False, height=False)
root.title("Image Processing App")
APP = ImageProcessing(root)
root.mainloop()
