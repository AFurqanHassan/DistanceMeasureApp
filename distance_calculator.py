import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import math


def get_distance(point1, point2):
    pixel_distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
    resolution = 6  # example resolution in pixels per inch
    cm_per_inch = 2.54
    cm_distance = pixel_distance / resolution * cm_per_inch
    return cm_distance


class DistanceCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Distance Calculator")

        self.canvas = tk.Canvas(master)
        self.canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.point_marker = None
        self.image_tk = None

        self.load_button = tk.Button(master, text="Load Image", command=self.load_image, width=10)
        self.load_button.grid(row=1, column=0, sticky="w")

        self.calculate_button = tk.Button(master, text="Calculate Distance", command=self.calculate_distance, width=15,
                                          state=tk.DISABLED)
        self.calculate_button.grid(row=1, column=1, sticky="e")

        self.reset_button = tk.Button(master, text="Reset", command=self.reset, width=10,
                                      state=tk.DISABLED)
        self.reset_button.grid(row=1, column=2, sticky="e")

        self.distance_label = tk.Label(master, text="Distance: ")
        self.distance_label.grid(row=2, column=0, columnspan=2)

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

    def load_image(self):
        filename = askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if filename:
            self.point_marker = None
            self.image_tk = ImageTk.PhotoImage(Image.open(filename))
            self.canvas.config(width=self.image_tk.width(), height=self.image_tk.height())
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

            self.point_marker = self.PointMarker(self.canvas)

            self.calculate_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def calculate_distance(self):
        if len(self.point_marker.points) < 2:
            return
        point1, point2 = self.point_marker.points[-2:]
        distance = get_distance(point1, point2)
        self.distance_label.config(text="Distance: {:.2f} cm".format(distance))

    class PointMarker:
        def __init__(self, canvas):
            self.canvas = canvas
            self.points = []
            self.current_point = None
            self.dot_size = 5

            self.canvas.bind("<Button-1>", self.on_click)

        def on_click(self, event):
            self.current_point = (event.x, event.y)
            self.draw_dot(self.current_point)

        def draw_dot(self, point):
            x, y = point
            self.canvas.create_oval(x - self.dot_size, y - self.dot_size, x + self.dot_size, y + self.dot_size,
                                    fill="red")
            self.points.append(point)

    def reset(self):
        self.canvas.delete("all")
        self.point_marker = None
        self.image_tk = None
        self.calculate_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.distance_label.config(text="Distance: ")


root = tk.Tk()
app = DistanceCalculator(root)
root.mainloop()
