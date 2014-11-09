# -*- encoding: utf-8 -*-
import os


def display(grid):
  def _print_horizontal_line(h_range):
    length = len(h_range) + 2
    print "━" * length

  def _print_row(row):
    print u"┃%s┃" % row

  os.system("clear")
  x_max, x_min = max(grid).x, min(grid).x
  key = lambda c: c.y
  y_max, y_min = max(grid, key=key).y, min(grid, key=key).y

  horizontal_range = range(x_min, x_max + 1)
  vertical_range = reversed(range(y_min, y_max + 1))

  _print_horizontal_line(horizontal_range)

  for y in vertical_range:
    row = ""
    for x in horizontal_range:
      row += u"█" if grid.Cell(x, y) in grid.live_cells else " "
    row += " " * (len(horizontal_range) - len(row))
    _print_row(row)

  _print_horizontal_line(horizontal_range)

