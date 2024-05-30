import os
import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import filedialog, messagebox

anime = "onepiece.txt"

# TO DO
# Select default file save location


class GUI:
    def __init__(self) -> None:
        self.window = tk.Tk()

        self.window.title("Down Img from HTML")
        self.window.geometry("750x250")

        self.download_frame = tk.Frame(self.window)
        self.download_frame.pack(side="top", pady=20, padx=5)

        self.html_text = tk.Text(self.download_frame, height=10, width=40)
        self.html_text.grid(row=0, padx=5)

        self.buttons_frame = tk.Frame(self.download_frame)
        self.buttons_frame.grid(row=0, column=1)

        self.save_location_frame = tk.Frame(self.buttons_frame)
        self.save_location_frame.grid(row=0)

        self.save_location = os.getcwd()

        self.down_label = tk.Label(self.save_location_frame, text="Download to:")
        self.down_label.pack(side="top")

        self.save_location_Btn = tk.Button(
            self.save_location_frame,
            text=f"{self.save_location}",
            command=self.change_save_location,
        )

        self.save_location_Btn.pack(side="top")

        self.naming_frame = tk.Frame(self.buttons_frame)
        self.naming_frame.grid(row=1)

        self.names_label = tk.Label(self.naming_frame, text="Naming convention:")
        self.names_label.grid(row=0, column=0)

        self.names_input = tk.Entry(self.naming_frame)
        self.names_input.grid(row=0, column=1)

        self.download_button = tk.Button(
            self.buttons_frame, text="Download", command=self.download_images
        )
        self.download_button.grid(row=2, column=0, pady=5)
        self.window.mainloop()

    def change_save_location(self):
        self.save_location = filedialog.askdirectory(
            parent=self.window,
            initialdir=self.save_location,
            title="Select where to save files",
        )
        self.save_location_Btn.config(text=f"{self.save_location}")

    def extract_image_urls(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        img_tags = soup.find_all("img")
        img_urls = [img["src"] for img in img_tags]
        return img_urls

    def download_images(self):
        html_text = self.html_text.get("1.0", tk.END)
        img_urls = self.extract_image_urls(html_text)

        output_folder = self.save_location
        names = self.names_input.get()

        for i, img_url in enumerate(img_urls):
            response = requests.get(img_url, verify=False)
            if response.status_code == 200:
                with open(
                    os.path.join(output_folder, f"{names}_{i+1}.jpg"),
                    "wb",
                ) as img_file:
                    img_file.write(response.content)
                    print(f"Downloaded {names}_{i+1}.jpg")
            else:
                messagebox.showerror(
                    "Something went wrong", f"Failed to download {img_url}"
                )

        messagebox.showinfo("Success", f"Downloaded {i+1} files")


window = GUI()
