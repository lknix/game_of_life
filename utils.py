# -*- encoding: utf-8 -*-
import os
from functools import partial, wraps


def tailrec(f):
  @wraps(f)
  def _wrapper(*args, **kwargs):
    f_ref = f.func_globals[f.func_name]
    f.func_globals[f.func_name] = partial(partial, f)
    f_call = partial(f, *args, **kwargs)
    while isinstance(f_call, partial):
      f_call = f_call()
    f.func_globals[f.func_name] = f_ref
  return _wrapper


def len(obj):
  try:
    return obj.__len__()
  except AttributeError:
    return reduce(lambda length, _: length + 1, iter(obj), 0)


def display(grid):
  def _print_horizontal_line(h_range):
    length = len(h_range) + 2
    print u"━" * length

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
