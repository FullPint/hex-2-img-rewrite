# Standard Library Imports
from glob import glob
import os
import re

# Package Imprts
import numpy as np
import cv2 as cv
from toolz.itertoolz import partition_all

# User Defined Imports

# User Defined VARS
DEFAULT_WIDTHS = {
    9: 32,
    29: 64,
    59: 128,
    99: 256,
    199: 384,
    499: 512,
    999: 768,
    1024: 1024,
}


def get_hex_vector(hex_file_path):
    hex_vector = []
    with open(hex_file_path) as f:
        for line in f:
            if "?" not in line:
                hex_vector.extend(get_clean_hex_list(line))
    return hex_vector


def get_clean_hex_list(hex_list):
    address_index = 8
    return [
        char
        for char in hex_list
        if (char != " " and char != "\t" and char != "\n")
    ][address_index:]


def get_base_ten_vector(hex_vector):
    dec_vector = []
    for pair in partition_all(2, hex_vector):
        dec_vector.append(int("".join(pair), 16))
    return dec_vector


def get_width_from_dict(file_size, widths_opts=DEFAULT_WIDTHS):
    width = max(widths_opts, key=int)
    for key in DEFAULT_WIDTHS:
        if file_size <= key:
            return widths_opts[key]
    return width


def pad_vector(vector, width):
    vector.extend([0] * (width - (len(vector) % width)))
    return vector


def get_2D_decimal_from_hex_file(hex_file_path):
    dec_vector = get_base_ten_vector(get_hex_vector(hex_file_path))
    width = get_width_from_dict(int(len(dec_vector) * 0.001))
    padded_vector = pad_vector(dec_vector, width)
    height = int(len(padded_vector) / width)
    return np.array(padded_vector, dtype=np.float32).reshape((height, width))


def get_image_path(hex_file_path):
    return os.path.splitext(hex_file_path)[0] + ".png"


def directory_to_images(samples_dir):
    for hex_file_path in glob(samples_dir):
        cv.imwrite(
            get_image_path(hex_file_path),
            get_2D_decimal_from_hex_file(hex_file_path),
        )
