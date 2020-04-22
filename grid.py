from random import random
from cell import Cell
import numpy as np


class Grid:
    number_of_columns = None
    number_of_rows = None
    number_of_grain = None
    growth_type = None
    bc = None
    count_grain = None
    grid = None

    def __init__(self, columns, rows, bc, growth, grains, nucleation_type, radius):
        self.number_of_columns = columns
        self.number_of_rows = rows
        self.number_of_grain = grains
        self.count_grain = 0
        self.bc = bc
        self.growth_type = growth
        self.grid = [[Cell() for j in range(columns)] for i in range(rows)]
        self.choose_nucleation_type(nucleation_type, rows, columns, grains, radius)

    def choose_nucleation_type(self, nucleation, rows, columns, grains, radius):
        if nucleation == 'Homogenous':
            self.grains_homogeneous(rows, columns)
        elif nucleation == 'In range':
            self.grains_radius(grains, radius, rows, columns)
        elif nucleation == 'Random':
            self.grains_random(grains, rows, columns)
        elif nucleation == 'Manual choose':
            return

    def get_neighbour(self, row_index, column_index):
        N = row_index - 1
        E = column_index + 1
        S = row_index + 1
        W = column_index - 1

        if self.growth_type == "Moore":
            return [self.boundary_condition(N, W),
                    self.boundary_condition(N, column_index),
                    self.boundary_condition(N, E),
                    self.boundary_condition(row_index, E),
                    self.boundary_condition(S, E),
                    self.boundary_condition(S, column_index),
                    self.boundary_condition(S, W),
                    self.boundary_condition(row_index, W)]
        elif self.growth_type == "Von Neumann":
            return [self.boundary_condition(N, column_index),
                    self.boundary_condition(row_index, E),
                    self.boundary_condition(S, column_index),
                    self.boundary_condition(row_index, W)]
        elif self.growth_type == "Pentagonal random":
            number = np.random.randint(1, 5)
            if number == 1:
                return [self.boundary_condition(N, W),
                        self.boundary_condition(N, column_index),
                        self.boundary_condition(S, column_index),
                        self.boundary_condition(S, W),
                        self.boundary_condition(row_index, W)
                        ]
            if number == 2:
                return [self.boundary_condition(N, column_index),
                        self.boundary_condition(N, E),
                        self.boundary_condition(row_index, E),
                        self.boundary_condition(S, E),
                        self.boundary_condition(S, column_index)
                        ]
            if number == 3:
                return [self.boundary_condition(row_index, E),
                        self.boundary_condition(S, E),
                        self.boundary_condition(S, column_index),
                        self.boundary_condition(S, W),
                        self.boundary_condition(row_index, W)
                        ]
            if number == 4:
                return [self.boundary_condition(N, W),
                        self.boundary_condition(N, column_index),
                        self.boundary_condition(N, E),
                        self.boundary_condition(row_index, E),
                        self.boundary_condition(row_index, W)
                        ]
        elif self.growth_type == "Hexagonal left":
            return [self.boundary_condition(N, W),
                    self.boundary_condition(N, column_index),
                    self.boundary_condition(row_index, E),
                    self.boundary_condition(S, E),
                    self.boundary_condition(S, column_index),
                    self.boundary_condition(row_index, W)
                    ]
        elif self.growth_type == "Hexagonal right":
            return [self.boundary_condition(N, column_index),
                    self.boundary_condition(N, E),
                    self.boundary_condition(row_index, E),
                    self.boundary_condition(S, column_index),
                    self.boundary_condition(S, W),
                    self.boundary_condition(row_index, W)
                    ]
        elif self.growth_type == "Hexagonal random":
            number = np.random.randint(1, 3)
            if number == 1:
                return [self.boundary_condition(N, column_index),
                        self.boundary_condition(N, E),
                        self.boundary_condition(row_index, E),
                        self.boundary_condition(S, column_index),
                        self.boundary_condition(S, W),
                        self.boundary_condition(row_index, W)
                        ]
            if number == 2:
                return [self.boundary_condition(N, W),
                        self.boundary_condition(N, column_index),
                        self.boundary_condition(row_index, E),
                        self.boundary_condition(S, E),
                        self.boundary_condition(S, column_index),
                        self.boundary_condition(row_index, W)
                        ]

    def boundary_condition(self, row_index, column_index):
        if self.bc == "periodic":
            return self.grid[(row_index + self.number_of_rows) % self.number_of_rows][(column_index + self.number_of_columns) % self.number_of_columns]
        elif self.bc == "absorbing":
            if row_index >= self.number_of_rows or column_index >= self.number_of_columns or row_index < 0 or column_index < 0:
                return Cell()
            else:
                return self.grid[row_index][column_index]

    def grains_homogeneous(self, rows, columns):
        for i in range(1, rows, 3):
            for j in range(1, columns, 3):
                if self.count_grain == self.number_of_grain:
                    return
                self.count_grain += 1
                self.grid[i][j].id = self.count_grain
                self.grid[i][j].state = True
                self.grid[i][j].color = (np.random.randint(255),
                                         np.random.randint(255),
                                         np.random.randint(255))

    def grains_random(self, number_of_grains, rows, columns):
        i = 0
        while i < number_of_grains:
            row = np.random.randint(rows)
            column = np.random.randint(columns)
            if self.grid[row][column].state:
                i = i - 1
            else:
                self.grid[row][column].state = True
                self.grid[row][column].id = i
                self.grid[row][column].color = (np.random.randint(255),
                                                np.random.randint(255),
                                                np.random.randint(255))
                i = i + 1

    def grains_radius(self, number_of_grains, radius, rows, columns):

        i = 0
        while i < number_of_grains:

            row = np.random.randint(rows)
            column = np.random.randint(columns)
            if 0 <= row < rows and 0 <= column < columns and self.grid[row][column].state:
                i = i - 1
            else:
                if self.is_alive(row, column, radius, rows, columns):
                    i = i - 1
                else:
                    self.grid[row][column].state = True
                    self.grid[row][column].id = i
                    self.grid[row][column].color = (np.random.randint(255),
                                                    np.random.randint(255),
                                                    np.random.randint(255))
                    i = i + 1

    def is_alive(self, row, column, radius, rows, columns):
        alive = False
        for i in range(row - radius, row + radius + 1):
            for j in range(column - radius, column + radius + 1):
                if 0 <= i < rows and 0 <= j < columns:
                    if self.grid[i][j].state:
                        alive = True
        return alive

    def grain_growth_color(self, neighbours):
        Colors = {}
        if not neighbours:
            None
        else:
            for i in neighbours:
                if i.state:
                    if i.color in Colors:
                        Colors[i.color] = Colors[i.color] + 1
                    else:
                        Colors[i.color] = 1

            if Colors:
                max_value = max(Colors.values())
                for key, value in Colors.items():
                    if value == max_value:
                        return key

    def caluclate_next_state(self):

        next_state = [[Cell() for i in range(0, self.number_of_columns)] for j in range(0, self.number_of_rows)]

        for i in range(self.number_of_rows):
            for j in range(self.number_of_columns):
                if self.boundary_condition(i, j).state is True:
                    next_state[i][j] = self.grid[i][j]
                else:
                    neighbours = self.get_neighbour(i, j)
                    color = self.grain_growth_color(neighbours)
                    if color is not None:
                        next_state[i][j].state = True
                        next_state[i][j].color = color
                        self.count_grain = self.count_grain + 1
                        next_state[i][j].id = self.count_grain
        self.grid = next_state
