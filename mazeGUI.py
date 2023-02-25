from enum import Enum
from typing import List, NamedTuple
from tkinter import *
from tkinter.ttk import *
from MCO1 import find_start, find_end, a_star, get_maze_size, get_maze

# Coded by glee Feb 26
# still need animation for a_star
# I suggest to update the parts with "TODO"
# suggested references 1: https://github.com/davecom/MazeSolvingGUI/blob/master/maze_gui.py
# suggested reference 2: https://github.com/davecom/MazeSolvingGUI/blob/master/data_structures.py

#not sure sa purpose neto but keep it here for now
#T = TypeVar('T')

class Cell(str, Enum):
    EMPTY = " "
    WALL = "#"
    START = "S"
    GOAL = "G"
    EXPLORED = "E"
    CURRENT = "C"
    FRONTIER = "F"
    PATH = "*"

# class MazeLocation(NamedTuple):
#     row: int
#     column: int

#     def __str__(self):
#         return f"({self.row}, {self.column})"

class MazeGUI:
    def __init__(self, start, goal) -> None:
        maze = get_maze()
        size = get_maze_size()

        self.rows = size
        self.columns = size
        self.start = start
        self.goal = goal
        
        
        #fill the grid space, walls, start, and goal
        

        self.grid: List[List[Cell]] = [[Cell.EMPTY for c in range(size)] for r in range(size)]
        for row in range(size):
            for column in range(size):
                if maze[row][column] == ".":
                    self.grid[row][column] = Cell.EMPTY
                if maze[row][column] == "#":
                    self.grid[row][column] = Cell.WALL
                elif maze[row][column] == "S":
                    self.grid[row][column] = Cell.START
                elif maze[row][column] == "G":
                    self.grid[row][column] = Cell.GOAL

        self.setup_GUI()

    def setup_GUI(self):
        self.root: Tk = Tk()
        self.root.title("Heuristic Mazebot")
        Grid.rowconfigure(self.root, 0, weight = 1)
        Grid.columnconfigure(self.root, 0, weight = 1)

        #main window
        frame: Frame = Frame(self.root)
        frame.grid(row = 0, column = 0, sticky = N + S + E + W)

        #style for widgets
        style: Style = Style()
        style.theme_use('classic')
        style.configure("BG.TLabel", foreground = "black", font = ('Helvetica', 26))
        style.configure("BG.TButton", foreground = "black", font = ('Helvetica', 26))
        style.configure("BG.TListBox", foreground = "black", font = ('Helvetica', 26))
        style.configure("BG.TComboBox", foreground = "black", font = ('Helvetica', 26))
        style.configure(" ", foreground = "black", background = "white")
        style.configure(Cell.EMPTY.value + ".TLabel", foreground = "black", background = "white", font = ('Helvetica', 26))
        style.configure(Cell.WALL.value + ".TLabel", foreground = "white", background = "black", font = ('Helvetica', 26))
        style.configure(Cell.START.value + ".TLabel", foreground = "black", background = "green", font = ('Helvetica', 26))
        style.configure(Cell.GOAL.value + ".TLabel", foreground = "black", background = "red", font = ('Helvetica', 26))
        style.configure(Cell.PATH.value + ".TLabel", foreground = "black", background = "cyan", font = ('Helvetica', 26))
        style.configure(Cell.EXPLORED.value + ".TLabel", foreground = "black", background = "yellow", font = ('Helvetica', 26))
        style.configure(Cell.CURRENT.value + ".TLabel", foreground = "black", background = "blue", font = ('Helvetica', 26))
        style.configure(Cell.FRONTIER.value + ".TLabel", foreground = "black", background = "orange", font = ('Helvetica', 26))

        #put labels on side
        for row in range(self.rows):
            Grid.rowconfigure(frame, row, weight = 1)
            row_label: Label = Label(frame, text=str(row), style="BG.TLabel", anchor="center")
            row_label.grid(row=row, column = 0, sticky = N + S + E + W)
            Grid.rowconfigure(frame, row, weight = 1)
            Grid.grid_columnconfigure(frame, 0, weight=1)

        #put labels on bottom
        for column in range(self.columns):
            Grid.columnconfigure(frame, column, weight = 1)
            column_label: Label = Label(frame, text=str(column), style="BG.TLabel", anchor="center")
            column_label.grid(row=self.rows, column=column + 1, sticky = N + S + E + W)
            Grid.rowconfigure(frame, self.rows, weight = 1)
            Grid.columnconfigure(frame, column + 1, weight = 1)

        #setup grid display
        self.cell_labels: List[List[Label]] = [[Label(frame, anchor="center") for c in range(self.columns)] for r in range(self.rows)]

        for row in range(self.rows):
            for column in range(self.columns):
                cell_label: Label = self.cell_labels[row][column]
                Grid.columnconfigure(frame, column+1, weight = 1)
                Grid.rowconfigure(frame, row, weight = 1)
                cell_label.grid(row=row, column=column + 1, sticky = N + S + E + W)
        
        self.display_grid()

        #TODO: edit function at command for animation
        #setup buttons
        heuristic_button: Button = Button(frame, style="BG.TButton", text="run heuristic search", command = a_star(get_maze_size(), get_maze()))
        heuristic_button.grid(row=self.rows + 2, column = 0, columnspan = 6, sticky = N + S + E + W)
        Grid.rowconfigure(frame, self.rows + 2, weight = 1)

        #setup data structure displays
        frontier_label: Label = Label(frame, text = "Frontier", style = "BG.TLabel", anchor = "center")
        frontier_label.grid(row = 0, column = self.columns + 2, columnspan = 3, sticky = N + S + E + W)
        explored_label: Label = Label(frame, text = "Explored", style = "BG.TLabel", anchor = "center")
        explored_label.grid(row = self.rows // 2, column = self.columns + 2, columnspan = 3, sticky = N + S + E + W)
        Grid.columnconfigure(frame, self.columns + 2, weight = 1)
        Grid.columnconfigure(frame, self.columns + 3, weight = 1)
        Grid.columnconfigure(frame, self.columns + 4, weight = 1)
        self.frontier_listbox: Listbox = Listbox(frame, font=('Helvetica', 14))
        self.frontier_listbox.grid(row = 1, column = self.columns + 2, columnspan = 3, rowspan = self.rows // 2-1, sticky = N + S + E + W)
        self._explored_listbox: Listbox = Listbox(frame, font=("Helvetica", 14))
        self._explored_listbox.grid(row=self.rows // 2 + 1, column=self.columns + 2, columnspan=3,
                                    rowspan=self.rows // 2 - 1,
                                    sticky=N + S + E + W)
        interval_label: Label = Label(frame, text="Interval", style="BG.TLabel", anchor="center")
        interval_label.grid(row=self.rows + 1, column=self.columns + 2, columnspan=3, sticky=N + S + E + W)
        self._interval_box: Combobox = Combobox(frame, state="readonly", values=[1, 2, 3, 4, 5], justify="center",
                                                style="BG.TCombobox")
        self._interval_box.set(2)
        self._interval_box.grid(row=self.rows + 2, column=self.columns + 2, columnspan=3, sticky=N + S + E + W)
        # pack and go
        frame.pack(fill="both", expand=True)
        self.root.mainloop()

    def display_grid(self):
        self.grid[self.start[0]][self.start[1]] = Cell.START #check
        self.grid[self.goal[0]][self.goal[1]] = Cell.GOAL #check
        for row in range(self.rows):
            for column in range(self.columns):
                cell: Cell = self.grid[row][column]
                cell_label: Label = self.cell_labels[row][column]
                cell_label.configure(style = cell.value + ".TLabel")

if __name__ == "__main__":
    maze_size = get_maze_size()
    maze = get_maze()
    start = find_start(maze_size, maze)
    end = find_end(maze_size, maze)
    m: MazeGUI = MazeGUI(start, end)
