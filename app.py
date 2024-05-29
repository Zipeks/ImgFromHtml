import os
import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import filedialog

anime = "onepiece.txt"

# TO DO
# Select default file save location


class GUI:
    def __init__(self) -> None:
        self.window = tk.Tk()

        self.window.title("Down Img from HTML")
        self.window.geometry("750x750")

        self.download_frame = tk.Frame(self.window)
        self.download_frame.pack(side="top", pady=10, padx=5)

        self.html_text = tk.Text(self.download_frame, height=10, width=50)
        self.html_text.grid(row=0, padx=5)

        self.buttons_frame = tk.Frame(self.download_frame)
        self.buttons_frame.grid(row=0, column=1)

        self.save_location = os.getcwd()

        self.save_location_Btn = tk.Button(
            self.buttons_frame,
            text=f"Download directory: {self.save_location}",
            command=self.change_save_location,
        )

        self.save_location_Btn.grid(row=0)

        self.download_button = tk.Button(self.buttons_frame, text="Download")
        self.download_button.grid(row=1, column=0, pady=5)
        self.window.mainloop()

    def change_save_location(self):
        self.save_location = filedialog.askdirectory(
            parent=self.window,
            initialdir=self.save_location,
            title="Select where to save files",
        )
        self.save_location_Btn.config(text=f"Download to: {self.save_location}")

    def extract_image_urls(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        img_tags = soup.find_all("img")
        img_urls = [img["src"] for img in img_tags]
        return img_urls

    # Function to download images given their URLs
    def download_images(self, img_urls, output_folder):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for i, img_url in enumerate(img_urls):
            response = requests.get(img_url, verify=False)
            if response.status_code == 200:
                with open(
                    os.path.join(output_folder, f"{filePrefix}_{chapter}_{i+1}.jpg"),
                    "wb",
                ) as img_file:
                    img_file.write(response.content)
                    print(f"Downloaded {filePrefix}_{chapter}_{i+1}.jpg")
            else:
                print(f"Failed to download {img_url}")

        # Read the HTML text from the file
        file_path = "ToExtractUrl.txt"  # Replace 'your_input_file.txt' with the path to your input file
        with open(file_path, "r", encoding="utf8") as file:
            html_text = re.sub(r"<noscript>.*?</noscript>", "", file.read())

        # Extract image URLs
        image_urls = self.extract_image_urls(html_text)

        # Download images to a folder
        with open(anime, "r") as f:
            output_folder = (
                f.readline().rstrip()
            )  # Replace 'downloaded_images' with your desired output folder name
            filePrefix = f.readline().rstrip()
            chapter = f.readline().rstrip()

        self.download_images(image_urls, output_folder)

        lines = []

        with open(anime, "r") as f:
            lines = f.readlines()[:-1]
            lines.append(f"{int(chapter) + 1}")
        with open(anime, "w") as f:
            f.writelines(lines)


window = GUI()
