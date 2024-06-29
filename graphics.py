from tkinter import Tk, BOTH, Canvas
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def sleep(self):
        self.__root.after(50)

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)

    def draw_cell(self, cell):
        cell.draw()
        
    pass

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    pass

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

        pass
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

        pass
    
    pass

class Cell:
    def __init__(self, x1, y1, x2, y2, win = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = False

        pass

    def draw(self):
        if self._win is None:
            return
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black")
        pass

    def draw_move(self, to_cell, undo=False):
        center_self_x = self._x1 + ((self._x2 - self._x1) / 2)
        center_self_y = self._y1 + ((self._y2 - self._y1) / 2)
        center_to_x = to_cell._x1 + ((to_cell._x2 - to_cell._x1) / 2)
        center_to_y = to_cell._y1 + ((to_cell._y2 - to_cell._y1) / 2)
        if undo:
            self.line_color = "gray"
        else:
            self.line_color = "red"

        move_line = Line(Point(center_self_x, center_self_y), Point(center_to_x, center_to_y))
        self._win.draw_line(move_line, self.line_color)
    pass

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        self._create_cells()
        pass

    def _create_cells(self):
        self._cells = []
        rows = []
        for j in range(0, self.num_rows):
            #create a list of None types
            rows.insert(j, None)
        #print(rows)
        for i in range(0, self.num_cols):
            self._cells.insert(i, rows.copy())

        for j in range(0, self.num_rows):
            for i in range(0, self.num_cols):
                cell_grid = Cell(self.x1 + (i * self.cell_size_x), self.y1 + (j * self.cell_size_y), self.x1 + self.cell_size_x + (i * self.cell_size_x), self.y1+ self.cell_size_y + (j * self.cell_size_y), self._win) 
                self._cells[i][j] = cell_grid
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self._draw_cell()
        pass

    def _reset_cells_visited(self):
        for j in range(0, self.num_rows):
            for i in range(0, self.num_cols):
                self._cells[i][j].visited = False
        pass
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_left_wall = False
        self._cells[self.num_cols - 1][self.num_rows - 1].has_right_wall = False
        pass

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            #2 check 4 directions
            up = False
            down = False
            left = False
            right = False
            if i - 1 >= 0: 
                if not self._cells[i - 1][j].visited:
                    left = True
            if i + 1 < self.num_cols:
                if not self._cells[i + 1][j].visited:
                    right = True
            if j - 1 >= 0:
                if not self._cells[i][j - 1].visited:
                    up = True
            if j + 1 < self.num_rows:
                if not self._cells[i][j + 1].visited:
                    down = True
            # 3. 
            if not up and not down and not left and not right:
                self._cells[i][j].draw
                return
            # 4.
            if self._seed is not None:
                random.seed(self._seed)
            possible_dirs = []
            if up:
                possible_dirs.append("up")
            if down:
                possible_dirs.append("down")
            if left:
                possible_dirs.append("left")
            if right:
                possible_dirs.append("right")
            direction = random.choice(possible_dirs)
            # 5.
            if direction == "up":
                #print("Up!")
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
                self._break_walls_r(i, j - 1)
            elif direction == "down":
                #print("Down!")
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
                self._break_walls_r(i, j + 1)
            elif direction == "left":
                #print("Left!")
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
                self._break_walls_r(i - 1, j)
            elif direction == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
                self._break_walls_r(i + 1, j)
                #print("Right!") 
        
        pass

    def _draw_cell(self):
        if self._win is None:
            return
        for j in range(0, self.num_rows):
            for i in range(0, self.num_cols):
                self._win.draw_cell(self._cells[i][j])
                self._animate()
        pass

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        self._win.sleep()
        pass

    def solve(self):
        self._solve_r(0, 0)
        pass

    def _solve_r(self, i, j):
        # 1. Call the _animate method
        self._animate()
        # 2. Mark current cell as visited
        self._cells[i][j].visited = True
        # 3. If you are at the "end" cell (the goal) then return True
        if i == (self.num_cols - 1) and j == (self.num_rows - 1):
            return True
        # 4 For each direction
        # 4.1 If there is a cell in that direction and 
        #   no wall blocking and (This first two may be redudant except for the start cell.)
        #       cell has not been visited.
        #Right
        if i + 1 < self.num_cols:
            if not self._cells[i][j].has_right_wall:
                if not self._cells[i + 1][j].visited:
                    self._cells[i][j].draw_move(self._cells[i + 1][j])
                    if self._solve_r(i + 1, j):
                        return True
                    self._cells[i][j].draw_move(self._cells[i + 1][j], True)
         #Down
        if j + 1 < self.num_rows:
            if not self._cells[i][j].has_bottom_wall:
                if not self._cells[i][j + 1].visited:
                    self._cells[i][j].draw_move(self._cells[i][j + 1])
                    if self._solve_r(i, j + 1):
                        return True
                    self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        #Left
        if i - 1 >= 0: 
            if not self._cells[i][j].has_left_wall:
                if not self._cells[i - 1][j].visited:
                    #4.1.1 Draw a move between the current cell and that cell.
                    self._cells[i][j].draw_move(self._cells[i - 1][j])
                    #4.1.2 Call _solve_r recursively to move to that cell. Cont...
                    if self._solve_r(i - 1, j):
                        #4.1.2 ...Cont: If that cell returns True then just return True don't worry about other directions
                        return True
                    #4.1.3
                    self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        #Up
        if j - 1 >= 0:
            if not self._cells[i][j].has_top_wall:
                if not self._cells[i][j - 1].visited:
                    self._cells[i][j].draw_move(self._cells[i][j - 1])
                    if self._solve_r(i, j - 1):
                        return True
                    self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        #5. If none of the directions worked out, return False
        # I changed the order to prefer Right, then down, then left and then up as that is more in line the natural direction we do want to go.
        return False
                
        


# ---------- My stuff below here ----------

class MyLine:
    def __init__(self, x_start, y_start, x_end, y_end):
        self.start = (x_start, y_start)
        self.end = (x_end, y_end)
        self.x = 0
        self.y = 1

        pass

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.start[self.x], self.start[self.y], self.end[self.x], self.end[self.y], fill=fill_color, width=2)

        pass
    
    pass