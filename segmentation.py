import cv2
import numpy as np
from customtkinter import *
from PIL import Image, ImageTk

set_appearance_mode("system")
set_default_color_theme("green")


class ImageProcessing:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing")

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

        # Create IntVar for slider value
        self.threshold_value_var = IntVar(value=127)
        self.add_slider("Threshold", 0, 255, 127, self.update_thresholding_segmentation)

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
        self.image_label.image = img

    def add_button(self, text, command):
        button = CTkButton(
            master=self.button_frame, text=text, command=command, width=200
        )
        button.pack(pady=6)

    def add_buttons_and_sliders(self):
        # Region Split and Merge Segmentation
        self.add_button(
            "Apply Region Split Merge Segmentation",
            self.apply_region_split_merge_segmentation,
        )

    def add_slider(self, name, min_val, max_val, default_val, command):
        label = CTkLabel(self.button_frame, text=f"{name}: {default_val}")
        label.pack()

        slider = CTkSlider(
            self.button_frame,
            from_=min_val,
            to=max_val,
            command=command,
            variable=self.threshold_value_var,
            orientation=HORIZONTAL,
        )
        slider.set(default_val)
        slider.pack()
        return slider

    def apply_region_split_merge_segmentation(self):
        region_split_merge_image = self.original_image.copy()
        height, width = region_split_merge_image.shape[:2]

        def region_growing(image, seed):
            visited = set()
            stack = [seed]

            while stack:
                x, y = stack.pop()
                if (x, y) not in visited:
                    visited.add((x, y))
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                if abs(int(image[y, x]) - int(image[ny, nx])) < 20:
                                    stack.append((nx, ny))

            return visited

        def merge_regions(visited_regions):
            new_regions = []
            for region in visited_regions:
                merged_region = region.copy()
                while True:
                    for other_region in visited_regions:
                        if other_region != region and not set(region).isdisjoint(
                            other_region
                        ):
                            merged_region.update(other_region)
                            visited_regions.remove(other_region)
                            break
                    else:
                        break
                new_regions.append(merged_region)
            return new_regions

        seeds = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1)]

        visited_regions = []
        for seed in seeds:
            visited_region = region_growing(region_split_merge_image, seed)
            visited_regions.append(visited_region)

        merged_regions = merge_regions(visited_regions)

        for region in merged_regions:
            for x, y in region:
                region_split_merge_image[y, x] = 255

        self.update_image(region_split_merge_image)

    def update_thresholding_segmentation(self, event):
        threshold_value = int(event.widget.get())
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        _, threshold_image = cv2.threshold(
            gray_image, threshold_value, 255, cv2.THRESH_BINARY
        )
        self.update_image(cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR))


root = CTk()
root.geometry("800x600")
root.resizable(width=False, height=False)
root.title("Image Processing App")
APP = ImageProcessing(root)
root.mainloop()
