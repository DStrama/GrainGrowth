import tkinter as tk
from tkinter import ttk
from grid import Grid
import numpy as np


class Gui(tk.Tk):
    grid = None
    rows = None
    columns = None
    bc = None
    neighborhood = None
    grain = None
    nucleation = None
    radius = None
    iteration = None

    def __init__(self):

        tk.Tk.__init__(self)
        self.canvas = tk.Canvas(self, width=1150, height=1000)
        self.canvas.pack()

        self.label = tk.Label(self, text="Width:")
        self.label.place(x=20, y=5)

        self.entry_width = tk.Entry(self, width=5)
        self.entry_width.place(x=20, y=30)

        self.label = tk.Label(self, text="Height:")
        self.label.place(x=100, y=5)

        self.entry_height = tk.Entry(self, width=5)
        self.entry_height.place(x=100, y=30)

        self.label = tk.Label(self, text="Grain nucleation:")
        self.label.place(x=180, y=5)

        self.combobox_nucleation = ttk.Combobox(self, values=["Homogenous",
                                                              "In range",
                                                              "Manual choose",
                                                              "Random"
                                                              ], state="readonly")
        self.combobox_nucleation.place(x=180, y=30)

        self.label = tk.Label(self, text="Neighborhood:")
        self.label.place(x=420, y=5)

        self.combobox_neighborhood = ttk.Combobox(self, values=["Moore",
                                                                "Von Neumann",
                                                                "Pentagonal random",
                                                                "Hexagonal random",
                                                                "Hexagonal right",
                                                                "Hexagonal left",
                                                                "In radius"
                                                                ], state="readonly")
        self.combobox_neighborhood.place(x=420, y=30)

        self.label = tk.Label(self, text="Number Of Grain:")
        self.label.place(x=670, y=5)

        self.entry_grain = tk.Entry(self, width=15)
        self.entry_grain.place(x=670, y=30)

        self.label = tk.Label(self, text="Boundary Condition:")
        self.label.place(x=850, y=5)

        self.combobox_bc = ttk.Combobox(self, values=["periodic",
                                                      "absorbing",
                                                      ], state="readonly")
        self.combobox_bc.place(x=850, y=30)

        self.button = tk.Button(self, text="Start", command=self.on_button_click)
        self.button.place(x=1080, y=30)

        self.label = tk.Label(self, text="Radius:")
        self.label.place(x=20, y=70)

        self.entry_radius = tk.Entry(self, width=15)
        self.entry_radius.place(x=20, y=95)

    def printing(self, value_x1, value_x2, value_y1, value_y2, rows, columns):
        x1 = value_x1
        x2 = value_x2
        y1 = value_y1
        y2 = value_y2

        for i in range(rows):
            for j in range(columns):
                if self.grid.grid[i][j].state:
                    colorval = "#%02x%02x%02x" % self.grid.grid[i][j].color
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=colorval)
                else:
                    white = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
                    self.canvas.tag_bind(white, "<ButtonPress-1>",
                                         lambda event, arg_one=i, arg_two=j: self.set_color(event, arg_one, arg_two))
                x1 = x1 + 5
                x2 = x2 + 5
            y1 = y1 + 5
            y2 = y2 + 5
            x1 = value_x1
            x2 = value_x2
        self.canvas.update()

    def set_color(self, event, arg_one, arg_two):
        self.grid.grid[arg_one][arg_two].state = True
        self.grid.number_of_grain += 1
        self.grid.count_grain += 1
        self.grid.grid[arg_one][arg_two].id = self.grid.count_grain
        self.grid.grid[arg_one][arg_two].color = (np.random.randint(255),
                                                  np.random.randint(255),
                                                  np.random.randint(255))
        self.printing(20, 25, 200, 205, self.grid.number_of_columns, self.grid.number_of_rows)

    def how_many_iteration(self, grid):
        x1 = 20
        x2 = 25
        y1 = 200
        y2 = 205
        full = True

        while full:

            number_of_alive = 0
            for i in range(grid.number_of_rows):
                for j in range(grid.number_of_columns):
                    if grid.grid[i][j].state:
                        number_of_alive += 1

            if number_of_alive >= grid.number_of_columns * grid.number_of_rows:
                full = False

            self.printing(x1,
                          x2,
                          y1,
                          y2,
                          grid.number_of_rows,
                          grid.number_of_columns)
            self.grid.caluclate_next_state()

    def on_button_click(self):

        self.columns = int(self.entry_width.get())
        self.rows = int(self.entry_height.get())
        self.bc = self.combobox_bc.get()
        self.neighborhood = self.combobox_neighborhood.get()
        self.grain = int(self.entry_grain.get())
        self.nucleation = self.combobox_nucleation.get()
        if self.entry_radius.get() == '':
            self.radius = 0
        else:
            self.radius = int(self.entry_radius.get())

        self.grid = Grid(self.columns,
                         self.rows,
                         self.combobox_bc.get(),
                         self.combobox_neighborhood.get(),
                         int(self.entry_grain.get()),
                         self.combobox_nucleation.get(),
                         self.radius)

        self.how_many_iteration(self.grid)


gui = Gui()
gui.mainloop()
