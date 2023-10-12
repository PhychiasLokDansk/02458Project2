#!/usr/bin/python
# -*- coding: UTF-8 -*-
import scipy
import numpy as np
import os
import tkinter as tk
import PIL
from PIL import ImageTk
from PIL import Image
from PIL import ImageFilter
import matplotlib.pyplot as plt
from time import time

factor = 2

Image_Path = ".\\Anger"
Save_Path = '.\\saves\\save%5s.txt' % time()


class ImageClass:
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.rate = 0
        self.image = None

    def read(self):
        image = Image.open(self.path)
        image = image.filter(filter=ImageFilter.BLUR)
        image = image.reduce(factor, box=None)
        self.image = image


def images_load(path):
    image_bundle = []
    for file in os.listdir(path):
        path_cur = os.path.join(path, file)
        image_class = ImageClass(path_cur, file)
        image_class.read()
        image_bundle.append(image_class)
    return image_bundle


class RatingApps:
    def __init__(self, master_window, image_bundle, save_path):
        # image bundle define
        self.image_bundle = image_bundle
        self.idx = 1
        self.image_current = image_bundle[0]

        self.save_path = save_path

        self.master_window = master_window
        self.master_window.title("Rating App")

        # create remind
        self.label = tk.Label(self.master_window, text='please rate the pic, it should be between 0 to 10', )
        self.label.grid(column=0, row=0)

        # create and show the picture
        global tk_image
        tk_image = ImageTk.PhotoImage(self.image_current.image)
        self.graph = tk.Label(self.master_window, image=tk_image)
        self.graph.grid(column=0, row=1)

        # create text column

        # create button
        self.refresh_button = tk.Button(self.master_window, text="Confirm", command=self.button_clicked)
        self.refresh_button.grid(column=0, row=3)

        # 创建文本框并绑定"<Return>"事件
        self.text = tk.Entry(self.master_window, width=20)
        self.text.grid(column=0, row=2)
        self.text.bind("<Return>", lambda event: self.button_clicked(event))

    def frame(self):
        # clc
        self.text.delete(0, tk.END)
        self.graph.destroy()
        self.label.destroy()

        # create label
        self.label = tk.Label(self.master_window, text='please rate the pic, it should be between 0 to 10')
        self.label.grid(column=0, row=0)

        # create image
        global tk_image
        tk_image = ImageTk.PhotoImage(self.image_current.image)
        self.graph = tk.Label(self.master_window, image=tk_image)
        self.graph.grid(column=0, row=1)

    def button_clicked(self, event=None):
        # record the rate
        rate_cur = float(self.text.get())
        self.image_current.rate = rate_cur
        print("%d, %s, %.1f" % (self.idx, self.image_current.name, self.image_current.rate))

        # write the rate
        save = open(self.save_path, "a")
        save.write("%d, %s, %.1f\n" % (self.idx, self.image_current.path, self.image_current.rate))
        save.close()
        # refresh the window
        self.frame()

        # refresh the index
        self.idx += 1
        self.image_current = self.image_bundle[self.idx]


if __name__ == '__main__':
    Save = open(Save_Path, "w")
    Save.close()
    Image_Bundle = images_load(Image_Path)
    App_Window = tk.Tk()
    Rate_App = RatingApps(App_Window, Image_Bundle, Save_Path)
    App_Window.mainloop()
