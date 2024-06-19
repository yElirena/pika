#!/usr/bin/python3
import os
from PIL import Image


def convert_png_to_bmp(source_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith(".png"):
            with Image.open(os.path.join(source_folder, filename)) as img:
                bmp_filename = os.path.splitext(filename)[0] + ".bmp"
                bmp_path = os.path.join(dest_folder, bmp_filename)
                img.save(bmp_path)
                print(f"Converted {filename} to {bmp_filename}")


source_folder = "/home/fuse/cloud/CBM/Java/Java_3Pojeckt/"
dest_folder = "/home/fuse/NAS/pic/"

convert_png_to_bmp(source_folder, dest_folder)
