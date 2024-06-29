from graphics import Window, Line, Point, MyLine, Cell, Maze


def main():
    win = Window(800, 600)
    line = Line(Point(10, 10), Point(100,100))
    #win.draw_line(line, "black")
    # myline = MyLine(10, 10, 10, 100)
    # win.draw_line(myline, "red")
    # myline = MyLine(10, 100, 100, 100)
    # win.draw_line(myline, "yellow")
    # myline = MyLine(100, 10, 100, 100)
    # win.draw_line(myline, "blue")
    '''
    cell_nw = Cell(win, 10, 10, 110, 110)
    cell_nw.has_right_wall = False
    cell_ne = Cell(win, 110, 10, 210, 110)
    cell_ne.has_left_wall = False
    cell_ne.has_bottom_wall = False
    cell_sw = Cell(win, 10, 110, 110, 210)
    cell_sw.has_right_wall = False
    cell_se = Cell(win, 110, 110, 210, 210)
    cell_se.has_top_wall = False
    cell_se.has_left_wall = False
    win.draw_cell(cell_nw)
    win.draw_cell(cell_ne)
    win.draw_cell(cell_sw)
    win.draw_cell(cell_se)
    cell_nw.draw_move(cell_ne, False)
    cell_ne.draw_move(cell_se, True)

    win.draw_cell(cell2)
    for j in range(0, 10):
        for i in range(0, 15):
            cell_grid = Cell(win, 5 + (i * 50), 5 + (j * 50), 55 + (i * 50), 55 + (j * 50)) 
            win.draw_cell(cell_grid)
    
    '''
    #Maze(x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None)
    maze = Maze(5, 5, 11, 14, 50, 50, win)
    maze.solve()

    win.wait_for_close()


main()